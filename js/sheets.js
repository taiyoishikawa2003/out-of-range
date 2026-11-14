import { h, icon, sourcesBlock } from './render.js';
import { t, L, getLang } from './i18n.js';
import { localComments, addComment } from './store.js';
import { account } from './data.js';

let tmr;
export function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.classList.add('show');
  clearTimeout(tmr); tmr = setTimeout(() => el.classList.remove('show'), 1600);
}
export const fmt = n => new Intl.NumberFormat(getLang() === 'ja' ? 'ja-JP' : 'en', { notation: 'compact', maximumFractionDigits: 1 }).format(n);

let current = null;
export function closeSheet() {
  if (!current) return;
  const { scrim, sheet, prevFocus, onKey } = current;
  scrim.remove(); sheet.remove(); document.removeEventListener('keydown', onKey, true);
  current = null; prevFocus?.focus?.();
}
export const sheetOpen = () => !!current;

function openSheet(title, body, footer) {
  closeSheet();
  const root = document.getElementById('sheet-root');
  const scrim = h('div', { class: 'scrim', onclick: closeSheet });
  const x = h('button', { class: 'x', type: 'button', 'aria-label': 'Close', onclick: closeSheet }, icon('x'));
  const head = h('header', {}, h('span', { text: title }), x);
  const sheet = h('div', { class: 'sheet', role: 'dialog', 'aria-modal': 'true', 'aria-label': title }, head, h('div', { class: 'body' }, body), footer || '');
  // drag header down to close
  let y0 = null;
  head.addEventListener('pointerdown', e => { y0 = e.clientY; head.setPointerCapture(e.pointerId); });
  head.addEventListener('pointermove', e => { if (y0 != null) sheet.style.transform = `translateY(${Math.max(0, e.clientY - y0)}px)`; });
  head.addEventListener('pointerup', e => { if (y0 != null && e.clientY - y0 > 80) closeSheet(); else sheet.style.transform = ''; y0 = null; });
  const onKey = e => {
    if (e.key === 'Escape') { e.stopPropagation(); closeSheet(); }
    if (e.key === 'Tab') { // keep focus inside
      const f = [...sheet.querySelectorAll('button,a,input')]; if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f.at(-1).focus(); }
      else if (!e.shiftKey && document.activeElement === f.at(-1)) { e.preventDefault(); f[0].focus(); }
    }
    e.stopPropagation();
  };
  document.addEventListener('keydown', onKey, true);
  root.append(scrim, sheet);
  current = { scrim, sheet, prevFocus: document.activeElement, onKey };
  setTimeout(() => x.focus(), 30);
  return sheet;
}

const initial = s => (s || '?').replace(/^@/, '').slice(0, 1).toUpperCase();

/* comment likes are kept on this device only */
const CL = 'oor.cmlikes';
const cmLikes = () => { try { return new Set(JSON.parse(localStorage.getItem(CL) || '[]')); } catch { return new Set(); } };
const toggleCmLike = k => { const s = cmLikes(); s.has(k) ? s.delete(k) : s.add(k); try { localStorage.setItem(CL, JSON.stringify([...s])); } catch {} return s.has(k); };

function likeBtn(key, base = 0) {
  const b = h('button', { class: 'cmlike', type: 'button' });
  const draw = on => { b.replaceChildren(icon('heart'), h('span', { text: base + (on ? 1 : 0) ? fmt(base + (on ? 1 : 0)) : '' })); b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); b.setAttribute('aria-label', t('like')); };
  draw(cmLikes().has(key));
  b.addEventListener('click', () => draw(toggleCmLike(key)));
  return b;
}

function explainCard(post, c) {
  const e = c.explain; const box = h('div', { class: 'xp' });
  const full = () => h('div', { class: 'xp-in' },
    h('div', { class: 'xp-title', text: L(e.title) }),
    h('p', { class: 'xp-lead', text: L(e.lead) }),
    h('ol', { class: 'xp-steps' }, e.steps.map((st, i) => h('li', {},
      h('span', { class: 'xp-n', text: String(i + 1) }),
      h('div', {}, h('b', { text: L(st.h) }), h('p', { text: L(st.t) }),
        st.img ? h('figure', {}, h('img', { src: st.img, alt: L(st.alt) || '', loading: 'lazy' }), st.cap ? h('figcaption', { text: L(st.cap) }) : '') : '')))),
    e.why ? h('div', { class: 'xp-why' }, h('b', { text: L(e.why.h) }), h('p', { text: L(e.why.t) })) : '',
    e.note ? h('p', { class: 'xp-note', text: L(e.note) }) : '',
    h('button', { class: 'btn sm ghost xp-src', type: 'button', text: t('cm.sources'), onclick: () => openSources(post) }));
  if (c.spoiler) {
    const cover = h('button', { class: 'xp-cover', type: 'button' }, h('span', { class: 'xp-eye', text: '?' }), h('b', { text: L(c.spoiler) }), h('small', { text: t('cm.spoilerHint') }));
    cover.addEventListener('click', () => { box.replaceChildren(full()); });
    box.append(cover);
  } else box.append(full());
  return box;
}

