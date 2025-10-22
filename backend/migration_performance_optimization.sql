-- Performance Optimization Migration
-- Add indexes for better query performance

-- Indexes for analytics queries
CREATE INDEX IF NOT EXISTS idx_analytics_draft_id ON analytics(draft_id);
CREATE INDEX IF NOT EXISTS idx_analytics_sent_at ON analytics(sent_at);
CREATE INDEX IF NOT EXISTS idx_analytics_opened_at ON analytics(opened_at);
CREATE INDEX IF NOT EXISTS idx_analytics_clicked_at ON analytics(clicked_at);

-- Indexes for drafts queries
CREATE INDEX IF NOT EXISTS idx_drafts_user_id ON drafts(user_id);
CREATE INDEX IF NOT EXISTS idx_drafts_status ON drafts(status);
CREATE INDEX IF NOT EXISTS idx_drafts_created_at ON drafts(created_at);
CREATE INDEX IF NOT EXISTS idx_drafts_sent_at ON drafts(sent_at);

-- Indexes for bundles queries
CREATE INDEX IF NOT EXISTS idx_bundles_user_id ON bundles(user_id);
CREATE INDEX IF NOT EXISTS idx_bundles_is_preset ON bundles(is_preset);

-- Indexes for auto_newsletters queries
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_user_id ON auto_newsletters(user_id);
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_is_active ON auto_newsletters(is_active);

-- Indexes for sources queries
CREATE INDEX IF NOT EXISTS idx_sources_bundle_id ON sources(bundle_id);
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(type);
CREATE INDEX IF NOT EXISTS idx_sources_is_active ON sources(is_active);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_drafts_user_status ON drafts(user_id, status);
CREATE INDEX IF NOT EXISTS idx_analytics_draft_sent ON analytics(draft_id, sent_at);
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_user_active ON auto_newsletters(user_id, is_active);

-- Add partial indexes for better performance on filtered queries
CREATE INDEX IF NOT EXISTS idx_drafts_sent ON drafts(user_id, sent_at) WHERE status = 'sent';
CREATE INDEX IF NOT EXISTS idx_analytics_opened ON analytics(draft_id) WHERE opened_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_analytics_clicked ON analytics(draft_id) WHERE clicked_at IS NOT NULL;
