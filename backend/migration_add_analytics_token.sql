-- Add token field to analytics table for per-recipient tracking
ALTER TABLE analytics ADD COLUMN IF NOT EXISTS token TEXT;
ALTER TABLE analytics ADD COLUMN IF NOT EXISTS last_clicked_url TEXT;

-- Create index on token for faster lookups
CREATE INDEX IF NOT EXISTS idx_analytics_token ON analytics(token);
