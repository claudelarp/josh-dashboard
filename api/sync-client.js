/**
 * Cloud sync client for the dashboard.
 * Syncs localStorage ↔ Vercel API in the background.
 * Works offline, merges changes when reconnected.
 */

class SyncClient {
  constructor(apiUrl, apiKey) {
    this.apiUrl = apiUrl;
    this.apiKey = apiKey;
    this.online = navigator.onLine;
    this.syncing = false;
    this.queue = [];
    this.lastSync = null;

    window.addEventListener('online', () => {
      this.online = true;
      this.flush();
    });
    window.addEventListener('offline', () => {
      this.online = false;
    });
  }

  async headers() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`
    };
  }

  async fetch(path, options = {}) {
    try {
      const res = await fetch(`${this.apiUrl}${path}`, {
        ...options,
        headers: await this.headers()
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.error(`[Sync] ${path}:`, err.message);
      if (this.online) this.online = false;
      throw err;
    }
  }

  // Pull all data for today from server
  async pull(date) {
    if (!this.online) return null;
    try {
      this.syncing = true;
      const data = await this.fetch(`/api/functions/sync?date=${date}`);
      this.lastSync = data.serverTime;
      this.syncing = false;
      return data;
    } catch (err) {
      this.syncing = false;
      return null;
    }
  }

  // Push all changes to server
  async push(date, tasks, backlog, settings, history) {
    if (!this.online) {
      this.queue.push({ date, tasks, backlog, settings, history });
      return false;
    }
    try {
      this.syncing = true;
      await this.fetch('/api/functions/sync', {
        method: 'POST',
        body: JSON.stringify({ date, tasks, backlog, settings, history })
      });
      this.syncing = false;
      return true;
    } catch (err) {
      this.queue.push({ date, tasks, backlog, settings, history });
      this.syncing = false;
      return false;
    }
  }

  // Flush queued changes when reconnected
  async flush() {
    while (this.queue.length > 0 && this.online) {
      const item = this.queue.shift();
      try {
        await this.push(item.date, item.tasks, item.backlog, item.settings, item.history);
      } catch (err) {
        this.queue.unshift(item);
        break;
      }
    }
  }

  // Merge server data with local, server wins for conflicts
  mergeData(local, server) {
    if (!server) return local;
    return {
      tasks: server.tasks || local.tasks || [],
      backlog: { ...local.backlog, ...server.backlog },
      settings: server.settings || local.settings,
      history: server.history || local.history
    };
  }
}

// Export for dashboard integration
export const initSync = (apiUrl, apiKey) => new SyncClient(apiUrl, apiKey);
