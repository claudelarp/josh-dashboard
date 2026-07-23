import { supabase, apiResponse } from './_auth.js';
import crypto from 'crypto';

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return apiResponse({}, 200);

  // POST /api/functions/register — generate API key
  if (req.method === 'POST') {
    const { email } = await req.json();
    if (!email) return apiResponse({ error: 'email required' }, 400);

    try {
      // Generate a secure API key
      const apiKey = 'sk_' + crypto.randomBytes(32).toString('hex');

      // Insert user
      const { data, error } = await supabase
        .from('users')
        .insert([{ api_key: apiKey }])
        .select('id');

      if (error) {
        // If user exists, get their API key
        if (error.code === '23505') {
          const { data: existing } = await supabase
            .from('users')
            .select('api_key')
            .eq('api_key', apiKey)
            .single();
          if (existing) {
            return apiResponse({ apiKey: existing.api_key, isNew: false });
          }
        }
        return apiResponse({ error: error.message }, 500);
      }

      return apiResponse({ apiKey, userId: data[0].id, isNew: true });
    } catch (error) {
      return apiResponse({ error: error.message }, 500);
    }
  }

  return apiResponse({ error: 'Method not allowed' }, 405);
}
