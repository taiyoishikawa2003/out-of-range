import * as AU from './audio.js';
import { applyStatic, setLang, getLang, onLang } from './i18n.js';
import { loadData } from './data.js';
import { renderFeed } from './feed.js';
import { renderDiscover, renderProfile, renderMe, renderAbout } from './pages.js';
import { renderCreate } from './create.js';
import { renderMap } from './map.js';
import { closeSheet } from './sheets.js';

const view = document.getElementById('view');
let destroy = null;

function route() {
  closeSheet();
  destroy?.(); destroy = null;
  const [, a = '', b = ''] = (location.hash || '#/').split('/');
  const nav = { '': 'feed', p: 'feed', discover: 'discover', create: 'create', me: 'me', u: 'discover', about: 'about', map: 'discover' }[a] || 'feed';
  document.querySelectorAll('[data-nav]').forEach(n => { const on = n.dataset.nav === nav; n.classList.toggle('on', on); if (on) n.setAttribute('aria-current', 'page'); else n.removeAttribute('aria-current'); });
  const id = decodeURIComponent(b);
  switch (a) {
    case 'p': destroy = renderFeed(view, { startId: id }); break;
    case 'discover': renderDiscover(view, id); break;
    case 'u': renderProfile(view, id); break;
    case 'me': renderMe(view); break;
    case 'create': renderCreate(view); break;
    case 'about': renderAbout(view); break;
    case 'map': renderMap(view, id); break;
    default: destroy = renderFeed(view);
  }
  if (a !== '' && a !== 'p') view.focus({ preventScroll: true });
}

document.addEventListener('click', e => {
  if (e.target.closest('[data-action="lang"]')) setLang(getLang() === 'ja' ? 'en' : 'ja');
});
onLang(() => route());
// any first tap/key also unlocks Web Audio
['pointerdown', 'keydown'].forEach(ev => addEventListener(ev, () => AU.unlock(), { once: true, capture: true }));

(async () => {
  applyStatic();
  try { await loadData(); }
  catch (e) { view.textContent = 'Could not load data. ' + e.message; return; }
  window.addEventListener('hashchange', route);
  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => {});
  route();
})();
