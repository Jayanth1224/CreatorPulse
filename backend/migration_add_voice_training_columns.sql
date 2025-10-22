-- Add missing voice training columns to drafts table
-- This migration adds the columns that are referenced in the draft generation code

ALTER TABLE drafts 
ADD COLUMN IF NOT EXISTS voice_training_used BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS voice_samples_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS generation_metadata JSONB DEFAULT NULL;

-- Add index for better performance on voice training queries
CREATE INDEX IF NOT EXISTS idx_drafts_voice_training_used ON drafts(voice_training_used);
CREATE INDEX IF NOT EXISTS idx_drafts_voice_samples_count ON drafts(voice_samples_count);

-- Update existing drafts to have default values
UPDATE drafts 
SET 
    voice_training_used = FALSE,
    voice_samples_count = 0,
    generation_metadata = NULL
WHERE voice_training_used IS NULL;
