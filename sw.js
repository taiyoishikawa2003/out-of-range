// Offline support: app shell cached on install; data network-first; media cache-first.
const V = 'oor-v56';
const SHELL = ['./', 'index.html', 'css/app.css', 'js/main.js', 'js/i18n.js', 'js/data.js', 'js/store.js', 'js/render.js', 'js/feed.js', 'js/sheets.js', 'js/pages.js', 'js/create.js', 'js/speech.js', 'js/audio.js', 'js/furi.js', 'js/map.js', 'vendor/idb-keyval.js', 'vendor/html-to-image.js', 'manifest.webmanifest', 'icons/icon-192.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin || e.request.headers.has('range')) return;
  const isMedia = /\.(jpe?g|png|webp|gif|mp4|webm|mp3|m4a|vtt)$/i.test(u.pathname);
  if (isMedia) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { if (res.ok && res.status === 200) { const c = res.clone(); caches.open(V).then(x => x.put(e.request, c)); } return res; })));
  } else {
    // app code and data: always check the server first (no stale JS/JSON after an update)
    const fresh = e.request.mode === 'navigate' ? fetch(e.request) : fetch(e.request.url, { cache: 'no-cache', credentials: 'same-origin' });
    e.respondWith(fresh.then(res => { if (res.ok) { const c = res.clone(); caches.open(V).then(x => x.put(e.request, c)); } return res; }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request))));
  }
});
