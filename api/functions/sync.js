import { supabase, authenticateRequest, apiResponse } from './auth.js';

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return apiResponse({}, 200);

  const auth = await authenticateRequest(req);
  if (auth.error) return apiResponse(auth, auth.status);
  const userId = auth.userId;

  // GET /api/functions/sync?date=2026-07-23 — pull all data for a date
  if (req.method === 'GET') {
    const url = new URL(req.url);
    const date = url.searchParams.get('date');
    if (!date) return apiResponse({ error: 'date required' }, 400);

    const [tasksRes, backlogRes, settingsRes, historyRes] = await Promise.all([
      supabase.from('tasks').select('*').eq('user_id', userId).eq('date', date),
      supabase.from('backlogs').select('*').eq('user_id', userId),
      supabase.from('settings').select('config').eq('user_id', userId).single(),
      supabase.from('history').select('*').eq('user_id', userId).eq('date', date).single()
    ]);

    // Normalize tasks
    const tasks = (tasksRes.data || []).map(t => ({
      id: t.id,
      text: t.text,
      done: t.done,
      doneAt: t.done_at,
      domain: t.domain,
      queued: t.queued,
      seedH: t.seed_h
    }));

    // Normalize backlog
    const backlog = {};
    for (const item of backlogRes.data || []) {
      const domainId = item.domain_id || '_none';
      backlog[domainId] = backlog[domainId] || [];
      backlog[domainId].push({
        id: item.id,
        text: item.text,
        addedAt: item.added_at,
        due: item.due,
        seedH: item.seed_h
      });
    }

    return apiResponse({
      date,
      tasks,
      backlog,
      settings: settingsRes.data?.config || null,
      history: historyRes.data || null,
      serverTime: new Date().toISOString()
    });
  }

  // POST /api/functions/sync — push all changes at once
  if (req.method === 'POST') {
    const { date, tasks, backlog, settings, history } = await req.json();
    if (!date) return apiResponse({ error: 'date required' }, 400);

    try {
      // Upsert tasks
      if (tasks && Array.isArray(tasks)) {
        const now = new Date().toISOString();
        const toInsert = tasks.map(t => ({
          id: t.id,
          user_id: userId,
          date,
          text: t.text,
          done: t.done || false,
          domain: t.domain || null,
          queued: t.queued || false,
          done_at: t.doneAt || null,
          seed_h: t.seedH || null,
          updated_at: now
        }));
        await supabase.from('tasks').upsert(toInsert, { onConflict: 'id' });
      }

      // Upsert backlog
      if (backlog && typeof backlog === 'object') {
        const items = [];
        for (const [domainId, list] of Object.entries(backlog)) {
          for (const item of list) {
            items.push({
              id: item.id,
              user_id: userId,
              domain_id: domainId === '_none' ? null : domainId,
              text: item.text,
              added_at: item.addedAt,
              due: item.due || null,
              seed_h: item.seedH || null
            });
          }
        }
        if (items.length > 0) {
          await supabase.from('backlogs').upsert(items, { onConflict: 'id' });
        }
      }

      // Upsert settings
      if (settings) {
        await supabase.from('settings').upsert(
          { user_id: userId, config: settings, updated_at: new Date().toISOString() },
          { onConflict: 'user_id' }
        );
      }

      // Upsert history
      if (history) {
        await supabase.from('history').upsert(
          {
            user_id: userId,
            date,
            total_goals: history.t,
            done_goals: history.d,
            by_domain: history.byDomain,
            streak_after: history.streakAfter
          },
          { onConflict: 'user_id, date' }
        );
      }

      return apiResponse({ synced: true, serverTime: new Date().toISOString() });
    } catch (error) {
      return apiResponse({ error: error.message }, 500);
    }
  }

  return apiResponse({ error: 'Method not allowed' }, 405);
}
