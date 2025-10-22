-- Migration: Add auto-newsletter functionality
-- This adds the ability for users to set up automated newsletter generation

-- Create auto_newsletters table
CREATE TABLE IF NOT EXISTS auto_newsletters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bundle_id UUID NOT NULL REFERENCES bundles(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT true,
    schedule_time TIME DEFAULT '08:00:00',  -- Default 8 AM
    schedule_frequency VARCHAR(20) DEFAULT 'daily',  -- daily, weekly, monthly
    schedule_day INTEGER,  -- For weekly (1-7) or monthly (1-31)
    email_recipients TEXT[],  -- Array of email addresses to notify
    last_generated TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for efficient querying
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_user_id ON auto_newsletters(user_id);
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_active ON auto_newsletters(is_active) WHERE is_active = true;

-- Add RLS policies
ALTER TABLE auto_newsletters ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own auto-newsletters
CREATE POLICY "Users can manage their own auto-newsletters" ON auto_newsletters
    FOR ALL USING (auth.uid() = user_id);

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_auto_newsletter_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_auto_newsletter_updated_at
    BEFORE UPDATE ON auto_newsletters
    FOR EACH ROW
    EXECUTE FUNCTION update_auto_newsletter_updated_at();
