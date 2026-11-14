import { h, icon, loadImgs, renderSlide } from './render.js';
import { t, L } from './i18n.js';
import * as S from './store.js';
import { db, reloadMine } from './data.js';
import { toast } from './sheets.js';

const LAYOUTS = ['overlay', 'number', 'quiz', 'compare', 'chat', 'document'];
const blank = (layout = 'overlay', bg) => ({ layout, bg: bg || db.library[0]?.src || '', bg2: db.library[1]?.src || '', pos: 'top', a: '', b: '', c: '', opts: '', ans: '1', rows: '', name: '' });

/** Turn simple form values into the shared slide schema used by the feed. */
function compile(f) {
  const s = { layout: f.layout, bg: f.bg };
  switch (f.layout) {
    case 'overlay': s.pos = f.pos; s.texts = [[f.a, 'title'], [f.b, 'label'], [f.c, 'highlight']].filter(x => x[0].trim()).map(([t, style]) => ({ t, style })); break;
    case 'number': Object.assign(s, { label: f.a, value: f.b, note: f.c }); break;
    case 'quiz': Object.assign(s, { q: f.a, options: f.opts.split('\n').map(x => x.trim()).filter(Boolean).slice(0, 4), answer: Math.max(0, (parseInt(f.ans, 10) || 1) - 1), explain: f.c }); break;
    case 'compare': Object.assign(s, { bg2: f.bg2, label1: f.a, label2: f.b, note: f.c }); break;
    case 'chat': delete s.bg; Object.assign(s, { name: f.name, msgs: f.rows.split('\n').filter(x => x.trim()).map(x => x.startsWith('>') ? { me: true, t: x.slice(1).trim() } : { t: x.trim() }) }); break;
    case 'document': Object.assign(s, { title: f.a, big: f.b, stamp: f.c, rows: f.rows.split('\n').filter(x => x.includes(':') || x.includes('：')).map(x => { const [k, ...v] = x.split(/[:：]/); return { k: k.trim(), v: v.join(':').trim() }; }) }); break;
  }
  return s;
}

