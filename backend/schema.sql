-- CreatorPulse Database Schema for Supabase
-- Run this SQL in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    timezone TEXT DEFAULT 'America/Los_Angeles',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Bundles table
CREATE TABLE IF NOT EXISTS bundles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key TEXT NOT NULL,
    label TEXT NOT NULL,
    description TEXT,
    is_preset BOOLEAN DEFAULT FALSE,
    sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sources table (for tracking RSS feeds, Twitter handles, YouTube channels)
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bundle_id UUID REFERENCES bundles(id) ON DELETE CASCADE,
    type TEXT DEFAULT 'rss' CHECK (type IN ('rss', 'twitter', 'youtube')),
    source_identifier TEXT NOT NULL,  -- RSS URL, Twitter handle, or YouTube channel ID
    label TEXT,  -- Display name for the source
    metadata JSONB DEFAULT '{}'::jsonb,  -- Type-specific data (follower count, video count, etc.)
    last_crawled TIMESTAMP WITH TIME ZONE,
    signal_score FLOAT DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Drafts table
CREATE TABLE IF NOT EXISTS drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bundle_id UUID REFERENCES bundles(id) ON DELETE SET NULL,
    bundle_name TEXT NOT NULL,
    topic TEXT,
    tone TEXT DEFAULT 'professional',
    generated_html TEXT NOT NULL,
    edited_html TEXT,
    status TEXT DEFAULT 'draft',
    readiness_score INTEGER,
    sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    scheduled_for TIMESTAMP WITH TIME ZONE,
    -- Voice training columns
    voice_training_used BOOLEAN DEFAULT FALSE,
    voice_samples_count INTEGER DEFAULT 0,
    generation_metadata JSONB DEFAULT NULL
);

