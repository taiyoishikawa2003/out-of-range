import { h, icon, sourcesBlock } from './render.js';
import { t, L, getLang } from './i18n.js';
import { localComments, addComment, addStamp, stampIds } from './store.js';
import { account, db } from './data.js';

let tmr;
export function toast(msg, gold = false) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.classList.add('show'); el.classList.toggle('gold', gold);
  clearTimeout(tmr); tmr = setTimeout(() => el.classList.remove('show'), gold ? 2800 : 1600);
}
const cmCount = n => (n === 1 && getLang() !== 'ja' ? '1 comment' : t('cm.count').replace('{n}', n));
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

/* comment reactions (👍/👎) are kept on this device only */
const CL = 'oor.cmreact';
const reacts = () => { try { return JSON.parse(localStorage.getItem(CL) || '{}'); } catch { return {}; } };
const setReact = (k, v) => { const r = reacts(); if (r[k] === v) delete r[k]; else r[k] = v; try { localStorage.setItem(CL, JSON.stringify(r)); } catch {} return r[k]; };
const ago = ms => {
  const m = Math.floor((Date.now() - ms) / 60000);
  if (m < 1) return t('cm.now');
  if (m < 60) return t('cm.min').replace('{n}', m);
  const hr = Math.floor(m / 60); if (hr < 24) return t('cm.hour').replace('{n}', hr);
  return t('cm.day').replace('{n}', Math.floor(hr / 24));
};
const THUMB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10v11H3V10h4zm2 11h8.3a2 2 0 0 0 2-1.6l1.4-7A2 2 0 0 0 18.7 10H14l.8-4.2A1.8 1.8 0 0 0 13 3.6L9 9.5V21z"/></svg>';

function actions(key, base = 0) {
  const up = h('button', { class: 'ya', type: 'button', 'aria-label': t('like') });
  const dn = h('button', { class: 'ya dn', type: 'button', 'aria-label': t('cm.dislike') });
  const draw = () => {
    const v = reacts()[key]; const n = base + (v === 1 ? 1 : 0);
    up.innerHTML = THUMB; if (n) up.append(h('span', { text: fmt(n) }));
    dn.innerHTML = THUMB;
    up.classList.toggle('on', v === 1); dn.classList.toggle('on', v === -1);
    up.setAttribute('aria-pressed', v === 1); dn.setAttribute('aria-pressed', v === -1);
  };
  up.addEventListener('click', () => { setReact(key, 1); draw(); });
  dn.addEventListener('click', () => { setReact(key, -1); draw(); });
  draw();
  return h('div', { class: 'yacts' }, up, dn);
}

/* long comments collapse to a few lines with "Read more" / "Show less", like YouTube */
function longText(text) {
  const box = h('div', { class: 'ytx clamp', text });
  const more = h('button', { class: 'ymore', type: 'button', text: t('more') });
  more.addEventListener('click', () => { const open = box.classList.toggle('clamp'); more.textContent = t(open ? 'more' : 'less'); });
  requestAnimationFrame(() => { if (box.scrollHeight <= box.clientHeight + 2) more.remove(); });
  return [box, more];
}

