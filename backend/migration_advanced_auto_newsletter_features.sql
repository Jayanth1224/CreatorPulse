-- Migration: Add advanced auto-newsletter features
-- This adds support for trend detection, spike detection, timezone support, and analytics

-- Add timezone support to auto_newsletters table
ALTER TABLE auto_newsletters 
ADD COLUMN IF NOT EXISTS timezone TEXT DEFAULT 'America/Los_Angeles';

-- Add trend detection settings
ALTER TABLE auto_newsletters 
ADD COLUMN IF NOT EXISTS trend_detection_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS trend_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
ADD COLUMN IF NOT EXISTS trend_sources TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Add spike detection settings
ALTER TABLE auto_newsletters 
ADD COLUMN IF NOT EXISTS spike_detection_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS spike_threshold FLOAT DEFAULT 2.0,
ADD COLUMN IF NOT EXISTS spike_timeframe_hours INTEGER DEFAULT 24;

-- Add custom scheduling options
ALTER TABLE auto_newsletters 
ADD COLUMN IF NOT EXISTS custom_schedule JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS schedule_enabled BOOLEAN DEFAULT TRUE;

-- Create trend_data table for storing trend information
CREATE TABLE IF NOT EXISTS trend_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    keyword TEXT NOT NULL,
    trend_score FLOAT NOT NULL,
    source TEXT NOT NULL,
    region TEXT DEFAULT 'US',
    data_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create spike_events table for tracking content spikes
CREATE TABLE IF NOT EXISTS spike_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auto_newsletter_id UUID REFERENCES auto_newsletters(id) ON DELETE CASCADE,
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    spike_score FLOAT NOT NULL,
    spike_reason TEXT,
    content_title TEXT,
    content_url TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);

-- Create auto_newsletter_analytics table for performance tracking
CREATE TABLE IF NOT EXISTS auto_newsletter_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auto_newsletter_id UUID REFERENCES auto_newsletters(id) ON DELETE CASCADE,
    draft_id UUID REFERENCES drafts(id) ON DELETE CASCADE,
    generation_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    content_quality_score FLOAT,
    trend_relevance_score FLOAT,
    spike_impact_score FLOAT,
    total_sources_used INTEGER DEFAULT 0,
    unique_trends_detected INTEGER DEFAULT 0,
    spike_events_processed INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_trend_data_keyword_date ON trend_data(keyword, data_date);
CREATE INDEX IF NOT EXISTS idx_trend_data_source ON trend_data(source);
CREATE INDEX IF NOT EXISTS idx_spike_events_auto_newsletter ON spike_events(auto_newsletter_id);
CREATE INDEX IF NOT EXISTS idx_spike_events_detected_at ON spike_events(detected_at);
CREATE INDEX IF NOT EXISTS idx_spike_events_processed ON spike_events(processed);
CREATE INDEX IF NOT EXISTS idx_auto_newsletter_analytics_auto_newsletter ON auto_newsletter_analytics(auto_newsletter_id);
CREATE INDEX IF NOT EXISTS idx_auto_newsletter_analytics_generation_time ON auto_newsletter_analytics(generation_time);

-- Enable RLS on new tables
ALTER TABLE trend_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE spike_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE auto_newsletter_analytics ENABLE ROW LEVEL SECURITY;

-- RLS Policies for trend_data (public read access for trend data)
CREATE POLICY "Anyone can read trend data" ON trend_data
    FOR SELECT USING (true);

CREATE POLICY "Service can insert trend data" ON trend_data
    FOR INSERT WITH CHECK (true);

-- RLS Policies for spike_events
CREATE POLICY "Users can view spike events for their auto newsletters" ON spike_events
    FOR SELECT USING (auto_newsletter_id IN (
        SELECT id FROM auto_newsletters WHERE user_id = auth.uid()
    ));

CREATE POLICY "Service can insert spike events" ON spike_events
    FOR INSERT WITH CHECK (true);

-- RLS Policies for auto_newsletter_analytics
CREATE POLICY "Users can view analytics for their auto newsletters" ON auto_newsletter_analytics
    FOR SELECT USING (auto_newsletter_id IN (
        SELECT id FROM auto_newsletters WHERE user_id = auth.uid()
    ));

CREATE POLICY "Service can insert analytics" ON auto_newsletter_analytics
    FOR INSERT WITH CHECK (true);

-- Add updated_at trigger for new tables
CREATE TRIGGER update_trend_data_updated_at BEFORE UPDATE ON trend_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spike_events_updated_at BEFORE UPDATE ON spike_events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_auto_newsletter_analytics_updated_at BEFORE UPDATE ON auto_newsletter_analytics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
