import { h, icon, img, loadImgs, renderSlide, slideText } from './render.js';
import { t, L, getLang } from './i18n.js';
import * as S from './store.js';
import { account, allPosts } from './data.js';
import { openComments, openSources, openShare, toast, fmt, sheetOpen } from './sheets.js';
import { speak, stopSpeak } from './speech.js';

/* ---------- WebVTT (minimal parser for captions) ---------- */
const vttCache = new Map();
async function loadVtt(url) {
  if (!url) return [];
  if (vttCache.has(url)) return vttCache.get(url);
  const p = fetch(url).then(r => r.ok ? r.text() : '').then(txt => {
    const ts = s => { const m = s.trim().split(':').map(parseFloat); return m.length === 3 ? m[0] * 3600 + m[1] * 60 + m[2] : m[0] * 60 + m[1]; };
    return txt.replace(/\r/g, '').split('\n\n').map(b => {
      const lines = b.split('\n'); const i = lines.findIndex(l => l.includes('-->'));
      if (i < 0) return null; const [a, z] = lines[i].split('-->');
      return { start: ts(a), end: ts(z.split(' ').filter(Boolean)[0]), text: lines.slice(i + 1).join('\n') };
    }).filter(Boolean);
  }).catch(() => []);
  vttCache.set(url, p); return p;
}

