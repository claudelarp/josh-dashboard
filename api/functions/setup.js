export const config = { runtime: 'edge' };

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
      }
    });
  }

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard Setup - Cloud Sync</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #050506;
      color: #FAFAFA;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .container {
      max-width: 500px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 16px;
      padding: 40px;
      backdrop-filter: blur(24px);
    }
    h1 {
      font-size: 24px;
      margin-bottom: 12px;
      background: linear-gradient(180deg, #FFFFFF 0%, #C7C4BC 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    p {
      color: #B8B6B0;
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 20px;
    }
    .status {
      padding: 12px;
      border-radius: 9px;
      font-size: 13px;
      margin-bottom: 16px;
      text-align: center;
    }
    .status.loading {
      background: rgba(100, 200, 255, 0.1);
      color: #6BE3A4;
    }
    .status.success {
      background: rgba(107, 227, 164, 0.1);
      color: #6BE3A4;
    }
    .status.error {
      background: rgba(255, 107, 107, 0.1);
      color: #FF6B6B;
    }
    .api-key {
      background: rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 9px;
      padding: 12px;
      font-family: ui-monospace, "SF Mono", monospace;
      font-size: 12px;
      word-break: break-all;
      margin: 16px 0;
      user-select: all;
    }
    button {
      background: linear-gradient(180deg, #FFFFFF 0%, #E8E5DD 100%);
      color: #0A0A0B;
      font-weight: 700;
      font-size: 13px;
      padding: 11px 20px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      width: 100%;
      transition: all 0.15s;
    }
    button:hover {
      filter: brightness(1.05);
      transform: translateY(-1px);
    }
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .note {
      font-size: 11px;
      color: #76746E;
      margin-top: 12px;
      line-height: 1.5;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Cloud Sync Setup</h1>
    <p>Generate an API key to sync your dashboard across devices.</p>

    <div id="status" class="status" style="display:none;"></div>
    <button id="generateBtn" onclick="generateKey()">Generate API Key</button>

    <div id="keyContainer" style="display:none;">
      <p style="margin-top: 16px; margin-bottom: 8px;">Your API Key:</p>
      <div class="api-key" id="keyDisplay"></div>
      <button onclick="copyKey()" style="background: rgba(255,255,255,0.08); color: #FAFAFA; margin-bottom: 12px;">Copy Key</button>
      <p style="font-size: 12px; color: #B8B6B0;">
        1. Copy your API key above<br>
        2. Go back to your dashboard<br>
        3. Paste it in the sync prompt<br>
        4. Your tasks now sync across all devices!
      </p>
    </div>

    <div class="note">
      <strong>Keep your API key private.</strong> Anyone with this key can access your tasks.
    </div>
  </div>

  <script>
    // Relative path on purpose: this page and the API always share an
    // origin (whichever domain the visitor actually used to load /setup —
    // stable alias, per-deployment hash URL, or a future custom domain).
    // Building an absolute URL from process.env.VERCEL_URL previously
    // pointed at a *different* hostname (the per-deployment hash, not the
    // one the browser was on), which fails as a cross-origin "Failed to
    // fetch" the moment that specific deployment hash isn't the current one.
    let generatedKey = '';

    async function generateKey() {
      const btn = document.getElementById('generateBtn');
      const status = document.getElementById('status');

      btn.disabled = true;
      status.className = 'status loading';
      status.textContent = 'Generating...';
      status.style.display = 'block';

      try {
        const res = await fetch('/api/functions/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: 'user@dashboard.local' })
        });

        if (!res.ok) throw new Error('Failed to generate key');

        const data = await res.json();
        generatedKey = data.apiKey;

        status.className = 'status success';
        status.textContent = data.isNew ? 'Key generated! Copy it below.' : 'Key retrieved.';

        document.getElementById('keyDisplay').textContent = generatedKey;
        document.getElementById('keyContainer').style.display = 'block';
        btn.style.display = 'none';
      } catch (err) {
        status.className = 'status error';
        status.textContent = 'Error: ' + err.message;
        btn.disabled = false;
      }
    }

    function copyKey() {
      navigator.clipboard.writeText(generatedKey);
      alert('API key copied! Go back to your dashboard and paste it in the sync prompt.');
    }
  </script>
</body>
</html>`;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html',
      'Access-Control-Allow-Origin': '*'
    }
  });
}
