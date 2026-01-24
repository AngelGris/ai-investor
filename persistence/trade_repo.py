import json
from abc import abstractmethod
from typing import Iterable

from execution.models.trade import Trade
from persistence.database import get_connection


class TradeRepository:
    @abstractmethod
    def save(trade: Trade) -> None:
        """Saves a transaction to the repository."""
        conn = get_connection()

        conn.cursor.execute(
            """
            INSERT INTO trades (
                trade_id,
                portfolio_id,
                executed_at,
                ticker,
                side,
                quantity,
                price,
                notional,
                commission,
                strategy,
                reason,
                metadata,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            TradeRepository._row_from_trade(trade),
        )
        conn.commit()

    @abstractmethod
    def save_many(trades: Iterable[Trade]) -> None:
        """Saves multiple transactions to the repository."""
        conn = get_connection()
        conn.executemany(
            """
            INSERT INTO trades (
                trade_id,
                portfolio_id,
                executed_at,
                ticker,
                side,
                quantity,
                price,
                notional,
                commission,
                strategy,
                reason,
                metadata,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [TradeRepository._row_from_trade(t) for t in trades],
        )
        conn.commit()

    @staticmethod
    def _row_from_trade(trade: Trade) -> tuple:
        return (
            str(trade.trade_id),
            str(trade.portfolio_id),
            trade.executed_at.isoformat(),
            trade.ticker,
            trade.side,
            trade.quantity,
            trade.price,
            trade.notional,
            trade.commission,
            trade.strategy,
            trade.reason,
            json.dumps(trade.metadata) if trade.metadata else None,
            trade.notes,
        )