export function renderFeed(view, { startId, tab = 'foryou' } = {}) {
  const wrap = h('div', { class: 'feedwrap' });
  const feed = h('div', { class: 'feed', role: 'feed', 'aria-label': 'Posts' });
  let posts = tab === 'following' ? allPosts().filter(p => S.isFollowing(p.account)) : allPosts();
  const items = []; // {post, el, api}
  let active = -1, cleanup = [];

  /* top bar */
  const tabBtn = (k, label) => h('button', { class: 'tab' + (tab === k ? ' on' : ''), type: 'button', text: t(label), onclick: () => { if (tab !== k) { destroy(); renderFeed(view, { tab: k }); } } });
  const muteBtn = h('button', { class: 'iconbtn', type: 'button', onclick: () => setMuted(!S.isMuted()) });
  const readBtn = h('button', { class: 'iconbtn', type: 'button', onclick: () => {
    S.setRead(!S.isRead()); drawTop(); toast(t(S.isRead() ? 'read.on' : 'read.off'));
    if (S.isRead()) readCurrent(); else stopSpeak();
  } }, icon('speak'));
  const drawTop = () => {
    muteBtn.replaceChildren(icon(S.isMuted() ? 'mute' : 'sound')); muteBtn.setAttribute('aria-label', t(S.isMuted() ? 'sound.off' : 'sound.on'));
    readBtn.classList.toggle('on', S.isRead()); readBtn.setAttribute('aria-label', t('read')); readBtn.setAttribute('aria-pressed', S.isRead());
  };
  drawTop();
  const top = h('div', { class: 'feedtop' }, h('div', { class: 'tl' }, muteBtn, readBtn), tabBtn('following', 'feed.following'), tabBtn('foryou', 'feed.foryou'),
    h('div', { class: 'tr' }, h('button', { class: 'iconbtn', type: 'button', 'data-action': 'lang', 'aria-label': t('lang'), style: { fontWeight: 800, fontSize: '13px' }, text: t('lang.short') }), h('a',{ class: 'iconbtn', href: '#/discover', 'aria-label': t('nav.discover') }, icon('search'))));

  function setMuted(m) {
    S.setMuted(m); drawTop();
    items.forEach(it => it.api?.applyMute?.());
  }

  /* posts */
  posts.forEach((p, i) => {
    const el = h('article', { class: 'post', 'data-id': p.id, 'aria-posinset': i + 1, 'aria-setsize': posts.length, 'aria-label': `@${p.account}: ${L(p.caption)}` });
    feed.append(el); items.push({ post: p, el, api: null, built: false });
  });
  if (!posts.length) feed.append(h('div', { class: 'feed-end' }, h('p', { text: t('feed.followEmpty') }), h('button', { class: 'btn', type: 'button', text: t('feed.foryou'), onclick: () => { destroy(); renderFeed(view, { tab: 'foryou' }); } })));
  else feed.append(h('section', { class: 'feed-end', 'aria-label': t('feed.end.title') }, h('h2', { text: t('feed.end.title') }), h('p', { text: t('feed.end.text') }),
    h('button', { class: 'btn', type: 'button', text: t('feed.replay'), onclick: () => go(0, 'auto') }),
    h('a', { class: 'btn ghost', href: '#/create', text: t('feed.makeOwn') })));

  function build(i) {
    const it = items[i]; if (!it || it.built) return;
    it.built = true; it.api = buildPost(it.post, it.el, { setMuted, onSlide: () => i === active && readCurrent() });
  }

  function setActive(i) {
    if (i === active) return;
    const prev = items[active]; active = i;
    prev?.api?.deactivate();
    for (let j = i - 1; j <= i + 2; j++) build(j);
    items.forEach((it, j) => { if (it.built && Math.abs(j - i) > 3) it.api.unload(); });
    items[i]?.api?.activate();
    items[i + 1]?.api?.preload(); items[i + 2]?.api?.preloadLight?.();
    const id = items[i]?.post.id; if (id) history.replaceState(null, '', '#/p/' + encodeURIComponent(id));
    readCurrent();
  }
  function readCurrent() {
    if (!S.isRead()) return;
    const it = items[active]; if (!it || it.post.type === 'video') { stopSpeak(); return; }
    speak(it.api.currentText(), getLang());
  }

  const io = new IntersectionObserver(es => {
    es.forEach(e => {
      if (e.isIntersecting && e.intersectionRatio >= .6) {
        const i = items.findIndex(x => x.el === e.target);
        if (i >= 0) setActive(i);
      }
      if (e.target.classList.contains('feed-end') && e.isIntersecting && e.intersectionRatio >= .6) { items[active]?.api?.deactivate(); active = -1; stopSpeak(); }
    });
  }, { root: feed, threshold: [.6] });
  items.forEach(it => io.observe(it.el));
  feed.querySelectorAll('.feed-end').forEach(e => io.observe(e));

  const go = (i, behavior = 'smooth') => { i = Math.max(0, Math.min(i, items.length)); feed.children[i]?.scrollIntoView({ behavior, block: 'start' }); };
  const cur = () => Math.round(feed.scrollTop / feed.clientHeight);

  /* keyboard */
  const onKey = e => {
    if (sheetOpen() || e.target.closest?.('input,textarea')) return;
    const k = e.key;
    if (k === 'ArrowDown' || k === 'j' || k === 'PageDown') { e.preventDefault(); go(cur() + 1); }
    else if (k === 'ArrowUp' || k === 'k' || k === 'PageUp') { e.preventDefault(); go(cur() - 1); }
    else if (k === ' ') { e.preventDefault(); items[active]?.api?.togglePlay(); }
    else if (k === 'm') setMuted(!S.isMuted());
    else if (k === 'l') items[active]?.api?.like(true);
    else if (k === 'ArrowRight') items[active]?.api?.slide(1);
    else if (k === 'ArrowLeft') items[active]?.api?.slide(-1);
  };
  document.addEventListener('keydown', onKey);
  // mouse wheel / trackpad: exactly one post per gesture (native snapping can skip several)
  let wAcc = 0, wLock = 0, wIdle;
  feed.addEventListener('wheel', e => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY) || e.ctrlKey) return;
    e.preventDefault();
    clearTimeout(wIdle); wIdle = setTimeout(() => { wAcc = 0; }, 180);
    if (Date.now() < wLock) return;
    wAcc += e.deltaY;
    if (Math.abs(wAcc) > 30) { go(cur() + Math.sign(wAcc)); wAcc = 0; wLock = Date.now() + 650; }
  }, { passive: false });
  const onVis = () => { if (document.hidden) items[active]?.api?.deactivate(); else items[active]?.api?.activate(); };
  document.addEventListener('visibilitychange', onVis);

  const arrows = h('div', { class: 'feedarrows' },
    h('button', { type: 'button', 'aria-label': 'Previous', onclick: () => go(cur() - 1) }, icon('up')),
    h('button', { type: 'button', 'aria-label': 'Next', onclick: () => go(cur() + 1) }, icon('down')));

  wrap.append(feed); view.replaceChildren(wrap, top, arrows);
  // first paint: build the first posts right away so the first frame is never empty
  let si = startId ? Math.max(0, items.findIndex(x => x.post.id === startId)) : 0;
  for (let j = si - 1; j <= si + 2; j++) build(j);
  if (si > 0) requestAnimationFrame(() => { feed.scrollTop = si * feed.clientHeight; });

  function destroy() {
    io.disconnect(); document.removeEventListener('keydown', onKey); document.removeEventListener('visibilitychange', onVis);
    items.forEach(it => it.built && it.api.unload()); stopSpeak(); cleanup.forEach(f => f());
  }
  return destroy;
}

