import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);

export async function authenticateRequest(req) {
  const token = req.headers.get('authorization')?.replace('Bearer ', '');
  if (!token) return { error: 'Unauthorized', status: 401 };

  const { data: user, error } = await supabase
    .from('users')
    .select('id')
    .eq('api_key', token)
    .single();

  if (error || !user) return { error: 'Invalid token', status: 401 };
  return { userId: user.id };
}

export function apiResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  });
}

export function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  };
}
