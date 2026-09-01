CREATE TABLE IF NOT EXISTS sponsors (
  id TEXT PRIMARY KEY,
  status TEXT NOT NULL DEFAULT 'pending', -- pending | approved | rejected
  slot INTEGER, -- 1..5 once approved, NULL while pending/rejected
  name TEXT NOT NULL,
  blurb TEXT NOT NULL,
  website_url TEXT NOT NULL,
  logo_url TEXT NOT NULL,
  customer_email TEXT,
  polar_order_id TEXT,
  polar_subscription_id TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  reviewed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_sponsors_status ON sponsors (status);
