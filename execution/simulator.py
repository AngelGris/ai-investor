import math
import uuid
from datetime import datetime, timezone
from typing import List

from ai_agents.portfolio_allocation.schema import PortfolioAllocation
from execution.models.portfolio_state import PortfolioState
from execution.models.position import Position
from execution.models.trade import Trade


class ExecutionResult:
    def __init__(
        self, portfolio_state: PortfolioState, trades: List[Trade], timestamp: datetime
    ):
        self.portfolio_state = portfolio_state
        self.trades = trades
        self.timestamp = timestamp


class ExecutionSimulator:
    def __init__(
        self,
        market_data_provider,
        commission_per_trade: float,
        min_trade_value: float = 50.0,
    ):
        self.market_data_provider = market_data_provider
        self.commission = commission_per_trade
        self.min_trade_value = min_trade_value

    async def execute_allocation(
        self,
        allocation: PortfolioAllocation,
        portfolio_state: PortfolioState,
    ) -> ExecutionResult:
        """
        Apply a portfolio allocation to the current portfolio state by simulating trades.
        """
        trades: List[Trade] = []
        cash = portfolio_state.cash

        # Compute portfolio value
        portfolio_value = await self._portfolio_value(portfolio_state)

        # Build allocation lookup
        target_allocations = {p.ticker: p for p in allocation.positions}

        # Fetch prices once per ticker
        prices = {}
        for ticker in target_allocations.keys():
            quote = await self.market_data_provider.get_market_quote(ticker)
            prices[ticker] = quote.price

        # SELL phase (allocation-driven)
        for ticker, position in list(portfolio_state.positions.items()):
            price = prices.get(ticker)
            if price is None:
                continue

            target = target_allocations.get(ticker)

            # Full liquidation
            if target is None or target.allocation_pct == 0.0:
                quantity = position.quantity
                proceeds = quantity * price
                cash += proceeds - self.commission

                trades.append(
                    await self._make_trade(
                        ticker=ticker,
                        side="sell",
                        quantity=quantity,
                        price=price,
                        commission=self.commission,
                        reason="portfolio_allocation",
                        notes="Position removed by allocation",
                    )
                )

                portfolio_state.realized_pnl += (
                    price - position.avg_price
                ) * quantity - self.commission
                portfolio_state.total_commissions += self.commission
                portfolio_state.positions.pop(ticker)
                continue

            current_value = position.quantity * price
            target_value = (target.allocation_pct / 100.0) * portfolio_value
            delta_value = target_value - current_value

            if abs(delta_value) <= self.commission + self.min_trade_value:
                continue

            if delta_value < 0:
                quantity = min(math.floor(abs(delta_value) / price), position.quantity)

                if quantity <= 0:
                    continue

                proceeds = quantity * price
                cash += proceeds - self.commission

                trades.append(
                    await self._make_trade(
                        ticker=ticker,
                        side="sell",
                        quantity=quantity,
                        price=price,
                        commission=self.commission,
                        reason="portfolio_allocation",
                        notes="Partial position reduction by allocation",
                    )
                )

                portfolio_state.realized_pnl += (
                    price - position.avg_price
                ) * quantity - self.commission
                portfolio_state.total_commissions += self.commission

                position.quantity -= quantity
                if position.quantity == 0:
                    portfolio_state.positions.pop(ticker)

        # BUY phase (allocation-driven)
        for ticker, target in target_allocations.items():
            price = prices[ticker]
            position = portfolio_state.positions.get(ticker)

            current_value = position.quantity * price if position else 0.0
            target_value = (target.allocation_pct / 100.0) * portfolio_value
            delta_value = target_value - current_value

            if delta_value <= self.commission + self.min_trade_value:
                continue

            raw_quantity = math.floor(delta_value / price)
            if raw_quantity <= 0:
                continue

            required_cash = raw_quantity * price + self.commission
            if required_cash > cash:
                raw_quantity = math.floor((cash - self.commission) / price)
                if raw_quantity <= 0:
                    continue

            cost = raw_quantity * price
            cash -= cost + self.commission

            trades.append(
                await self._make_trade(
                    ticker=ticker,
                    side="buy",
                    quantity=raw_quantity,
                    price=price,
                    commission=self.commission,
                    reason="portfolio_allocation",
                    notes="Position increased by allocation",
                )
            )

            portfolio_state.total_commissions += self.commission

            if position:
                total_cost = (
                    position.avg_price * position.quantity + cost + self.commission
                )
                position.quantity += raw_quantity
                position.avg_price = total_cost / position.quantity
            else:
                portfolio_state.positions[ticker] = Position(
                    ticker=ticker,
                    quantity=raw_quantity,
                    avg_price=(cost + self.commission) / raw_quantity,
                    stop_loss_pct=target.stop_loss_pct,
                    unrealized_pnl=0.0,
                )

        portfolio_state.cash = cash
        portfolio_state.timestamp = datetime.now(timezone.utc)

        return ExecutionResult(
            portfolio_state=portfolio_state,
            trades=trades,
            timestamp=datetime.now(timezone.utc),
        )

    async def enforce_stop_losses(
        self,
        portfolio_state: PortfolioState,
    ) -> ExecutionResult:
        """
        Enforce stop-loss rules on the current portfolio state by simulating trades.
        """
        trades: List[Trade] = []
        cash = portfolio_state.cash

        for ticker, position in list(portfolio_state.positions.items()):
            quote = await self.market_data_provider.get_latest_quote(ticker)
            price = quote.price
            stop_loss_price = position.avg_price * (1 - position.stop_loss_pct / 100.0)

            if price >= stop_loss_price:
                continue

            quantity = position.quantity
            proceeds = quantity * price
            cash += proceeds - self.commission

            trades.append(
                await self._make_trade(
                    ticker=ticker,
                    side="sell",
                    quantity=quantity,
                    price=price,
                    commission=self.commission,
                    reason="stop_loss",
                    notes=f"Stop-loss triggered at {stop_loss_price:.2f}",
                )
            )

            portfolio_state.realized_pnl += (
                price - position.avg_price
            ) * quantity - self.commission
            portfolio_state.total_commissions += self.commission
            portfolio_state.positions.pop(ticker)

        portfolio_state.cash = cash
        portfolio_state.timestamp = datetime.now(timezone.utc)

        return ExecutionResult(
            portfolio_state=portfolio_state,
            trades=trades,
            timestamp=datetime.now(timezone.utc),
        )

    async def _portfolio_value(self, portfolio_state: PortfolioState) -> float:
        """
        Calculate the total value of the portfolio (cash + market value of positions).
        """
        value = portfolio_state.cash

        for position in portfolio_state.positions.values():
            quote = await self.market_data_provider.get_market_quote(position.ticker)
            value += position.quantity * quote.price

        return value

    async def _make_trade(
        self,
        ticker: str,
        side: str,
        quantity: int,
        price: float,
        commission: float,
        reason: str,
        notes: str = None,
    ) -> Trade:
        """
        Create a Trade object representing a simulated trade.
        """
        return Trade(
            trade_id=str(uuid.uuid4()),
            portfolio_id="simulated_portfolio",
            executed_at=datetime.now(timezone.utc),
            ticker=ticker,
            side=side,
            quantity=quantity,
            price=price,
            commission=commission,
            reason=reason,
            notes=notes,
        )
