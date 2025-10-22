-- Migration: Add full_email_html field to drafts table
-- Run this SQL in your Supabase SQL Editor

-- Add the new column
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS full_email_html TEXT;

-- Update existing drafts to have the full_email_html field
-- For existing drafts, we'll set full_email_html to the same as generated_html
UPDATE drafts 
SET full_email_html = generated_html 
WHERE full_email_html IS NULL;

-- Add a comment to explain the field
COMMENT ON COLUMN drafts.full_email_html IS 'Full email template HTML for sending newsletters';
COMMENT ON COLUMN drafts.generated_html IS 'Editable content HTML for the editor interface';