/* ---------- one post ---------- */
function buildPost(p, el, { setMuted, onSlide }) {
  const stage = h('div', { class: 'stage' });
  let media = null; // {activate, deactivate, preload, unload, togglePlay, applyMute, slide, currentText}
  if (p.type === 'video') media = videoPost(p, el, stage, setMuted);
  else media = carouselPost(p, el, stage, onSlide);

  /* rail */
  const acc = account(p.account);
  const fol = h('button', { class: 'fol', type: 'button' });
  const drawFol = () => { const on = S.isFollowing(p.account); fol.textContent = on ? '✓' : '+'; fol.classList.toggle('on', on); fol.setAttribute('aria-label', `${t(on ? 'following' : 'follow')} @${p.account}`); };
  fol.addEventListener('click', e => { e.stopPropagation(); const on = S.toggleFollow(p.account); drawFol(); toast(t(on ? 'followed' : 'unfollowed')); });
  drawFol();
  const av = h('div', { class: 'avatar' }, h('a', { href: '#/u/' + p.account, 'aria-label': '@' + p.account },
    acc.avatar ? img(acc.avatar, '', '') : h('div', { class: 'ph', text: (L(acc.name) || p.account)[0] })), p.mine ? null : fol);

  const base = p.stats || {};
  const likeBtn = h('button', { class: 'rb like', type: 'button' });
  const cmBtn = h('button', { class: 'rb', type: 'button', onclick: e => { e.stopPropagation(); openComments(p, drawCounts); } });
  const saveBtn = h('button', { class: 'rb save', type: 'button' });
  const drawCounts = () => {
    const lk = S.isLiked(p.id), sv = S.isSaved(p.id);
    likeBtn.replaceChildren(icon('heart'), fmt((base.likes || 0) + (lk ? 1 : 0))); likeBtn.classList.toggle('on', lk); likeBtn.setAttribute('aria-pressed', lk); likeBtn.setAttribute('aria-label', t('like'));
    const nc = (p.comments?.length || 0) + S.localComments(p.id).length + (base.comments || 0);
    cmBtn.replaceChildren(icon('comment'), fmt(nc)); cmBtn.setAttribute('aria-label', t('comments'));
    saveBtn.replaceChildren(icon('save'), fmt((base.saves || 0) + (sv ? 1 : 0))); saveBtn.classList.toggle('on', sv); saveBtn.setAttribute('aria-pressed', sv); saveBtn.setAttribute('aria-label', t('save'));
  };
  drawCounts();
  const pop = b => { b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); };
  const like = force => { const on = S.toggleLike(p.id, force); drawCounts(); if (on) pop(likeBtn); return on; };
  likeBtn.addEventListener('click', e => { e.stopPropagation(); like(); });
  saveBtn.addEventListener('click', e => { e.stopPropagation(); const on = S.toggleSave(p.id); drawCounts(); if (on) pop(saveBtn); toast(t(on ? 'saved' : 'unsaved')); });
  const rail = h('div', { class: 'rail' }, av, likeBtn, cmBtn, saveBtn,
    h('button', { class: 'rb', type: 'button', 'aria-label': t('share'), onclick: e => { e.stopPropagation(); openShare(p); } }, icon('share'), t('share')),
    (p.sources?.length) ? h('button', { class: 'rb', type: 'button', 'aria-label': t('sources'), onclick: e => { e.stopPropagation(); openSources(p); } }, icon('doc'), t('sources')) : null,
    h('div', { class: 'disc', 'aria-hidden': 'true' }));

  /* meta */
  const cap = h('p', { class: 'cap' }, L(p.caption), ' ', (p.tags || []).map(x => '#' + x).join(' '));
  const more = h('button', { class: 'more', type: 'button', text: t('more'), onclick: e => { e.stopPropagation(); const o = cap.classList.toggle('open'); more.textContent = t(o ? 'less' : 'more'); } });
  if ((L(p.caption) + (p.tags || []).join(' ')).length < 38) more.hidden = true;
  const meta = h('div', { class: 'meta' }, h('a', { class: 'who', href: '#/u/' + p.account, text: '@' + p.account }), cap, more,
    h('div', { class: 'snd' }, icon('music'), h('span', { text: L(p.sound) || 'Original sound - OUT OF RANGE' })));

  /* gestures: tap = play/pause (or unmute), double tap = like, long press = 2x speed (video) */
  let lastTap = 0, tapTimer, down = null, lpTimer, longPressed = false;
  stage.addEventListener('pointerdown', e => {
    down = { x: e.clientX, y: e.clientY }; longPressed = false;
    clearTimeout(lpTimer);
    if (media.setRate && !e.target.closest('button,a,input')) lpTimer = setTimeout(() => { longPressed = true; media.setRate(2); }, 450);
  });
  const endPress = () => { clearTimeout(lpTimer); if (longPressed) media.setRate(1); };
  stage.addEventListener('pointercancel', () => { endPress(); down = null; });
  stage.addEventListener('pointermove', e => { if (down && Math.hypot(e.clientX - down.x, e.clientY - down.y) > 10) { clearTimeout(lpTimer); } });
  stage.addEventListener('pointerup', e => {
    endPress();
    if (longPressed || !down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 10) return;
    if (e.target.closest('button,a,input,.progress')) return;
    const now = Date.now();
    if (now - lastTap < 300) {
      clearTimeout(tapTimer); lastTap = 0; like(true);
      const r = el.getBoundingClientRect();
      const ht = icon('heart'); ht.classList.add('heart'); ht.style.left = (e.clientX - r.left) + 'px'; ht.style.top = (e.clientY - r.top) + 'px';
      el.append(ht); setTimeout(() => ht.remove(), 850);
    } else {
      lastTap = now;
      tapTimer = setTimeout(() => media.togglePlay?.(), 280);
    }
  });
  stage.addEventListener('contextmenu', e => e.preventDefault());

  el.replaceChildren(stage, rail, meta, ...(media.extra || []).filter(Boolean));
  return { ...media, like };
}

