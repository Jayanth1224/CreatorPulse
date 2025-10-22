-- Migration: Add voice training functionality
-- This migration adds support for user voice training samples

-- Create voice samples table
CREATE TABLE IF NOT EXISTS user_voice_samples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for efficient user queries
CREATE INDEX IF NOT EXISTS idx_user_voice_samples_user_id ON user_voice_samples(user_id);

-- Create index for created_at for ordering
CREATE INDEX IF NOT EXISTS idx_user_voice_samples_created_at ON user_voice_samples(created_at DESC);

-- Add RLS (Row Level Security) policy
ALTER TABLE user_voice_samples ENABLE ROW LEVEL SECURITY;

-- Create policy for users to only access their own voice samples
CREATE POLICY "Users can manage their own voice samples" ON user_voice_samples
    FOR ALL USING (auth.uid() = user_id);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_voice_samples_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_voice_samples_updated_at
    BEFORE UPDATE ON user_voice_samples
    FOR EACH ROW
    EXECUTE FUNCTION update_voice_samples_updated_at();

-- Add comment for documentation
COMMENT ON TABLE user_voice_samples IS 'Stores user writing samples for voice training via in-context learning';
COMMENT ON COLUMN user_voice_samples.title IS 'Title or identifier for the writing sample';
COMMENT ON COLUMN user_voice_samples.content IS 'The actual writing content used for voice training';
