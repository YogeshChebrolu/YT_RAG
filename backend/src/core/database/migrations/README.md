# Database Migrations for Screenshot & Watchtime Support

## Overview

This migration adds complete support for:
- **User Screenshots**: Storing screenshots captured by users with timestamp metadata
- **Watchtime Tracking**: Recording user viewing progress and engagement metrics

## Migration Files

1. `001_add_screenshot_watchtime_support.sql` - Creates tables and policies for screenshot and watchtime features

## How to Apply Migrations

### Option 1: Supabase Dashboard (Recommended)

1. Log in to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy the contents of `001_add_screenshot_watchtime_support.sql`
4. Paste into the SQL editor
5. Click **Run** to execute the migration

### Option 2: Supabase CLI

```bash
# Navigate to project root
cd YT_RAG

# Run migration using Supabase CLI
supabase db push
```

### Option 3: Python Script

```python
from core.database.supabase_client import get_supabase_client

supabase = get_supabase_client()

# Read migration file
with open('migrations/001_add_screenshot_watchtime_support.sql', 'r') as f:
    migration_sql = f.read()

# Execute migration
supabase.rpc('exec', {'sql': migration_sql})
```

## Database Schema

### Table: `user_screenshots`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to auth.users |
| `video_id` | TEXT | YouTube video ID |
| `screenshot_url` | TEXT | Supabase storage URL |
| `timestamp_seconds` | REAL | Video timestamp when captured |
| `description` | TEXT | Optional description |
| `created_at` | TIMESTAMPTZ | Creation timestamp |

**Indexes:**
- `idx_user_screenshots_user_id` - Fast lookup by user
- `idx_user_screenshots_video_id` - Fast lookup by video
- `idx_user_screenshots_timestamp` - Fast lookup by timestamp

**RLS Policies:**
- Users can only view, insert, and delete their own screenshots

### Table: `user_watchtime`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to auth.users |
| `video_id` | TEXT | YouTube video ID |
| `current_position_seconds` | REAL | Current playback position |
| `total_watched_seconds` | REAL | Total time watched |
| `engagement_score` | REAL | Engagement metric (0-1) |
| `last_watched_at` | TIMESTAMPTZ | Last watch timestamp |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Auto-updated timestamp |

**Indexes:**
- `idx_user_watchtime_user_id` - Fast lookup by user
- `idx_user_watchtime_video_id` - Fast lookup by video
- `idx_user_watchtime_last_watched` - Fast lookup by recent activity

**RLS Policies:**
- Users can only view, insert, and update their own watchtime data

**Unique Constraint:**
- One watchtime record per user per video

## Storage Bucket Configuration

Make sure you have a Supabase storage bucket named `video-frames`:

1. Go to **Storage** in Supabase dashboard
2. Create bucket `video-frames` (if it doesn't exist)
3. Set bucket to **Public** or configure RLS policies
4. User screenshots will be stored at: `user_screenshots/{user_id}/{video_id}/{screenshot_id}.jpg`

## Verification

After running the migration, verify with:

```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('user_screenshots', 'user_watchtime');

-- Check RLS policies
SELECT tablename, policyname, cmd FROM pg_policies
WHERE schemaname = 'public'
AND tablename IN ('user_screenshots', 'user_watchtime');

-- Test insert (replace with actual user_id)
INSERT INTO user_watchtime (user_id, video_id, current_position_seconds)
VALUES ('your-user-uuid', 'dQw4w9WgXcQ', 125.5);
```

## Rollback

To rollback this migration:

```sql
-- Drop tables (cascade will remove policies and triggers)
DROP TABLE IF EXISTS public.user_screenshots CASCADE;
DROP TABLE IF EXISTS public.user_watchtime CASCADE;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
DROP FUNCTION IF EXISTS calculate_engagement_score CASCADE;
```

## Next Steps

After applying the migration:

1. ✅ Database schema is ready
2. ✅ Backend API endpoints are implemented
3. 🔧 Update frontend to send screenshot + watchtime data
4. 🔧 Test end-to-end flow

See [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md) for frontend integration instructions.
