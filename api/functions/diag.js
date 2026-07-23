// TEMPORARY diagnostic endpoint — reports env var presence (never values) to
// debug why _auth.js sees SUPABASE_URL/SUPABASE_ANON_KEY as missing despite
// them being configured in the Vercel dashboard. Delete this file once
// resolved; even boolean/length metadata about secret names is unnecessary
// surface area to leave live long-term.
export const config = { runtime: 'edge' };

export default async function handler(req) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_ANON_KEY;

  return new Response(JSON.stringify({
    hasSupabaseUrl: !!url,
    supabaseUrlLength: url ? url.length : 0,
    hasSupabaseKey: !!key,
    supabaseKeyLength: key ? key.length : 0,
    vercelEnv: process.env.VERCEL_ENV || null,
    vercelUrl: process.env.VERCEL_URL || null,
    vercelGitCommitSha: process.env.VERCEL_GIT_COMMIT_SHA || null,
    vercelGitCommitRef: process.env.VERCEL_GIT_COMMIT_REF || null,
  }), {
    status: 200,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  });
}
