import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

// Don't call createClient() unconditionally at module scope: with missing/
// undefined args it throws synchronously, which crashes every function that
// imports this file with an opaque "FUNCTION_INVOCATION_FAILED" and no way
// to see why. Defer to a clear, catchable error instead.
export const supabase = (supabaseUrl && supabaseKey) ? createClient(supabaseUrl, supabaseKey) : null;

export async function authenticateRequest(req) {
  if (!supabase) {
    return { error: 'Server misconfigured: SUPABASE_URL/SUPABASE_ANON_KEY are not set on this deployment', status: 500 };
  }
  const token = req.headers.get('authorization')?.replace('Bearer ', '');
  if (!token) return { error: 'Unauthorized', status: 401 };

  try {
    const { data: user, error } = await supabase
      .from('users')
      .select('id')
      .eq('api_key', token)
      .single();

    if (error || !user) return { error: 'Invalid token', status: 401 };
    return { userId: user.id };
  } catch (err) {
    return { error: 'Auth check failed: ' + err.message, status: 500 };
  }
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
