import { loadMine } from './store.js';

export const db = { posts: [], accounts: {}, library: [], mine: [] };

export async function loadData() {
  const j = u => fetch(u, { cache: 'no-cache' }).then(r => r.json());
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
  if (p.type === 'video') return p.video.poster;
  const s = p.slides?.[0] || {};
  return s.bg || s.images?.[0] || s.rows?.[0]?.items?.[0]?.img || '';
}
