import { L, t } from './i18n.js';
import { refUrl } from './store.js';

/** Tiny DOM builder. Text is always set via textContent (no HTML injection). */
export function h(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') e.className = v;
    else if (k === 'text') e.textContent = v;
    else if (k === 'html') e.innerHTML = v; // only used for trusted static icons
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
    else if (k === 'style' && typeof v === 'object') Object.assign(e.style, v);
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(c));
  return e;
}

export const ICON = {
  heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-4.5-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 6C19 16.5 12 21 12 21z"/></svg>',
  comment: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C6.5 3 2 6.8 2 11.5c0 2.5 1.3 4.7 3.3 6.3L4.5 21l4-1.8c1.1.3 2.3.5 3.5.5 5.5 0 10-3.8 10-8.5S17.5 3 12 3z"/></svg>',
  save: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-6-4-6 4z"/></svg>',
  share: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4l8 8-8 8v-5c-6 0-9 2-12 6 1-6 4-11 12-12z"/></svg>',
  doc: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h7"/></svg>',
  play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l14 8-14 8z"/></svg>',
  music: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18V5l12-2v13" stroke="#fff" stroke-width="2" fill="none"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
  mute: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>',
  sound: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M17 8a5 5 0 0 1 0 8M19.5 5.5a9 9 0 0 1 0 13"/></svg>',
  speak: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/></svg>',
  search: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
  up: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M6 15l6-6 6 6"/></svg>',
  down: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M6 9l6 6 6-6"/></svg>',
  left: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M15 6l-6 6 6 6"/></svg>',
  right: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M9 6l6 6-6 6"/></svg>',
  x: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  link: '<svg viewBox="0 0 24 24" aria-hidden="true" class="st"><path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1"/><path d="M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/></svg>',
  layers: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5" stroke="#fff" stroke-width="2" fill="none"/></svg>'
};
export const icon = n => { const s = document.createElement('span'); s.style.display = 'contents'; s.innerHTML = ICON[n]; return s.firstChild; };

/** Image with lazy src (data-src) and graceful failure. */
export function img(src, cls = 'bg', alt = '') {
  const i = h('img', { class: cls, alt, decoding: 'async', draggable: 'false' });
  if (src) i.dataset.src = refUrl(src);
  i.addEventListener('error', () => { i.replaceWith(h('div', { class: cls + ' broken', style: { display: 'grid', placeItems: 'center', background: '#2a2a2a', color: '#999', fontSize: '12px' }, text: t('err.media') })); });
  return i;
}
export const loadImgs = (root, eager) => root.querySelectorAll('img[data-src]').forEach(i => {
  if (eager) i.loading = 'eager';
  i.src = i.dataset.src; i.removeAttribute('data-src');
});

const txt = (o, cls = 'label') => h('span', { class: 'tx tx-' + cls, text: L(o) });

/**
 * Generic slide: background media + text layers. Post templates are NOT defined here;
 * a template is just data (which texts, where, in what style) chosen later by the team.
 */
export function renderSlide(s, { post } = {}) {
  const el = h('section', { class: 'slide', 'aria-roledescription': 'slide' });
  if (s.layout === 'sources') { el.append(sourcesBlock(post)); return el; }
  if (s.bg) el.append(img(s.bg, 'bg', L(s.alt) || ''));
  if (s.pos === 'bottom') el.append(h('div', { class: 'shade' }));
  el.append(h('div', { class: 'lay ' + (s.pos || 'top') }, (s.texts || []).map(x => txt(x.t, x.style || 'label'))));
  return el;
}

export function sourcesBlock(post) {
  return h('div', { class: 'srcslide' },
    h('span', { class: 'realbadge', text: t('true') }),
    h('h3', { text: t('sources') }),
    h('ol', {}, (post.sources || []).map(s => h('li', {},
      s.url ? h('a', { href: s.url, target: '_blank', rel: 'noopener', text: L(s.title) || s.url }) : h('span', { text: L(s.title) }),
      s.note ? h('div', { class: 'hint', text: L(s.note) }) : null))));
}

/** Plain text of a slide, for read-aloud and search. */
/** Plain text of a slide, for read-aloud and search. */
export function slideText(s) {
  return (s.texts || []).map(x => L(x.t)).filter(Boolean).join('。 ');
}