-- Auto Newsletters table (Supabase-backed)
CREATE TABLE IF NOT EXISTS auto_newsletters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bundle_id UUID REFERENCES bundles(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    schedule_time TIME WITH TIME ZONE DEFAULT '08:00:00-00',
    schedule_frequency TEXT DEFAULT 'daily', -- daily | weekly | monthly
    schedule_day INTEGER, -- 1-7 (Mon-Sun) or 1-31
    email_recipients TEXT[] DEFAULT ARRAY[]::TEXT[],
    last_generated TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    draft_id UUID REFERENCES drafts(id) ON DELETE CASCADE,
    section_id TEXT,
    reaction TEXT CHECK (reaction IN ('thumbs_up', 'thumbs_down')),
    edit_diff TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics table
CREATE TABLE IF NOT EXISTS analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    draft_id UUID REFERENCES drafts(id) ON DELETE CASCADE,
    sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
    opened_at TIMESTAMP WITH TIME ZONE,
    clicked_at TIMESTAMP WITH TIME ZONE,
    recipient_email TEXT,
    token TEXT,
    last_clicked_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ESP Credentials table (encrypted)
CREATE TABLE IF NOT EXISTS esp_credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider TEXT NOT NULL CHECK (provider IN ('sendgrid', 'mailgun', 'smtp')),
    encrypted_credentials TEXT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content Entries cache (temporary storage for RSS, Twitter, YouTube)
CREATE TABLE IF NOT EXISTS content_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,  -- 'rss', 'twitter', 'youtube'
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    summary TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    author TEXT,
    content_hash TEXT UNIQUE,
    metadata JSONB DEFAULT '{}'::jsonb,  -- Type-specific data (engagement, video duration, etc.)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '48 hours'
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_drafts_user_id ON drafts(user_id);
CREATE INDEX IF NOT EXISTS idx_drafts_status ON drafts(status);
CREATE INDEX IF NOT EXISTS idx_drafts_created_at ON drafts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_user_id ON auto_newsletters(user_id);
CREATE INDEX IF NOT EXISTS idx_auto_newsletters_active ON auto_newsletters(is_active);
CREATE INDEX IF NOT EXISTS idx_bundles_user_id ON bundles(user_id);
CREATE INDEX IF NOT EXISTS idx_bundles_is_preset ON bundles(is_preset);
CREATE INDEX IF NOT EXISTS idx_analytics_draft_id ON analytics(draft_id);
CREATE INDEX IF NOT EXISTS idx_analytics_token ON analytics(token);
CREATE INDEX IF NOT EXISTS idx_content_entries_source_id ON content_entries(source_id);
CREATE INDEX IF NOT EXISTS idx_content_entries_source_type ON content_entries(source_type);
CREATE INDEX IF NOT EXISTS idx_content_entries_expires_at ON content_entries(expires_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bundles_updated_at BEFORE UPDATE ON bundles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drafts_updated_at BEFORE UPDATE ON drafts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_auto_newsletters_updated_at BEFORE UPDATE ON auto_newsletters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_esp_credentials_updated_at BEFORE UPDATE ON esp_credentials
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE bundles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE esp_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE auto_newsletters ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- RLS Policies for bundles
CREATE POLICY "Users can view own bundles and presets" ON bundles
    FOR SELECT USING (user_id = auth.uid() OR is_preset = TRUE);

CREATE POLICY "Users can create own bundles" ON bundles
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own bundles" ON bundles
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own bundles" ON bundles
    FOR DELETE USING (user_id = auth.uid());

-- RLS Policies for drafts
CREATE POLICY "Users can view own drafts" ON drafts
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create own drafts" ON drafts
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own drafts" ON drafts
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own drafts" ON drafts
    FOR DELETE USING (user_id = auth.uid());

-- RLS Policies for auto_newsletters
CREATE POLICY "Users can view own auto newsletters" ON auto_newsletters
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create own auto newsletters" ON auto_newsletters
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own auto newsletters" ON auto_newsletters
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own auto newsletters" ON auto_newsletters
    FOR DELETE USING (user_id = auth.uid());

-- RLS Policies for feedback
CREATE POLICY "Users can view feedback on own drafts" ON feedback
    FOR SELECT USING (draft_id IN (SELECT id FROM drafts WHERE user_id = auth.uid()));

CREATE POLICY "Users can create feedback on own drafts" ON feedback
    FOR INSERT WITH CHECK (draft_id IN (SELECT id FROM drafts WHERE user_id = auth.uid()));

-- RLS Policies for analytics
CREATE POLICY "Users can view analytics on own drafts" ON analytics
    FOR SELECT USING (draft_id IN (SELECT id FROM drafts WHERE user_id = auth.uid()));

CREATE POLICY "Users can create analytics on own drafts" ON analytics
    FOR INSERT WITH CHECK (draft_id IN (SELECT id FROM drafts WHERE user_id = auth.uid()));

-- RLS Policies for ESP credentials
CREATE POLICY "Users can view own ESP credentials" ON esp_credentials
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can manage own ESP credentials" ON esp_credentials
    FOR ALL USING (user_id = auth.uid());

-- Insert preset bundles
INSERT INTO bundles (id, key, label, description, is_preset, sources) VALUES
    ('00000000-0000-0000-0000-000000000001', 'ai-ml-trends', 'AI & ML Trends', 'The latest news, research, and breakthroughs in Artificial Intelligence and Machine Learning.', TRUE, '["https://techcrunch.com/category/artificial-intelligence/feed/", "https://venturebeat.com/category/ai/feed/"]'::jsonb),
    ('00000000-0000-0000-0000-000000000002', 'creator-economy', 'Creator Economy', 'Insights on the creator economy, monetization, and platform trends.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000003', 'marketing-growth', 'Marketing & Growth', 'Growth hacking, marketing strategies, and conversion optimization.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000004', 'startups-innovation', 'Startups & Innovation', 'Startup news, funding rounds, and innovation in tech.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000005', 'cybersecurity-privacy', 'Cybersecurity & Privacy', 'Security vulnerabilities, privacy concerns, and data protection news.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000006', 'productivity-workflow', 'Productivity & Workflow Tools', 'Tools and techniques to boost productivity and streamline workflows.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000007', 'sustainability-future-tech', 'Sustainability & Future Tech', 'Green technology, climate tech, and sustainable innovation.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000008', 'tech-policy-regulation', 'Tech Policy & Regulation', 'Regulatory changes, policy debates, and legal issues in tech.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000009', 'health-wellness-tech', 'Health & Wellness Tech', 'Digital health, wellness apps, and medical technology.', TRUE, '[]'::jsonb),
    ('00000000-0000-0000-0000-000000000010', 'mindset-creativity', 'Mindset & Creativity', 'Creative thinking, mental models, and personal development.', TRUE, '[]'::jsonb)
ON CONFLICT DO NOTHING;

-- Create cleanup function for expired content entries
CREATE OR REPLACE FUNCTION cleanup_expired_content_entries()
RETURNS void AS $$
BEGIN
    DELETE FROM content_entries WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- Note: Set up a cron job or use pg_cron extension to run cleanup_expired_content_entries() periodically

