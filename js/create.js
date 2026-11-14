import { h, icon, loadImgs, renderSlide } from './render.js';
import { t, L } from './i18n.js';
import * as S from './store.js';
import { db, reloadMine } from './data.js';
import { toast } from './sheets.js';

const blank = bg => ({ bg: bg || db.library[0]?.src || '', pos: 'top', a: '', b: '', c: '' });

/** Form values → the generic slide schema used by the feed (no templates here). */
function compile(f) {
  return { bg: f.bg, pos: f.pos, texts: [[f.a, 'title'], [f.b, 'label'], [f.c, 'highlight']].filter(x => x[0].trim()).map(([t, style]) => ({ t, style })) };
}

export function renderCreate(view) {
  const d = { slides: [blank()], cur: 0, caption: '', srcTitle: '', srcUrl: '' };
  const pv = h('div', { class: 'pv', role: 'group', 'aria-label': 'Preview' });
  const form = h('div', {});
  const page = h('div', { class: 'page nofuri' }, h('h1', { text: t('cr.title') }), h('div', { class: 'cr' }, pv, form));

  const f = () => d.slides[d.cur];
  const drawPreview = () => { const el = renderSlide(compile(f())); pv.replaceChildren(el); loadImgs(el, true); };
  const field = (label, key, { area, type = 'text', max = 120 } = {}) => {
    const inp = area ? h('textarea', { maxlength: 400 }) : h('input', { type, maxlength: max });
    inp.setAttribute('aria-label', label); inp.value = f()[key]; inp.addEventListener('input', () => { f()[key] = inp.value; drawPreview(); });
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

  const thumbs = h('div', { class: 'thumbs', role: 'group', 'aria-label': t('cr.slides') });
  function drawThumbs() {
    thumbs.replaceChildren(...d.slides.map((s, i) => h('button', { type: 'button', 'aria-pressed': i === d.cur, class: i === d.cur ? 'on' : '', 'aria-label': `${t('cr.slides')} ${i + 1}`, onclick: () => { d.cur = i; drawAll(); } },
      s.bg ? h('img', { src: S.refUrl(s.bg), alt: '' }) : '', h('span', { class: 'n', text: i + 1 }))),
      h('button', { type: 'button', 'aria-label': t('cr.add'), style: { display: 'grid', placeItems: 'center', fontSize: '28px' }, text: '+', onclick: () => { d.slides.push(blank(f().bg)); d.cur = d.slides.length - 1; drawAll(); } }));
  }

  function drawForm() {
    const s = f();
    const sel = h('select', { 'aria-label': t('cr.pos') }, ['top', 'center', 'bottom'].map(k => h('option', { value: k, text: t('cr.' + k), selected: s.pos === k })));
    sel.addEventListener('change', () => { s.pos = sel.value; drawPreview(); });
    const fields = [...field(t('cr.text'), 'a'), ...field(t('cr.text2'), 'b'), ...field(t('cr.text3'), 'c'), h('label', { text: t('cr.pos') }), sel, ...picker('bg', t('cr.bg'))];
    const cap = h('textarea', { maxlength: 300, 'aria-label': t('cr.caption') }); cap.value = d.caption; cap.addEventListener('input', () => { d.caption = cap.value; });
    const st = h('input', { type: 'text', maxlength: 120, 'aria-label': t('cr.sourceTitle') }); st.value = d.srcTitle; st.addEventListener('input', () => { d.srcTitle = st.value; });
    const su = h('input', { type: 'url', maxlength: 400, placeholder: 'https://', 'aria-label': t('cr.source') }); su.value = d.srcUrl; su.addEventListener('input', () => { d.srcUrl = su.value; });
    form.replaceChildren(
      h('label', { text: t('cr.slides') }), thumbs,
      d.slides.length > 1 ? h('button', { class: 'btn ghost sm', type: 'button', text: t('cr.remove'), onclick: () => { d.slides.splice(d.cur, 1); d.cur = Math.max(0, d.cur - 1); drawAll(); } }) : '',
      ...fields,
      h('label', { text: t('cr.caption') }), cap,
      h('label', { text: t('cr.sourceTitle') }), st, h('label', { text: t('cr.source') }), su,
      h('div', { class: 'row2' }, h('button', { class: 'btn', type: 'button', text: t('cr.post'), onclick: post }),
        h('button', { class: 'btn ghost', type: 'button', text: t('cr.download'), onclick: download })));
  }
  function drawAll() { drawThumbs(); drawForm(); drawPreview(); }

  function sources() {
    const out = [];
    if (/^https?:\/\/\S+\.\S+/.test(d.srcUrl.trim())) out.push({ title: d.srcTitle.trim() || d.srcUrl.trim(), url: d.srcUrl.trim() });
    const used = new Set(d.slides.map(s => s.bg));
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
      const el = renderSlide(compile(d.slides[i]));
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
