// Tiny timeline runtime for motion videos. A page builds its timeline with these helpers;
// tools/motion/build.mjs then steps time frame by frame, records the frames and mixes the sound.
const Q = new URLSearchParams(location.search);
export const LANG = Q.get('lang') || 'ja';
export const A = Q.get('assets') || '/assets';
export const T = (ja, en) => (LANG === 'ja' ? ja : en);
document.documentElement.lang = LANG; document.body.classList.add(LANG);   // set language first, so text is measured with its final line breaks
export const M = { dur: 0, poster: 1, events: [], music: [], ticks: [], anims: [] };
const ms = s => Math.round(s * 1000);
const clamp = x => Math.min(1, Math.max(0, x));
export function an(el, kf, opt) { const a = el.animate(kf, { fill: 'both', easing: 'linear', ...opt }); a.pause(); M.anims.push(a); return a; }
export function el(html, parent) { const d = document.createElement('div'); d.innerHTML = html.trim(); const e = d.firstElementChild; if (parent) parent.append(e); return e; }
export const img = id => `${A}/${id}.jpg`;
export function sfx(t, name, gain = 1) { M.events.push({ t, s: name, g: gain }); }
export function music(src, at, until, o = {}) { M.music.push({ src, at, until, from: 0, gain: 1, fadeIn: 0.05, fadeOut: 0.3, ...o }); }
/** Show an element only inside [start, end). */
export function win(e, start, end, fade = 0) {
  const D = M.dur, o = x => clamp(x / D);
  an(e, [{ opacity: 0, offset: 0 }, { opacity: 0, offset: o(start) }, { opacity: 1, offset: o(Math.min(start + fade, end)) }, { opacity: 1, offset: o(Math.max(end - fade, start)) }, { opacity: 0, offset: o(end) }, { opacity: 0, offset: 1 }], { duration: ms(D) });
}
/** Pop an element in at time `at` (stays visible afterwards). */
export function pop(e, at, { dur = 0.26, from = 'scale(.55)', snd = 'pop', gain = 1, to = 'none' } = {}) {
  an(e, [{ opacity: 0, transform: from }, { opacity: 1, transform: to === 'none' ? 'scale(1.07)' : to + ' scale(1.07)', offset: 0.65 }, { opacity: 1, transform: to }], { duration: ms(dur), delay: ms(at), easing: 'ease-out' });
  if (snd) sfx(at, snd, gain);
}
export function fadeIn(e, at, dur = 0.4) { an(e, [{ opacity: 0 }, { opacity: 1 }], { duration: ms(dur), delay: ms(at) }); }
export function slideIn(e, at, { dur = 0.35, from = 'translateY(140px)', snd = null } = {}) {
  an(e, [{ opacity: 0, transform: from }, { opacity: 1, transform: 'none' }], { duration: ms(dur), delay: ms(at), easing: 'cubic-bezier(.2,.9,.3,1)' }); if (snd) sfx(at, snd);
}
/** Slow camera move on a photo between two times. */
export function kb(e, start, end, { s0 = 1.02, s1 = 1.14, x0 = 0, y0 = 0, x1 = 0, y1 = 0 } = {}) {
  an(e, [{ transform: `translate(${x0}px,${y0}px) scale(${s0})` }, { transform: `translate(${x1}px,${y1}px) scale(${s1})` }], { duration: ms(end - start), delay: ms(start) });
}
/** Short emphasis: the element jumps bigger and settles. */
export function punch(e, at, { scale = 1.16, dur = 0.32 } = {}) { an(e, [{ transform: `scale(${scale})` }, { transform: 'scale(1)' }], { duration: ms(dur), delay: ms(at), easing: 'ease-out', fill: 'none' }); }
export function shake(e, at, dur = 0.4, amp = 14) {
  const kf = []; const n = 8; for (let i = 0; i <= n; i++) { const k = 1 - i / n; kf.push({ transform: `translate(${(i % 2 ? 1 : -1) * amp * k}px,${(i % 3 ? -1 : 1) * amp * 0.6 * k}px)` }); }
  an(e, kf, { duration: ms(dur), delay: ms(at), fill: 'none' });
}
/** Count a number up (JS-driven so it can be formatted). */
export function count(e, at, dur, from, to, fmt = v => Math.round(v), { snd = 'tick', every = 0.07 } = {}) {
  M.ticks.push(t => { const u = clamp((t - at) / dur); e.textContent = fmt(from + (to - from) * (1 - Math.pow(1 - u, 3))); });
  if (snd) for (let x = at; x < at + dur; x += every) sfx(x, snd, 0.5);
}
/** Type text letter by letter. */
export function type(e, at, text, cps = 14, snd = 'tick') {
  const chars = [...text]; M.ticks.push(t => { e.textContent = chars.slice(0, Math.max(0, Math.floor((t - at) * cps))).join(''); });
  if (snd) chars.forEach((_, i) => sfx(at + i / cps, snd, 0.45)); return at + chars.length / cps;
}
export function done() {
  window.__motion = { dur: M.dur, poster: M.poster, events: M.events, music: M.music };
  window.__seek = t => { const x = t * 1000; for (const a of M.anims) a.currentTime = x; for (const f of M.ticks) f(t); };
  window.__seek(Number(Q.get('t') || 0)); window.__ready = true;
}
/** A full-screen photo scene with a text column; returns its parts. */
export function scene(stage, s, e, { bg, pos = '50% 50%', filt = 'none', shade = 'top', move = {}, cr = '', colCls = '', colStyle = '' } = {}) {
  const sc = el('<div class="sc"></div>', stage);
  const im = bg ? el(`<img class="bg" src="${img(bg)}" style="object-position:${pos};filter:${filt}">`, sc) : null;
  if (shade) el(`<div class="shade ${shade}"></div>`, sc);
  const col = el(`<div class="col ${colCls}" style="${colStyle}"></div>`, sc);
  if (cr) el(`<div class="cr">${cr}</div>`, sc);
  win(sc, s, e); if (im) kb(im, s, e, move); return { sc, col, im };
}
/** Add a text block to a column and pop it in at `at`. */
export function add(col, html, at, opt) { const w = el(`<div class="wrap">${html}</div>`, col); pop(w, at, opt); return w; }
export const tag = (t, cls = '') => `<div class="tag ${cls}">${t}</div>`;
export const h = (t, cls = '') => `<div class="h ${cls}">${t}</div>`;
export const bx = (t, cls = '') => `<div class="bxw"><span class="bx ${cls}">${t}</span></div>`;
/** A quick white flash on a cut. */
export function flash(parent, at, dur = 0.28, peak = 0.75) { const f = el('<div class="flash"></div>', parent); an(f, [{ opacity: peak }, { opacity: 0 }], { duration: ms(dur), delay: ms(at), easing: 'ease-out', fill: 'none' }); return f; }
/** Auto-playing chat: messages arrive one by one, with a typing indicator for incoming ones. Call build() after adding all messages. */
export function chat(stage, start, end, { title, sub = '', avatar = '🌍' } = {}) {
  const root = el('<div class="sc chat2"></div>', stage); win(root, start, end);
  el(`<div class="chbar"><div class="av">${avatar}</div><div>${title}<small>${sub}</small></div></div>`, root);
  const view = el('<div class="view"></div>', root), list = el('<div class="list"></div>', view), items = [];
  const push = (html, at, o = {}) => { const e = el(html, list); items.push({ e, at, ...o }); return e; };
  const api = {
    root, list,
    who: (at, name, side = 'l') => push(`<div class="who ${side === 'r' ? 'r' : ''}">${name}</div>`, at, { quiet: true }),
    L: (at, html, cls = '', ty = 0.75) => push(`<div class="m l ${cls}">${html}</div>`, at, { ty, snd: 'msg' }),
    R: (at, html, cls = '', snd = 'send') => push(`<div class="m r ${cls}">${html}</div>`, at, { snd }),
    sep: (at, text) => push(`<div class="daysep">${text}</div>`, at, { quiet: true }),
    build() {
      const VH = view.clientHeight, ev = [];
      for (const it of items) {
        const top = it.e.offsetTop, bottom = top + it.e.offsetHeight;
        if (it.ty) {
          const tp = el('<div class="typing" style="position:absolute;left:0"><i></i><i></i><i></i></div>', list); tp.style.top = top + 'px';
          win(tp, it.at - it.ty, it.at); [...tp.children].forEach((d, i) => an(d, [{ opacity: 0.3 }, { opacity: 1 }, { opacity: 0.3 }], { duration: 600, iterations: Infinity, delay: i * 150 }));
          ev.push({ t: it.at - it.ty, bottom: top + 84 });
        }
        if (it.quiet) an(it.e, [{ opacity: 0 }, { opacity: 1 }], { duration: 120, delay: ms(it.at) });
        else pop(it.e, it.at, { snd: it.snd, dur: 0.22, from: `translateY(26px) scale(.9)` });
        ev.push({ t: it.at, bottom });
      }
      ev.sort((a, b) => a.t - b.t); let y = 0; for (const e of ev) { y = Math.min(y, VH - 30 - e.bottom); e.y = y; }
      M.ticks.push(t => { let prev = 0, cur = 0; for (const e of ev) { if (e.t <= t) { const u = clamp((t - e.t) / 0.28); cur = prev + (e.y - prev) * (1 - Math.pow(1 - u, 3)); prev = e.y; } else break; } list.style.transform = `translateY(${cur}px)`; });
    }
  };
  return api;
}
