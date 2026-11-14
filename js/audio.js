// Background music for photo posts. One shared <audio> element is "unlocked" by the first tap,
// then reused for every post: it keeps playing on later swipes (Safari) and ignores the iPhone silent switch
// (Web Audio would be muted by it).
let el = null;
export function unlock() {
  try {
    if (!el) { el = new Audio(); el.loop = true; el.preload = 'auto'; el.setAttribute('playsinline', ''); }
    if (!el.src) { el.src = 'media/silence.mp3'; }
    el.play().catch(() => {});
  } catch {}
}
export const ready = () => !!el;
export function preload() {}
export function once(url) { try { const a = new Audio(url); a.play().catch(() => {}); } catch {} }
export function loop(url) {
  if (!el) return { stop() {} };
  const abs = new URL(url, location.href).href;
  if (el.src !== abs) { el.src = abs; }
  el.currentTime = 0; el.loop = true;
  el.play().catch(() => {});
  return { stop() { if (el.src === abs) el.pause(); } };
}
