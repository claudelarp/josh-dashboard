import { supabase, authenticateRequest, apiResponse } from './_auth.js';

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return apiResponse({}, 200);

  const auth = await authenticateRequest(req);
  if (auth.error) return apiResponse(auth, auth.status);
  const userId = auth.userId;

  // GET /api/functions/settings
  if (req.method === 'GET') {
    const { data, error } = await supabase
      .from('settings')
      .select('config')
      .eq('user_id', userId)
      .single();

    if (error && error.code !== 'PGRST116') {
      return apiResponse({ error: error.message }, 500);
    }
    return apiResponse({ settings: data?.config || null });
  }

  // POST /api/functions/settings — save config
  if (req.method === 'POST') {
    const { config } = await req.json();
    if (!config) return apiResponse({ error: 'config required' }, 400);

    const { data, error } = await supabase
      .from('settings')
      .upsert(
        { user_id: userId, config, updated_at: new Date().toISOString() },
        { onConflict: 'user_id' }
      )
      .select('config')
      .single();

    if (error) return apiResponse({ error: error.message }, 500);
    return apiResponse({ settings: data.config });
  }

  return apiResponse({ error: 'Method not allowed' }, 405);
}
