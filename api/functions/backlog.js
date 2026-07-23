import { supabase, authenticateRequest, apiResponse } from './_auth.js';

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return apiResponse({}, 200);

  const auth = await authenticateRequest(req);
  if (auth.error) return apiResponse(auth, auth.status);
  const userId = auth.userId;

  // GET /api/functions/backlog
  if (req.method === 'GET') {
    const { data, error } = await supabase
      .from('backlogs')
      .select('*')
      .eq('user_id', userId)
      .order('created_at');

    if (error) return apiResponse({ error: error.message }, 500);
    const grouped = {};
    for (const item of data) {
      const domainId = item.domain_id || '_none';
      grouped[domainId] = grouped[domainId] || [];
      grouped[domainId].push({
        id: item.id,
        text: item.text,
        addedAt: item.added_at,
        due: item.due,
        seedH: item.seed_h
      });
    }
    return apiResponse({ backlog: grouped });
  }

  // POST /api/functions/backlog — add/update items
  if (req.method === 'POST') {
    const { backlog } = await req.json(); // { domainId: [{id, text, addedAt, ...}] }
    if (!backlog) return apiResponse({ error: 'backlog required' }, 400);

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

    const { data, error } = await supabase
      .from('backlogs')
      .upsert(items, { onConflict: 'id' })
      .select();

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ backlog: data });
  }

  // DELETE /api/functions/backlog?id=...
  if (req.method === 'DELETE') {
    const url = new URL(req.url);
    const id = url.searchParams.get('id');
    if (!id) return apiResponse({ error: 'id required' }, 400);

    const { error } = await supabase
      .from('backlogs')
      .delete()
      .eq('id', id)
      .eq('user_id', userId);

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ deleted: true });
  }

  return apiResponse({ error: 'Method not allowed' }, 405);
}
