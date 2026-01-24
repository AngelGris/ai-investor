CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cash REAL NOT NULL,
    realized_pnl REAL NOT NULL,
    total_commissions REAL NOT NULL,
    reason TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS position_snapshots (
    snapshot_id INTEGER NOT NULL,
    ticker TEXT NOT NULL,
    quantity REAL NOT NULL,
    avg_price REAL NOT NULL,
    stop_loss_pct REAL NOT NULL,
    FOREIGN KEY(snapshot_id) REFERENCES portfolio_snapshots(snapshot_id)
);


CREATE TABLE IF NOT EXISTS trades (
    trade_id TEXT PRIMARY KEY,
    portfolio_id TEXT NOT NULL,

    executed_at TEXT NOT NULL,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL,              -- BUY / SELL

    quantity REAL NOT NULL,
    price REAL NOT NULL,
    notional REAL NOT NULL,
    commission REAL NOT NULL,

    strategy TEXT,
    reason TEXT,
    metadata TEXT,                   -- JSON: signals, slippage, etc.
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_trades_portfolio_time
ON trades (portfolio_id, executed_at);

CREATE INDEX IF NOT EXISTS idx_trades_ticker
ON trades (ticker);