/* YouTube-style comment thread; used in the bottom sheet (phone) and the side panel (desktop) */
export function commentsView(post, onCount) {
  const root = h('div', { class: 'yc' });
  const count = h('div', { class: 'yc-count' });
  const list = h('div', { class: 'yc-list' });
  const total = () => (post.comments?.length || 0) + localComments(post.id).length;
  const draw = () => {
    count.textContent = cmCount(total());
    list.replaceChildren();
    (post.comments || []).forEach((c, i) => {
      const a = account(c.user); const isAuthor = c.user === post.account;
      list.append(h('div', { class: 'ycm' + (c.pinned ? ' pinned' : '') },
        a.avatar ? h('img', { class: 'av', src: a.avatar, alt: '' }) : h('div', { class: 'av', text: initial(L(a.name) || c.user) }),
        h('div', { class: 'ycm-main' },
          c.pinned ? h('div', { class: 'ypin', text: '📌 ' + t('cm.pinnedBy').replace('{u}', '@' + c.user) }) : '',
          h('div', { class: 'yhd' }, h('span', { class: 'yname' + (isAuthor ? ' author' : ''), text: '@' + c.user })),
          ...longText(L(c.text)),
          actions(post.id + ':s' + i, c.likes || 0))));
    });
    if ((post.comments || []).some(c => !c.pinned)) list.append(h('p', { class: 'cm-note', text: t('cm.cast') }));
    const mine = localComments(post.id);
    mine.forEach((c, i) => list.append(h('div', { class: 'ycm' },
      h('div', { class: 'av me', text: '★' }),
      h('div', { class: 'ycm-main' },
        h('div', { class: 'yhd' }, h('span', { class: 'yname', text: t('mine') }), c.at ? h('span', { class: 'ytime', text: ago(c.at) }) : '', h('span', { class: 'ytime', text: '· ' + t('cm.local') })),
        h('div', { class: 'ytx nofuri', text: c.text }),
        actions(post.id + ':m' + i)))));
    if (!mine.length) list.append(h('p', { class: 'cm-empty', text: t('cm.first') }));
  };
  const input = h('textarea', { rows: 1, maxlength: '300', placeholder: t('cm.placeholder'), 'aria-label': t('cm.placeholder') });
  const send = h('button', { class: 'ybtn primary', type: 'submit', text: t('cm.send') });
  const cancel = h('button', { class: 'ybtn', type: 'button', text: t('cm.cancel') });
  const chips = h('div', { class: 'cmchips' }, ['😱', '🫣', '👀', '🤯', '🔥', '👏'].map(em =>
    h('button', { type: 'button', text: em, 'aria-label': em, onclick: () => { input.value += em; sync(); input.focus(); } })));
  const bar = h('div', { class: 'ybar' }, chips, h('div', { class: 'ybtns' }, cancel, send));
  const form = h('form', { class: 'yform' }, h('div', { class: 'av me', text: '★' }), h('div', { class: 'yin' }, input, bar));
  const sync = () => { send.disabled = !input.value.trim(); input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; };
  input.addEventListener('input', sync);
  input.addEventListener('focus', () => form.classList.add('open'));
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit(); } });
  cancel.addEventListener('click', () => { input.value = ''; sync(); form.classList.remove('open'); input.blur(); });
  form.addEventListener('submit', e => {
    e.preventDefault(); const v = input.value.trim(); if (!v) return;
    addComment(post.id, v); input.value = ''; sync(); draw(); onCount?.();
    list.querySelector('.ycm:last-of-type')?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });
  sync(); draw();
  root.append(count, form, list);
  return { root, focus: () => input.focus(), count: total };
}

export function openComments(post, onCount) {
  const v = commentsView(post, onCount);
  openSheet(cmCount(v.count()), v.root);
  document.querySelector('#sheet-root .sheet')?.classList.add('tall');
}

export function openSources(post) {
  const body = h('div', {}, h('p', { class: 'hint', text: t('src.note') }),
    h('ul', { class: 'srclist' }, (post.sources || []).map(s => h('li', {},
      s.kind ? h('span', { class: 'k', text: L(s.kind) }) : '',
      s.url ? h('a', { href: s.url, target: '_blank', rel: 'noopener', text: L(s.title) || s.url }) : h('b', { text: L(s.title) }),
      s.note ? h('div', { class: 'hint', text: L(s.note) }) : ''))));
  openSheet(t('src.title'), body);
  // opening the sources is the habit we want to reward: it earns that post's fact-check stamp
  if (db.posts.some(p => p.id === post.id) && addStamp(post.id)) {
    const ids = new Set(db.posts.map(p => p.id)), n = stampIds().filter(id => ids.has(id)).length;
    toast(t(n === ids.size ? 'stamp.all' : 'stamp.got').replace('{n}', n).replace('{m}', ids.size), true);
  }
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
