import { supabase, authenticateRequest, apiResponse, corsHeaders } from './auth.js';

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    return apiResponse({}, 200);
  }

  const auth = await authenticateRequest(req);
  if (auth.error) return apiResponse(auth, auth.status);
  const userId = auth.userId;

  // GET /api/functions/tasks?date=2026-07-23
  if (req.method === 'GET') {
    const url = new URL(req.url);
    const date = url.searchParams.get('date');

    if (!date) {
      return apiResponse({ error: 'date parameter required' }, 400);
    }

    const { data, error } = await supabase
      .from('tasks')
      .select('*')
      .eq('user_id', userId)
      .eq('date', date)
      .order('created_at');

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ tasks: data });
  }

  // POST /api/functions/tasks — create/update multiple
  if (req.method === 'POST') {
    const { tasks } = await req.json();
    if (!Array.isArray(tasks)) {
      return apiResponse({ error: 'tasks must be an array' }, 400);
    }

    const now = new Date().toISOString();
    const toInsert = tasks.map(t => ({
      id: t.id,
      user_id: userId,
      date: t.date,
      text: t.text,
      done: t.done || false,
      domain: t.domain || null,
      queued: t.queued || false,
      done_at: t.doneAt || null,
      seed_h: t.seedH || null,
      updated_at: now
    }));

    // Upsert: insert if new, update if exists
    const { data, error } = await supabase
      .from('tasks')
      .upsert(toInsert, { onConflict: 'id' })
      .select();

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ tasks: data });
  }

  // DELETE /api/functions/tasks — delete by id
  if (req.method === 'DELETE') {
    const { id } = await req.json();
    if (!id) return apiResponse({ error: 'id required' }, 400);

    const { error } = await supabase
      .from('tasks')
      .delete()
      .eq('id', id)
      .eq('user_id', userId);

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ deleted: true });
  }

  return apiResponse({ error: 'Method not allowed' }, 405);
}