function videoPost(p, el, stage, setMuted) {
  const v = h('video', { playsinline: true, 'webkit-playsinline': true, loop: true, preload: 'none', poster: L(p.video.poster), muted: true, 'aria-label': L(p.caption) });
  v.muted = true;
  if (p.video.fit === 'contain') el.classList.add('contain');
  const capBox = h('div', { class: 'captions', 'aria-hidden': 'true' });
  const playI = h('div', { class: 'playicon' }, icon('play'));
  const bar = h('b'); const prog = h('div', { class: 'progress', role: 'slider', 'aria-label': 'Seek', tabindex: '0', 'aria-valuemin': 0, 'aria-valuemax': 100 }, h('i', {}, bar));
  const unmute = h('button', { class: 'unmute', type: 'button', hidden: true, onclick: e => { e.stopPropagation(); setMuted(false); } }, icon('mute'), t('tap.unmute'));
  const spin = h('div', { class: 'spinner', 'aria-hidden': 'true' });
  const rate = h('div', { class: 'pill ratebadge', hidden: true, text: '2x ▶▶' });
  const errBox = h('div', { class: 'verr', hidden: true, text: t('err.video') });
  const tlabel = h('div', { class: 'seektime', hidden: true });
  const cc = p.video.captions ? h('button', { class: 'pill ccbtn', type: 'button', text: 'CC' }) : null;
  const drawCC = () => { if (cc) { cc.classList.toggle('off', !S.isCC()); cc.setAttribute('aria-pressed', S.isCC()); cc.setAttribute('aria-label', t('cc')); } };
  cc?.addEventListener('click', e => { e.stopPropagation(); S.setCC(!S.isCC()); drawCC(); toast(t(S.isCC() ? 'cc.on' : 'cc.off')); });
  drawCC();
  stage.append(v, capBox, playI, spin, rate, errBox, tlabel);
  v.addEventListener('waiting', () => el.classList.add('buffering'));
  ['playing', 'canplay', 'pause'].forEach(ev => v.addEventListener(ev, () => el.classList.remove('buffering')));
  v.addEventListener('error', () => { el.classList.remove('buffering'); if (loaded) errBox.hidden = false; });
  const mmss = x => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, '0')}`;
  let loaded = false, isActive = false, cues = [], wantPlay = false;
  const loadCues = async () => { cues = await loadVtt(p.video.captions?.[getLang()] || p.video.captions?.en); };
  const src = () => { if (!loaded) { v.src = L(p.video.src); loaded = true; loadCues(); } };
  const applyMute = () => { v.muted = S.isMuted(); unmute.hidden = !S.isMuted() || !isActive; };
  const play = () => { src(); wantPlay = true; v.play().then(() => { el.classList.add('playing'); el.classList.remove('paused'); }).catch(() => {
    // autoplay with sound blocked → fall back to muted
    if (!v.muted) { S.setMuted(true); v.muted = true; applyMute(); v.play().catch(() => el.classList.add('paused')); } else el.classList.add('paused');
  }); };
  const pause = () => { wantPlay = false; v.pause(); el.classList.remove('playing'); };
  let raf;
  const tick = () => {
    if (v.duration) { const pc = v.currentTime / v.duration * 100; bar.style.width = pc + '%'; prog.setAttribute('aria-valuenow', Math.round(pc)); }
    const c = cues.find(c => v.currentTime >= c.start && v.currentTime <= c.end);
    const txt = c ? c.text : '';
    if (!S.isCC()) { if (capBox.dataset.t) { capBox.dataset.t = ''; capBox.replaceChildren(); } }
    else if (capBox.dataset.t !== txt) { capBox.dataset.t = txt; capBox.replaceChildren(txt ? h('span', { text: txt }) : ''); }
    raf = requestAnimationFrame(tick);
  };
  // scrub
  const seekTo = x => { const r = prog.getBoundingClientRect(); if (v.duration) { v.currentTime = Math.max(0, Math.min(1, (x - r.left) / r.width)) * v.duration; tlabel.hidden = false; tlabel.textContent = `${mmss(v.currentTime)} / ${mmss(v.duration)}`; } };
  prog.addEventListener('pointerdown', e => { e.stopPropagation(); prog.setPointerCapture(e.pointerId); prog.classList.add('drag'); seekTo(e.clientX); });
  prog.addEventListener('pointermove', e => { if (prog.classList.contains('drag')) seekTo(e.clientX); });
  prog.addEventListener('pointerup', () => { prog.classList.remove('drag'); setTimeout(() => { tlabel.hidden = true; }, 600); });
  prog.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { v.currentTime += 2; e.stopPropagation(); } if (e.key === 'ArrowLeft') { v.currentTime -= 2; e.stopPropagation(); } });
  return {
    extra: [prog, unmute, cc],
    activate() { isActive = true; applyMute(); play(); cancelAnimationFrame(raf); tick(); },
    deactivate() { isActive = false; pause(); unmute.hidden = true; cancelAnimationFrame(raf); },
    preload() { if (!loaded) { v.preload = 'auto'; src(); } },
    preloadLight() { if (!loaded) { v.preload = 'metadata'; src(); } },
    setRate(r) { v.playbackRate = r; rate.hidden = r === 1; if (r !== 1) unmute.hidden = true; else applyMute(); },
    applyCC: drawCC,
    unload() { pause(); cancelAnimationFrame(raf); if (loaded) { v.removeAttribute('src'); v.load(); loaded = false; } },
    togglePlay() { if (v.paused) { play(); } else if (S.isMuted()) { setMuted(false); } else { pause(); el.classList.add('paused'); } },
    applyMute, slide() {}, currentText: () => L(p.caption)
  };
}

function carouselPost(p, el, stage, onSlide) {
  const slides = [...(p.slides || [])];
  if (p.sources?.length) slides.push({ layout: 'sources' });
  const car = h('div', { class: 'car', 'aria-roledescription': 'carousel' });
  slides.forEach(s => car.append(renderSlide(s, { post: p })));
  stage.append(car);
  const dots = h('div', { class: 'dots', 'aria-hidden': 'true' }, slides.map(() => h('i')));
  const counter = h('span', { class: 'pill counter', 'aria-live': 'polite' });
  const prev = h('button', { class: 'carnav prev', type: 'button', 'aria-label': 'Previous slide', onclick: e => { e.stopPropagation(); go(idx - 1); } }, icon('left'));
  const next = h('button', { class: 'carnav next', type: 'button', 'aria-label': 'Next slide', onclick: e => { e.stopPropagation(); go(idx + 1); } }, icon('right'));
  let idx = 0, loaded = false;
  const audio = p.audio ? h('audio', { src: p.audio, loop: true, preload: 'none' }) : null;
  const draw = () => {
    [...dots.children].forEach((d, i) => d.classList.toggle('on', i === idx));
    counter.textContent = `${idx + 1}/${slides.length}`;
    prev.hidden = idx === 0; next.hidden = idx === slides.length - 1;
  };
  const go = i => { i = Math.max(0, Math.min(slides.length - 1, i)); car.scrollTo({ left: i * car.clientWidth, behavior: 'smooth' }); };
  let st;
  car.addEventListener('scroll', () => {
    clearTimeout(st); st = setTimeout(() => {
      const i = Math.round(car.scrollLeft / car.clientWidth);
      if (i !== idx) { idx = i; draw(); onSlide(); }
    }, 60);
  }, { passive: true });
  draw();
  const load = () => { if (!loaded) { loadImgs(car); loaded = true; } };
  return {
    extra: [dots, counter, prev, next],
    activate() { load(); el.classList.add('playing'); if (audio && !S.isMuted()) audio.play().catch(() => {}); },
    deactivate() { el.classList.remove('playing'); audio?.pause(); },
    preload: load, preloadLight() { const i = car.querySelector('img[data-src]'); if (i) { i.src = i.dataset.src; i.removeAttribute('data-src'); } },
    unload() { audio?.pause(); },
    togglePlay() { if (audio) { if (audio.paused && !S.isMuted()) audio.play().catch(() => {}); else audio.pause(); } },
    applyMute() { if (!audio) return; if (S.isMuted()) audio.pause(); else if (el.classList.contains('playing')) audio.play().catch(() => {}); },
    slide: d => go(idx + d),
    currentText: () => slides[idx].layout === 'sources' ? t('true') : slideText(slides[idx])
  };
}
