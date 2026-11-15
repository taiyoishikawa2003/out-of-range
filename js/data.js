import { L } from './i18n.js';
import { loadMine } from './store.js';

export const db = { posts: [], accounts: {}, library: [], mine: [] };

export async function loadData() {
  // retry: a phone on a weak connection (or a moment during a site update) can fail one request
  const j = async u => {
    for (let k = 0; ; k++) {
      try { const r = await fetch(u + (k ? `?r=${Date.now()}` : ''), { cache: k ? 'reload' : 'no-cache' }); if (!r.ok) throw new Error(r.status); return await r.json(); }
      catch (e) { if (k >= 3) throw e; await new Promise(res => setTimeout(res, 600 * (k + 1))); }
    }
  };
  const [posts, accounts, library] = await Promise.all([j('data/posts.json'), j('data/accounts.json'), j('data/library.json')]);
  db.posts = posts; db.accounts = accounts; db.library = library;
  await reloadMine();
}
export async function reloadMine() {
  try { db.mine = await loadMine(); } catch { db.mine = []; }
  db.mine.forEach(p => { p.mine = true; });
}
/** All posts in feed order: user's own first, then the curated feed. */
export const allPosts = () => [...db.mine, ...db.posts];
export const postById = id => allPosts().find(p => p.id === id);
export const account = h => db.accounts[h] || { name: h, handle: h };
export const postsBy = h => allPosts().filter(p => p.account === h);
export function thumbOf(p) {
  if (p.type === 'video') return L(p.video.poster);
  if (p.type === 'app') return L(p.poster) || '';
  const s = p.slides?.[0] || {};
  return L(s.bg) || '';
}