export function renderCreate(view) {
  const d = { slides: [blank()], cur: 0, caption: '', srcTitle: '', srcUrl: '' };
  const pv = h('div', { class: 'pv', 'aria-label': 'Preview' });
  const form = h('div', {});
  const page = h('div', { class: 'page' }, h('h1', { text: t('cr.title') }), h('div', { class: 'cr' }, pv, form));

  const f = () => d.slides[d.cur];
  const drawPreview = () => { const el = renderSlide(compile(f())); pv.replaceChildren(el); loadImgs(el, true); };
  const field = (label, key, { area, type = 'text', max = 120 } = {}) => {
    const inp = area ? h('textarea', { maxlength: 400 }) : h('input', { type, maxlength: max });
    inp.value = f()[key]; inp.addEventListener('input', () => { f()[key] = inp.value; drawPreview(); });
    return [h('label', { text: label }), inp];
  };
  const picker = (key, label) => {
    const lib = h('div', { class: 'lib' });
    const drawLib = () => lib.replaceChildren(...db.library.map(it => h('button', { type: 'button', class: f()[key] === it.src ? 'on' : '', 'aria-label': L(it.title), 'aria-pressed': f()[key] === it.src,
      onclick: () => { f()[key] = it.src; drawLib(); drawPreview(); drawThumbs(); } }, h('img', { src: it.src, alt: '' }))));
    drawLib();
    const file = h('input', { type: 'file', accept: 'image/*', hidden: true, onchange: async () => {
      const fl = file.files[0]; if (!fl) return;
      f()[key] = await S.putImage(fl); drawLib(); drawPreview(); drawThumbs();
    } });
    return [h('label', { text: label }), lib, h('div', { class: 'row2' }, h('button', { class: 'btn ghost sm', type: 'button', text: t('cr.upload'), onclick: () => file.click() }), file),
      h('p', { class: 'hint', text: t('cr.privacy') })];
  };

  const thumbs = h('div', { class: 'thumbs', role: 'tablist' });
  function drawThumbs() {
    thumbs.replaceChildren(...d.slides.map((s, i) => h('button', { type: 'button', role: 'tab', 'aria-selected': i === d.cur, class: i === d.cur ? 'on' : '', 'aria-label': `${t('cr.slides')} ${i + 1}`, onclick: () => { d.cur = i; drawAll(); } },
      s.bg && s.layout !== 'chat' ? h('img', { src: S.refUrl(s.bg), alt: '' }) : '', h('span', { class: 'n', text: i + 1 }))),
      h('button', { type: 'button', 'aria-label': t('cr.add'), style: { display: 'grid', placeItems: 'center', fontSize: '28px' }, text: '+', onclick: () => { d.slides.push(blank(f().layout, f().bg)); d.cur = d.slides.length - 1; drawAll(); } }));
  }

  function drawForm() {
    const s = f();
    const lays = h('div', { class: 'layouts' }, LAYOUTS.map(k => h('button', { type: 'button', class: s.layout === k ? 'on' : '', 'aria-pressed': s.layout === k, text: t('lay.' + k), onclick: () => { s.layout = k; drawAll(); } })));
    const fields = [];
    const pos = () => { const sel = h('select', {}, ['top', 'center', 'bottom'].map(k => h('option', { value: k, text: t('cr.' + k), selected: s.pos === k }))); sel.addEventListener('change', () => { s.pos = sel.value; drawPreview(); }); return [h('label', { text: t('cr.pos') }), sel]; };
    switch (s.layout) {
      case 'overlay': fields.push(...field(t('cr.text'), 'a'), ...field(t('cr.text2'), 'b'), ...field(t('cr.text3'), 'c'), ...pos(), ...picker('bg', t('cr.bg'))); break;
      case 'number': fields.push(...field(t('cr.text'), 'a'), ...field(t('cr.number'), 'b', { max: 12 }), ...field(t('cr.text3'), 'c'), ...picker('bg', t('cr.bg'))); break;
      case 'quiz': fields.push(...field(t('cr.question'), 'a'), ...field(t('cr.options'), 'opts', { area: true }), ...field(t('cr.answer'), 'ans', { type: 'number', max: 1 }), ...field(t('cr.explain'), 'c'), ...picker('bg', t('cr.bg'))); break;
      case 'compare': fields.push(...field(t('cr.before'), 'a'), ...field(t('cr.after'), 'b'), ...field(t('cr.text3'), 'c'), ...picker('bg', t('cr.bg')), ...picker('bg2', t('cr.bg2'))); break;
      case 'chat': fields.push(...field('Name', 'name'), ...field(t('cr.msgs'), 'rows', { area: true })); break;
      case 'document': fields.push(...field(t('cr.docTitle'), 'a'), ...field(t('cr.text'), 'b'), ...field(t('cr.rows'), 'rows', { area: true }), ...field(t('cr.stamp'), 'c'), ...picker('bg', t('cr.bg'))); break;
    }
    const cap = h('textarea', { maxlength: 300 }); cap.value = d.caption; cap.addEventListener('input', () => { d.caption = cap.value; });
    const st = h('input', { type: 'text', maxlength: 120 }); st.value = d.srcTitle; st.addEventListener('input', () => { d.srcTitle = st.value; });
    const su = h('input', { type: 'url', maxlength: 400, placeholder: 'https://' }); su.value = d.srcUrl; su.addEventListener('input', () => { d.srcUrl = su.value; });
    form.replaceChildren(
      h('label', { text: t('cr.slides') }), thumbs,
      d.slides.length > 1 ? h('button', { class: 'btn ghost sm', type: 'button', text: t('cr.remove'), onclick: () => { d.slides.splice(d.cur, 1); d.cur = Math.max(0, d.cur - 1); drawAll(); } }) : '',
      h('label', { text: t('cr.layout') }), lays, ...fields,
      h('label', { text: t('cr.caption') }), cap,
      h('label', { text: t('cr.sourceTitle') }), st, h('label', { text: t('cr.source') }), su,
      h('div', { class: 'row2' }, h('button', { class: 'btn', type: 'button', text: t('cr.post'), onclick: post }),
        h('button', { class: 'btn ghost', type: 'button', text: t('cr.download'), onclick: download })));
  }
  function drawAll() { drawThumbs(); drawForm(); drawPreview(); }

  function sources() {
    const out = [];
    if (/^https?:\/\/\S+\.\S+/.test(d.srcUrl.trim())) out.push({ title: d.srcTitle.trim() || d.srcUrl.trim(), url: d.srcUrl.trim() });
    const used = new Set(d.slides.flatMap(s => [s.bg, s.layout === 'compare' ? s.bg2 : null]));
    db.library.filter(it => used.has(it.src) && it.url).forEach(it => out.push({ kind: { en: 'Photo', ja: '写真' }, title: L(it.credit), url: it.url }));
    return out;
  }
  async function post() {
    const src = sources();
    if (!src.some(s => !s.kind)) { toast(t('cr.needSource')); return; }
    const p = { id: 'me-' + Date.now().toString(36), type: 'carousel', account: 'you', caption: d.caption.trim(), tags: [], slides: d.slides.map(compile), sources: src, stats: {} };
    await S.saveMine(p); await reloadMine();
    toast(t('cr.posted')); location.hash = '#/p/' + p.id;
  }
  async function download() {
    if (!window.htmlToImage) return;
    toast(t('cr.downloading'));
    const box = h('div', { style: { position: 'fixed', left: '-10000px', top: 0, width: '360px', height: '640px' } });
    document.body.append(box);
    for (let i = 0; i < d.slides.length; i++) {
      const el = renderSlide(compile(d.slides[i]), { interactive: false });
      el.style.width = '360px'; el.style.height = '640px';
      box.replaceChildren(h('div', { class: 'cr' }, h('div', { class: 'pv', style: { width: '360px', borderRadius: 0, border: 0 } }, el)));
      loadImgs(el, true);
      await Promise.all([...el.querySelectorAll('img')].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
      try {
        const url = await window.htmlToImage.toPng(box.firstChild.firstChild, { pixelRatio: 3, cacheBust: true });
        h('a', { href: url, download: `out-of-range-${i + 1}.png` }).click();
      } catch (e) { console.warn(e); }
    }
    box.remove();
  }
  drawAll();
  view.replaceChildren(page);
}
