from execution.models.portfolio_state import PortfolioState
from portfolio_calculator.dataclasses import PortfolioMetrics, PositionMetrics


class PortfolioCalculator:
    @staticmethod
    def calculate(
        state: PortfolioState,
        prices: dict[str, float],
    ) -> PortfolioMetrics:
        """
        Compute derived portfolio metrics from a portfolio state and market prices.
        """
        position_values: dict[str, float] = {}
        position_pnls: dict[str, float] = {}

        # --- 1. Compute position market values & unrealized PnL ---
        for ticker, position in state.positions.items():
            if ticker not in prices:
                raise ValueError(f"Missing price for ticker {ticker}")

            price = prices[ticker]
            market_value = position.quantity * price.price
            unrealized_pnl = (price.price - position.avg_price) * position.quantity

            position_values[ticker] = market_value
            position_pnls[ticker] = unrealized_pnl

        # --- 2. Compute totals ---
        positions_value = sum(position_values.values())
        total_value = state.cash + positions_value
        total_unrealized_pnl = sum(position_pnls.values())

        if total_value <= 0:
            raise ValueError("Total portfolio value must be positive")

        # --- 3. Build PositionMetrics ---
        positions_metrics: dict[str, PositionMetrics] = {}

        for ticker, position in state.positions.items():
            market_value = position_values[ticker]
            allocation_pct = market_value / total_value

            positions_metrics[ticker] = PositionMetrics(
                ticker=ticker,
                quantity=position.quantity,
                avg_price=position.avg_price,
                market_price=prices[ticker],
                market_value=market_value,
                unrealized_pnl=position_pnls[ticker],
                allocation_pct=allocation_pct,
            )

        # --- 4. Cash allocation ---
        cash_allocation_pct = state.cash / total_value

        return PortfolioMetrics(
            total_value=total_value,
            cash=state.cash,
            cash_allocation_pct=cash_allocation_pct,
            unrealized_pnl=total_unrealized_pnl,
            realized_pnl=state.realized_pnl,
            total_commissions=state.total_commissions,
            positions=positions_metrics,
        )
