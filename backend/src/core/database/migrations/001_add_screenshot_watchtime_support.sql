-- Migration: Add Screenshot and Watchtime Support
-- Description: Creates tables to store user screenshots and watchtime tracking data
-- Date: 2025-03-25

-- Table: user_screenshots
-- Stores user-captured screenshots with timestamp metadata
CREATE TABLE IF NOT EXISTS public.user_screenshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    video_id TEXT NOT NULL,
    screenshot_url TEXT NOT NULL,
    timestamp_seconds REAL NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Foreign key constraints
    CONSTRAINT fk_user_screenshots_user
        FOREIGN KEY (user_id)
        REFERENCES auth.users(id)
        ON DELETE CASCADE,

    -- Indexes for performance
    CONSTRAINT idx_user_screenshots_user_video
        UNIQUE (user_id, video_id, timestamp_seconds)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_screenshots_user_id
    ON public.user_screenshots(user_id);

CREATE INDEX IF NOT EXISTS idx_user_screenshots_video_id
    ON public.user_screenshots(video_id);

CREATE INDEX IF NOT EXISTS idx_user_screenshots_timestamp
    ON public.user_screenshots(timestamp_seconds);

-- Add RLS (Row Level Security) policies
ALTER TABLE public.user_screenshots ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own screenshots
CREATE POLICY "Users can view their own screenshots"
    ON public.user_screenshots
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can only insert their own screenshots
CREATE POLICY "Users can insert their own screenshots"
    ON public.user_screenshots
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only delete their own screenshots
CREATE POLICY "Users can delete their own screenshots"
    ON public.user_screenshots
    FOR DELETE
    USING (auth.uid() = user_id);

-- Table: user_watchtime
-- Tracks user's video watching progress and engagement
CREATE TABLE IF NOT EXISTS public.user_watchtime (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    video_id TEXT NOT NULL,
    current_position_seconds REAL NOT NULL DEFAULT 0,
    total_watched_seconds REAL NOT NULL DEFAULT 0,
    engagement_score REAL,
    last_watched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Foreign key constraints
    CONSTRAINT fk_user_watchtime_user
        FOREIGN KEY (user_id)
        REFERENCES auth.users(id)
        ON DELETE CASCADE,

    -- Unique constraint: one watchtime record per user per video
    CONSTRAINT unique_user_video_watchtime
        UNIQUE (user_id, video_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_watchtime_user_id
    ON public.user_watchtime(user_id);

CREATE INDEX IF NOT EXISTS idx_user_watchtime_video_id
    ON public.user_watchtime(video_id);

CREATE INDEX IF NOT EXISTS idx_user_watchtime_last_watched
    ON public.user_watchtime(last_watched_at DESC);

-- Add RLS (Row Level Security) policies
ALTER TABLE public.user_watchtime ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own watchtime
CREATE POLICY "Users can view their own watchtime"
    ON public.user_watchtime
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can only insert their own watchtime
CREATE POLICY "Users can insert their own watchtime"
    ON public.user_watchtime
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only update their own watchtime
CREATE POLICY "Users can update their own watchtime"
    ON public.user_watchtime
    FOR UPDATE
    USING (auth.uid() = user_id);

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_watchtime_updated_at
    BEFORE UPDATE ON public.user_watchtime
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Optional: Add engagement score calculation function
-- This can be called to calculate engagement based on watch patterns
CREATE OR REPLACE FUNCTION calculate_engagement_score(
    p_total_watched REAL,
    p_video_duration REAL DEFAULT NULL
)
RETURNS REAL AS $$
DECLARE
    engagement_score REAL;
BEGIN
    -- Simple engagement calculation: watched time / video duration
    -- Returns value between 0 and 1
    IF p_video_duration IS NOT NULL AND p_video_duration > 0 THEN
        engagement_score := LEAST(p_total_watched / p_video_duration, 1.0);
    ELSE
        -- If duration unknown, just return normalized watch time
        engagement_score := LEAST(p_total_watched / 600.0, 1.0); -- Normalize to 10 min
    END IF;

    RETURN engagement_score;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions (adjust based on your auth setup)
-- GRANT ALL ON public.user_screenshots TO authenticated;
-- GRANT ALL ON public.user_watchtime TO authenticated;

-- Comments for documentation
COMMENT ON TABLE public.user_screenshots IS 'Stores user-captured screenshots with timestamp metadata for video analysis';
COMMENT ON TABLE public.user_watchtime IS 'Tracks user video watching progress and engagement metrics';
COMMENT ON COLUMN public.user_screenshots.timestamp_seconds IS 'Video timestamp when screenshot was captured';
COMMENT ON COLUMN public.user_watchtime.current_position_seconds IS 'Current playback position in seconds';
COMMENT ON COLUMN public.user_watchtime.total_watched_seconds IS 'Total time user has watched this video';
COMMENT ON COLUMN public.user_watchtime.engagement_score IS 'Engagement metric (0-1) based on watch patterns';