export function openComments(post, onCount) {
  const list = h('div', { class: 'cmlist' });
  const draw = () => {
    list.replaceChildren();
    const seeded = post.comments || [];
    const mine = localComments(post.id);
    seeded.forEach((c, i) => {
      const a = account(c.user); const isAuthor = c.user === post.account;
      const name = h('div', { class: 'n' }, h('span', { text: '@' + c.user }),
        isAuthor ? h('span', { class: 'badge', text: t('cm.author') }) : '', c.pinned ? h('span', { class: 'badge pin', text: '📌 ' + t('cm.pinned') }) : '');
      list.append(h('div', { class: 'cm' + (c.pinned ? ' pinned' : '') },
        h('div', { class: 'av', text: initial(L(a.name) || c.user) }),
        h('div', { class: 'cm-main' }, name, c.explain ? explainCard(post, c) : h('div', { class: 't', text: L(c.text) })),
        likeBtn(post.id + ':s' + i, c.likes || 0)));
    });
    mine.forEach((c, i) => list.append(h('div', { class: 'cm' },
      h('div', { class: 'av me', text: '★' }),
      h('div', { class: 'cm-main' }, h('div', { class: 'n' }, h('span', { text: t('mine') })), h('div', { class: 't', text: c.text }), h('div', { class: 'loc', text: t('cm.local') })),
      likeBtn(post.id + ':m' + i))));
    if (!mine.length) list.append(h('p', { class: 'cm-empty', text: t('cm.first') }));
  };
  draw();
  const input = h('input', { type: 'text', maxlength: '150', placeholder: t('cm.placeholder'), 'aria-label': t('cm.placeholder'), enterkeyhint: 'send' });
  const send = h('button', { class: 'cmsend', type: 'submit', 'aria-label': t('cm.send'), text: t('cm.send') });
  const sync = () => { send.disabled = !input.value.trim(); };
  input.addEventListener('input', sync); sync();
  const chips = h('div', { class: 'cmchips' }, ['😱', '🫣', '👀', '🤯', '🔥', '👏'].map(em =>
    h('button', { type: 'button', text: em, 'aria-label': em, onclick: () => { input.value += em; sync(); input.focus(); } })));
  const form = h('form', { class: 'cmform', onsubmit: e => {
    e.preventDefault(); const v = input.value.trim(); if (!v) return;
    addComment(post.id, v); input.value = ''; sync(); draw(); onCount?.(); list.querySelector('.cm-empty')?.remove();
    list.lastElementChild?.scrollIntoView({ block: 'end', behavior: 'smooth' });
  } }, chips, h('div', { class: 'cmrow' }, input, send));
  const n = (post.comments?.length || 0) + localComments(post.id).length;
  openSheet(t('cm.count').replace('{n}', n), list, form);
  document.querySelector('.sheet:last-of-type')?.classList.add('tall');
}

export function openSources(post) {
  const body = h('div', {}, h('p', { class: 'hint', text: t('src.note') }),
    h('ul', { class: 'srclist' }, (post.sources || []).map(s => h('li', {},
      s.kind ? h('span', { class: 'k', text: L(s.kind) }) : '',
      s.url ? h('a', { href: s.url, target: '_blank', rel: 'noopener', text: L(s.title) || s.url }) : h('b', { text: L(s.title) }),
      s.note ? h('div', { class: 'hint', text: L(s.note) }) : ''))));
  openSheet(t('src.title'), body);
}

export function postUrl(post) {
  return location.href.split('#')[0] + '#/p/' + encodeURIComponent(post.id);
}
export function openShare(post) {
  const url = postUrl(post);
  const copy = async () => {
    try { await navigator.clipboard.writeText(url); } catch {
      const ta = h('textarea', { style: { position: 'fixed', opacity: 0 } }); ta.value = url; document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove();
    }
    closeSheet(); toast(t('share.copied'));
  };
  const btns = [h('button', { type: 'button', onclick: copy }, icon('link'), t('share.copy'))];
  if (navigator.share) btns.push(h('button', { type: 'button', onclick: () => { closeSheet(); navigator.share({ title: 'OUT OF RANGE', text: L(post.caption), url }).catch(() => {}); } }, icon('share'), t('share.native')));
  openSheet(t('share.title'), h('div', { class: 'sharegrid' }, btns));
}

export { sourcesBlock };
