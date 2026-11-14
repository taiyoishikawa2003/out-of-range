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

export function openComments(post, onCount) {
  const list = h('div', {});
  const draw = () => {
    list.replaceChildren();
    const seeded = post.comments || [];
    const mine = localComments(post.id);
    if (!seeded.length && !mine.length) list.append(h('p', { class: 'hint', text: t('cm.empty') }));
    seeded.forEach(c => {
      const a = account(c.user);
      list.append(h('div', { class: 'cm' }, h('div', { class: 'av', text: initial(L(a.name) || c.user) }),
        h('div', {}, h('div', { class: 'n', text: L(a.name) || c.user }), h('div', { class: 't', text: L(c.text) }))));
    });
    mine.forEach(c => list.append(h('div', { class: 'cm' }, h('div', { class: 'av', style: { background: '#ffb000', color: '#111' }, text: '★' }),
      h('div', {}, h('div', { class: 'n', text: t('mine') }), h('div', { class: 't', text: c.text }), h('div', { class: 'loc', text: t('cm.local') })))));
  };
  draw();
  const input = h('input', { type: 'text', maxlength: '150', placeholder: t('cm.placeholder'), 'aria-label': t('cm.placeholder'), enterkeyhint: 'send' });
  const form = h('form', { class: 'cmform', onsubmit: e => {
    e.preventDefault(); const v = input.value.trim(); if (!v) return;
    addComment(post.id, v); input.value = ''; draw(); onCount?.(); list.lastChild?.scrollIntoView({ block: 'end' });
  } }, input, h('button', { class: 'btn sm', type: 'submit', text: t('cm.send') }));
  const n = (post.comments?.length || 0) + localComments(post.id).length;
  openSheet(`${t('comments')} ${n ? '(' + n + ')' : ''}`, list, form);
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
