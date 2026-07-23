# Cloud Sync Deployment Guide

Your dashboard now has cloud sync! Tasks sync across Mac, Windows, and any browser. Here's how to set it up.

## What you need

- A Vercel account (free): https://vercel.com
- A Supabase account (free): https://supabase.com

**Time: ~5 minutes.**

---

## Step 1: Set up Supabase (database)

1. **Create Supabase account** at https://supabase.com (sign up with GitHub for fastest)
2. **Create a new project**: name it `josh-dashboard`, choose a region close to you
3. **Wait for project to initialize** (~1 min)
4. **Run the database schema** in the SQL Editor:
   - Go to **SQL Editor** in the left sidebar
   - Click **New Query**
   - Paste this entire SQL block:

```sql
-- Users table
create table public.users (
  id uuid primary key default gen_random_uuid(),
  api_key text unique not null,
  created_at timestamp default now()
);

-- Tasks table (daily goals)
create table public.tasks (
  id text primary key,
  user_id uuid references public.users(id) on delete cascade,
  date text not null,
  text text not null,
  done boolean default false,
  domain text,
  queued boolean default false,
  done_at bigint,
  seed_h text,
  created_at timestamp default now(),
  updated_at timestamp default now()
);

-- Backlogs table
create table public.backlogs (
  id text primary key,
  user_id uuid references public.users(id) on delete cascade,
  domain_id text not null,
  text text not null,
  added_at text,
  due text,
  seed_h text,
  created_at timestamp default now()
);

-- Settings table
create table public.settings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid unique references public.users(id) on delete cascade,
  config jsonb not null,
  updated_at timestamp default now()
);

-- History table
create table public.history (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  date text not null,
  total_goals int,
  done_goals int,
  by_domain jsonb,
  streak_after int,
  created_at timestamp default now(),
  unique(user_id, date)
);

-- Indexes
create index idx_tasks_user_date on tasks(user_id, date);
create index idx_tasks_user_updated on tasks(user_id, updated_at);
create index idx_backlogs_user on backlogs(user_id);
create index idx_history_user_date on history(user_id, date);

-- Enable RLS (Row Level Security)
alter table public.users enable row level security;
alter table public.tasks enable row level security;
alter table public.backlogs enable row level security;
alter table public.settings enable row level security;
alter table public.history enable row level security;
```

5. **Click "Run"** and verify it succeeds (should see "Successfully executed")
6. **Get your credentials**:
   - Click **Settings** (bottom left)
   - Click **API** in the left menu
   - Copy your **Project URL** (looks like `https://xyz.supabase.co`)
   - Copy your **anon key** (under "Your API keys")
   - Keep these handy!

---

## Step 1.5: Push code to GitHub (if needed)

**Already done?** Skip this section. Your code is at https://github.com/claudelarp/josh-dashboard

**Not pushed yet?** Here's how:

1. **Set up Git credentials** (one-time):
   ```bash
   git config --global credential.helper osxkeychain
   ```
   (On Windows, use: `git config --global credential.helper wincred`)

2. **Create a GitHub Personal Access Token**:
   - Go to: https://github.com/settings/tokens/new
   - Name: `josh-dashboard`
   - Scopes: check only `repo` (all options under it)
   - Click **Generate token** and copy it

3. **Push your code**:
   ```bash
   cd "/Users/joshuanieman/Desktop/Josh Brain"
   git push -u origin main
   # When prompted:
   #   Username: your-github-username
   #   Password: (paste your Personal Access Token)
   ```
   Git saves your credentials for next time.

**Error: "Repository not found"?**
- Make sure your token is for the correct GitHub account
- Verify the repo exists at: https://github.com/YOUR_USERNAME/josh-dashboard

---

## Step 2: Deploy to Vercel

1. **Sign up for Vercel** at https://vercel.com (connect your GitHub account `claudelarp`)

2. **Code is ready at GitHub**: https://github.com/claudelarp/josh-dashboard

3. **Import into Vercel**:
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select `josh-dashboard` from the list (it should appear automatically)
   - Click "Import"

4. **Add environment variables** in Vercel:
   - You'll see an "Environment Variables" section
   - Add these two:
     - **Name:** `SUPABASE_URL` → **Value:** (paste the Project URL from Supabase)
     - **Name:** `SUPABASE_ANON_KEY` → **Value:** (paste the anon key from Supabase)
   - Click **Deploy**

5. **Wait for deployment** (~2 min)
6. **You'll get a URL** that looks like `https://josh-dashboard.vercel.app`
   - **Save this URL** — you'll use it in the next step

---

## Step 3: Connect your dashboard

1. **Open** `/Users/joshuanieman/Desktop/Josh Brain/dashboard.html` in your browser
2. **A sync prompt will appear** asking for your API key
3. **Click "Get one here"** or go to: `https://josh-dashboard.vercel.app/setup`
4. **Click "Generate API Key"** on that page
5. **Copy the key** (it starts with `sk_`)
6. **Paste it into the dashboard sync prompt**
7. **Done!** Your dashboard is now synced to the cloud

---

## How it works

- **localStorage-first:** Your dashboard works offline. Tasks are saved locally.
- **Automatic sync:** Every 30 seconds, your changes push to Vercel's database.
- **Cross-device:** Open the dashboard on your Mac or Windows computer, and it pulls the latest tasks.
- **Conflict resolution:** Server data wins if you edit on two devices simultaneously (unlikely).

---

## Testing

- **On Mac:** Add a task, then open the dashboard on Windows — it should appear within 30 seconds.
- **Offline:** Disconnect your internet and add a task. It queues locally. Reconnect, and it syncs.
- **Settings sync:** Change your theme in Settings. It syncs to all devices.

---

## Troubleshooting

**"Connection failed" message:**
- Check your Supabase API credentials are correct in Vercel
- Make sure the Vercel deployment is live (check: https://josh-dashboard.vercel.app/setup)

**API key not working:**
- Copy it exactly (no spaces at the start/end)
- Go back to `/setup` and generate a new one

**Tasks not syncing:**
- Check your internet is connected
- Open browser DevTools (F12 → Console) and look for errors
- Refresh the page

**Need help?**
- Open DevTools (F12) and check the Console for error messages
- Paste the full error here and we can debug it

---

## Next steps

Your dashboard now syncs across all your devices! You can:

1. **On your Mac:** `python3 scripts/build-dashboard.py` to push tasks from your task list into the seed
2. **On both machines:** Access the same dashboard URL and all changes sync automatically
3. **Backups:** Use the Settings → Export JSON to backup your data anytime

Enjoy your cloud-synced dashboard! 🚀
