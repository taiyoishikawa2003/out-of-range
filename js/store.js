import { get, set, del } from '../vendor/idb-keyval.js';

const KEY = 'oor.state.v1';
const def = { likes: {}, saves: {}, follows: {}, comments: {}, stamps: {}, muted: false, read: false, cc: true };
let st;
try { st = { ...def, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; } catch { st = { ...def }; }
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch {} };
const subs = new Set();
const emit = (k, v) => subs.forEach(f => f(k, v));
export const onChange = f => subs.add(f);

export const isLiked = id => !!st.likes[id];
export const isSaved = id => !!st.saves[id];
export const isFollowing = h => !!st.follows[h];
export const likedIds = () => Object.keys(st.likes).filter(k => st.likes[k]).sort((a, b) => st.likes[b] - st.likes[a]);
export const savedIds = () => Object.keys(st.saves).filter(k => st.saves[k]).sort((a, b) => st.saves[b] - st.saves[a]);
export const followedHandles = () => Object.keys(st.follows).filter(k => st.follows[k]);
function toggle(map, id, force) {
  const on = force ?? !st[map][id];
  if (on) st[map][id] = Date.now(); else delete st[map][id];
  save(); emit(map, id); return on;
}
export const toggleLike = (id, force) => toggle('likes', id, force);
export const toggleSave = id => toggle('saves', id);
export const toggleFollow = h => toggle('follows', h);
export const localComments = id => st.comments[id] || [];
export function addComment(id, text) {
  (st.comments[id] ||= []).push({ text, at: Date.now() });
  save(); emit('comments', id);
}
/* fact-check stamps: one for each post whose sources the reader has opened */
export const stampIds = () => Object.keys(st.stamps || {});
export function addStamp(id) {
  if (!st.stamps) st.stamps = {};
  if (st.stamps[id]) return false;
  st.stamps[id] = Date.now(); save(); emit('stamps', id); return true;
}
export const isMuted = () => st.muted;
export function setMuted(m) { st.muted = m; save(); emit('muted', m); }
export const isCC = () => st.cc !== false;
export function setCC(v) { st.cc = v; save(); emit('cc', v); }
export const isRead = () => st.read;
export function setRead(r) { st.read = r; save(); emit('read', r); }

/* ---------- user-made posts (IndexedDB, never uploaded) ---------- */
const urlCache = new Map();
export async function loadMine() {
  const list = (await get('oor.mine')) || [];
  for (const p of list) for (const s of p.slides) for (const k of ['bg']) {
    if (s[k] && s[k].startsWith('idb:')) s[k] = await blobUrl(s[k]);
  }
  return list;
}
export async function blobUrl(ref) {
  if (urlCache.has(ref)) return urlCache.get(ref);
  const b = await get(ref);
  const u = b ? URL.createObjectURL(b) : '';
  urlCache.set(ref, u); return u;
}
export async function putImage(file) {
  const ref = 'idb:img:' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  await set(ref, file);
  urlCache.set(ref, URL.createObjectURL(file));
  return ref;
}
export const refUrl = ref => urlCache.get(ref) || ref;
export async function saveMine(post) {
  const list = (await get('oor.mine')) || [];
  list.unshift(post); await set('oor.mine', list);
}
export async function deleteMine(id) {
  const list = (await get('oor.mine')) || [];
  const p = list.find(x => x.id === id);
  if (p) for (const s of p.slides) for (const k of ['bg']) if (s[k]?.startsWith('idb:')) await del(s[k]);
  await set('oor.mine', list.filter(x => x.id !== id));
}
