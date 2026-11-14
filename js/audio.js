// Web Audio player: unlocked once by a user tap, then music/sfx can play on any later swipe (Safari-safe).
let ctx = null; const bufs = {};
export function unlock() {
  try {
    ctx ||= new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state !== 'running') ctx.resume();
    const s = ctx.createBufferSource(); s.buffer = ctx.createBuffer(1, 1, 22050); s.connect(ctx.destination); s.start(0);
  } catch {}
}
export const ready = () => !!ctx;
const load = url => bufs[url] ||= fetch(url).then(r => r.arrayBuffer()).then(a => new Promise((res, rej) => ctx.decodeAudioData(a, res, rej)));
export function preload(url) { if (ctx && url) load(url).catch(() => {}); }
export function once(url, vol = 1) {
  if (!ctx) return;
  load(url).then(b => { const s = ctx.createBufferSource(); s.buffer = b; const g = ctx.createGain(); g.gain.value = vol; s.connect(g).connect(ctx.destination); s.start(); }).catch(() => {});
}
export function loop(url, vol = 1) {
  if (!ctx) return { stop() {} };
  let src = null, stopped = false; const g = ctx.createGain(); g.gain.value = vol; g.connect(ctx.destination);
  load(url).then(b => { if (stopped) return; src = ctx.createBufferSource(); src.buffer = b; src.loop = true; src.connect(g); src.start(); }).catch(() => {});
  return { stop() { stopped = true; try { g.gain.setTargetAtTime(0, ctx.currentTime, .04); src?.stop(ctx.currentTime + .25); } catch {} } };
}
