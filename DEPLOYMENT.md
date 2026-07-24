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
```

**Do not enable Row Level Security on these tables.** Access control here happens in the API layer (`api/functions/_auth.js` checks the caller's API key before touching any table), not per-row Postgres policies — all requests use the same shared `anon` key from the serverless functions, never a per-user Supabase Auth session. RLS with no policies defined blocks 100% of access (that's Postgres's default-deny behavior), which would make every API call fail. If you already ran an earlier version of this schema that included `enable row level security` statements, undo it:

```sql
alter table public.users disable row level security;
alter table public.tasks disable row level security;
alter table public.backlogs disable row level security;
alter table public.settings disable row level security;
alter table public.history disable row level security;
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

**Not pushed yet, or setting this up on a new machine?** Use the GitHub CLI (`gh`) — it stores your credentials in the macOS keychain and never requires typing or pasting a raw token into a command, a URL, or anywhere that could end up in a screenshot or terminal scrollback.

1. **Install the GitHub CLI** (one-time):
   ```bash
   brew install gh
   ```
   (Windows: `winget install --id GitHub.cli`, or see https://cli.github.com)

2. **Log in** (opens a browser to authorize — no token ever touches your terminal):
   ```bash
   gh auth login --hostname github.com --git-protocol https --web
   ```
   It prints a one-time code and a URL (`github.com/login/device`) — open the URL, enter the code, click Authorize. If the CLI process itself hangs or times out mid-poll (a known flaky spot on some networks — the browser step can succeed while the CLI's polling connection stalls), just re-run the same command for a fresh code; it doesn't affect the code that's already been used.

3. **Wire git to use it** (one-time):
   ```bash
   gh auth setup-git
   ```
   From now on, `git push`/`pull` against GitHub authenticate silently through `gh` — no prompts, no pasted credentials.

4. **Push your code**:
   ```bash
   cd "/Users/joshuanieman/Desktop/Josh Brain"
   git push -u origin main
   ```

**Verify it's actually working:** `git push --dry-run origin main` should complete with no username/password prompt at all.

**If you ever do end up with a token in a git remote URL** (e.g. `https://user:TOKEN@github.com/...`) — that's stored in plaintext in `.git/config` on disk, not just at risk in a terminal screenshot. Clean it up with `git remote set-url origin https://github.com/YOUR_USERNAME/josh-dashboard.git`, then revoke that token at https://github.com/settings/tokens.

**Error: "Repository not found"?**
- Make sure you're logged into `gh` as the correct GitHub account: `gh auth status`
- Verify the repo exists at: https://github.com/YOUR_USERNAME/josh-dashboard

---

## Step 2: Deploy to Vercel

This project is a **static file + serverless functions** deployment — there's no build step. `dashboard.html` is served directly and everything under `api/functions/` becomes a serverless endpoint automatically. `vercel.json` sets `"framework": null` so Vercel doesn't try to guess a framework or look for a build output directory.

1. **Sign up for Vercel** at https://vercel.com (connect your GitHub account `claudelarp`)

2. **Code is ready at GitHub**: https://github.com/claudelarp/josh-dashboard

3. **If you previously tried importing this project and hit the "No Output Directory named public" error**, delete that project first (Project → Settings → scroll to bottom → Delete Project). That error came from a leftover `build` script in `package.json`, now removed — but Vercel caches settings from the first import, so a stale project needs to be deleted and re-imported fresh, not just redeployed.

4. **Import into Vercel**:
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select `josh-dashboard` from the list
   - Click "Import"
   - **Leave Build & Output Settings on "Auto" / default** — do not manually type anything into "Output Directory." It should show empty/auto since `framework: null` is set.

5. **Deploy without env vars first** to confirm the deploy itself succeeds:
   - Click **Deploy** (skip the Environment Variables section for now)
   - Wait ~30–60 seconds
   - It should say **"Ready"** with a green checkmark. If it still fails with the public-directory error, see Troubleshooting below.

6. **Add environment variables** once the base deploy succeeds:
   - Go to your project → **Settings** → **Environment Variables**
   - Add:
     - **Name:** `SUPABASE_URL` → **Value:** (paste the Project URL from Supabase)
     - **Name:** `SUPABASE_ANON_KEY` → **Value:** (paste the anon key from Supabase)
   - Go to **Deployments** → click the "..." on the latest deployment → **Redeploy**

7. **You'll get a URL** — this project's live URL is `https://josh-dashboard-six.vercel.app`
   - **Note:** the URL shown right after import (something like `josh-dashboard-<hash>-belated.vercel.app`) is a per-deployment URL that changes every time you redeploy. Use the **stable** one instead — find it under the project's **Domains** tab (no random hash in it). `dashboard.html` already has `https://josh-dashboard-six.vercel.app` hardcoded as the sync default, so unless yours differs, no code changes are needed.

---

## Step 2.5: Turn off Deployment Protection (required for sync to work)

Vercel Team projects (this one lives under the `belated` team) often ship with **Deployment Protection** on by default — an SSO login wall in front of every URL, including API routes. If it's on, every sync request from the dashboard silently fails with `401 Protected deployment`, and visiting the site in a browser redirects to a Vercel login page instead of showing the dashboard.

1. Go to the project in Vercel → **Settings** → **Deployment Protection**
2. Under **Vercel Authentication**, set it to **"Only Preview Deployments"** (or **"Disabled"**) so Production is public
3. Save — takes effect immediately, no redeploy needed
4. Verify: visiting `https://josh-dashboard-six.vercel.app/` in an incognito/private window (not logged into Vercel) should show the dashboard directly, not a login redirect

---

## Step 3: Connect your dashboard

1. **Open** `/Users/joshuanieman/Desktop/Josh Brain/dashboard.html` in your browser
2. **A sync prompt will appear** asking for your API key
3. **Click "Get one here"** or go to: `https://josh-dashboard-six.vercel.app/setup`
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

**"No Output Directory named 'public' found" error:**
This means Vercel thinks it needs to run a build and find output somewhere. Root cause was a stray `build` script in `package.json` (fixed — this repo now has none). If you still see this after pulling the latest code:
1. Check **Project Settings → Build & Development Settings** in Vercel — if "Output Directory" has anything manually typed in (like `public`), clear it back to the default/auto placeholder.
2. Check "Build Command" the same way — it should be empty/auto, not a custom command.
3. If unsure, delete the project entirely and re-import — manual dashboard overrides don't carry over to a fresh import, so this guarantees a clean slate.

**"Protected deployment" / 401 error, or the page redirects to a Vercel login screen:**
- This is **Deployment Protection**, not a code bug — see Step 2.5 above. Team projects can have an SSO wall on by default that blocks browser visits and all API calls alike. Disable "Vercel Authentication" for Production in Settings → Deployment Protection.

**"A server error has occurred / FUNCTION_INVOCATION_FAILED" (blank, no JSON body) on any `/api/functions/*` call:**
This is Vercel's generic crash page — it means the function crashed before it could return a normal response, usually at import/module-eval time, before our own error handling ever runs. Two known causes, both fixed in the code as of the `_auth.js` rewrite (which now fails with a clear JSON error instead of crashing), so if you're on the latest code and still see the raw crash page:
1. **Missing/misnamed env vars.** In Vercel → Settings → Environment Variables, confirm both `SUPABASE_URL` and `SUPABASE_ANON_KEY` exist, are spelled exactly like that (case-sensitive), and have the **Production** checkbox ticked (not just Preview/Development). Adding a var doesn't retroactively apply to old deployments — redeploy after adding.
2. **RLS enabled with no policies** (see Step 1's note above) — this blocks every table operation. Run the `disable row level security` statements if you ran an earlier version of the schema.
- Once `_auth.js`'s guard is in place, the same broken config shows up as a clean `{"error": "Server misconfigured: SUPABASE_URL/SUPABASE_ANON_KEY are not set..."}` JSON response instead of the opaque crash page — much faster to diagnose from here on.

**"Connection failed" message:**
- Check your Supabase API credentials are correct in Vercel
- Make sure the Vercel deployment is live (check: https://josh-dashboard-six.vercel.app/setup)
- Confirm Deployment Protection is off (see above) — a protection wall looks like a connection failure from the dashboard's point of view

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
