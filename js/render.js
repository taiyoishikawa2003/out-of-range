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

export function renderSlide(s, { post, interactive = true } = {}) {
  const lay = s.layout || 'overlay';
  const el = h('section', { class: 'slide lay-' + lay, 'aria-roledescription': 'slide' });
  const bg = () => s.bg && el.append(img(s.bg, 'bg', L(s.alt) || ''));
  switch (lay) {
    case 'overlay': {
      bg(); if (s.pos === 'bottom') el.append(h('div', { class: 'shade' }));
      el.append(h('div', { class: 'lay ' + (s.pos || 'top') }, (s.texts || []).map(x => txt(x.t, x.style || 'label'))));
      break;
    }
    case 'number': {
      bg();
      el.append(h('div', { class: 'lay center' }, s.label && txt(s.label, 'label'), h('span', { class: 'tx tx-big' + ([...L(s.value)].length > 5 ? ' long' : ''), text: L(s.value) }), s.note && txt(s.note, 'highlight')));
      break;
    }
    case 'quiz': {
      bg();
      const box = h('div', { class: 'lay top quiz' }, txt(s.q, 'label'));
      const exp = s.explain ? h('div', { class: 'qexp', hidden: true, text: L(s.explain) }) : null;
      (s.options || []).forEach((o, i) => {
        const b = h('button', { class: 'qopt', type: 'button', text: `${'ABCD'[i]}. ${L(o)}` });
        if (interactive) b.addEventListener('click', ev => {
          ev.stopPropagation();
          box.querySelectorAll('.qopt').forEach((x, j) => x.classList.add(j === s.answer ? 'right' : (x === b ? 'wrong' : 'x')));
          if (exp) exp.hidden = false;
        });
        box.append(b);
      });
      box.append(exp || '', h('span', { class: 'tx tx-note', text: t('quiz.tap') }));
      el.append(box);
      break;
    }
    case 'compare': {
      el.append(h('div', { class: 'cmp' },
        h('div', {}, img(s.bg, '', ''), h('span', { class: 'tag' }, txt(s.label1, 'label'))),
        h('div', {}, img(s.bg2, '', ''), h('span', { class: 'tag' }, txt(s.label2, 'highlight')))));
      if (s.note) el.append(h('div', { class: 'lay bottom' }, txt(s.note, 'note')));
      break;
    }
    case 'chat': {
      el.append(h('div', { class: 'chat' }, h('div', { class: 'who', text: L(s.name) }),
        (s.msgs || []).map(m => h('div', { class: 'bub ' + (m.me ? 'me' : 'them'), text: L(m.t) }))));
      break;
    }
    case 'document': {
      bg();
      el.append(h('div', { class: 'paper' }, h('h3', { text: L(s.title) }), s.big && h('div', { class: 'big', text: L(s.big) }),
        (s.rows || []).map(r => h('div', { class: 'row' }, h('b', { text: L(r.k) + '：' }), h('span', { text: L(r.v) }))),
        s.stamp && h('div', { class: 'stamp', text: L(s.stamp) })));
      break;
    }
    case 'tier': {
      const colors = { S: '#ff6b6b', A: '#ffb000', B: '#ffe066', C: '#8ce99a', D: '#74c0fc' };
      el.style.background = '#111';
      el.append(h('div', { class: 'tier' }, s.title && txt(s.title, 'label'),
        (s.rows || []).map(r => h('div', { class: 'row' }, h('div', { class: 'k', style: { background: colors[r.tier] || '#ccc' }, text: r.tier }),
          h('div', { class: 'v' }, (r.items || []).map(it => h('div', { class: 'it' }, img(it.img, '', L(it.label)), h('span', { text: L(it.label) }))))))));
      break;
    }
    case 'dump': {
      el.style.background = '#111';
      el.append(h('div', { class: 'dump' }, (s.images || []).map(u => img(u, '', ''))));
      if (s.texts) el.append(h('div', { class: 'lay bottom' }, s.texts.map(x => txt(x.t, x.style || 'label'))));
      break;
    }
    case 'sources': {
      el.append(sourcesBlock(post));
      break;
    }
  }
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
export function slideText(s) {
  const parts = [];
  const add = v => { const x = L(v); if (x) parts.push(x); };
  (s.texts || []).forEach(x => add(x.t));
  ['label', 'value', 'note', 'q', 'explain', 'label1', 'label2', 'title', 'big', 'stamp', 'name'].forEach(k => s[k] && add(s[k]));
  (s.options || []).forEach(add);
  (s.rows || []).forEach(r => { if (r.k) { add(r.k); add(r.v); } (r.items || []).forEach(i => add(i.label)); });
  (s.msgs || []).forEach(m => add(m.t));
  return parts.join('。 ');
}
