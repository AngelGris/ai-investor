from datetime import datetime, timezone

from execution.models.portfolio_state import PortfolioState
from execution.models.position import Position
from persistence.database import get_connection


class PortfolioRepository:
    def load(self) -> PortfolioState:
        conn = get_connection()

        row = conn.execute(
            "SELECT * FROM portfolio_snapshots ORDER BY snapshot_id DESC LIMIT 1"
        ).fetchone()

        if row is None:
            # Initial portfolio
            state = PortfolioState(
                timestamp=datetime.now(timezone.utc),
                cash=5_000.0,
                positions={},
                trades=[],
                realized_pnl=0.0,
                total_commissions=0.0,
            )
            self.save(state=state, reason="initial_state")
            return state

        positions = {}
        for p in conn.execute(
            "SELECT * FROM position_snapshots where snapshot_id = ?",
            (row["snapshot_id"],),
        ):
            positions[p["ticker"]] = Position(
                ticker=p["ticker"],
                quantity=p["quantity"],
                avg_price=p["avg_price"],
                stop_loss_pct=p["stop_loss_pct"],
                unrealized_pnl=None,
                allocation_pct=None,
            )

        conn.close()

        return PortfolioState(
            timestamp=datetime.fromisoformat(row["timestamp"]),
            cash=row["cash"],
            positions=positions,
            trades=[],
            realized_pnl=row["realized_pnl"],
            total_commissions=row["total_commissions"],
        )

    def save(self, state: PortfolioState, reason: str):
        conn = get_connection()

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO portfolio_snapshots
            (timestamp, cash, realized_pnl, total_commissions, reason)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                state.timestamp.isoformat(),
                state.cash,
                state.realized_pnl,
                state.total_commissions,
                reason,
            ),
        )

        snapshot_id = cursor.lastrowid

        for pos in state.positions.values():
            cursor.execute(
                """
                INSERT INTO position_snapshots
                (snapshot_id, ticker, quantity, avg_price, stop_loss_pct)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    pos.ticker,
                    pos.quantity,
                    pos.avg_price,
                    pos.stop_loss_pct,
                ),
            )

        conn.commit()
        conn.close()
