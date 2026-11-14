// "Where are they now?" An interactive map of the Moon and Mars with the machines NASA left there.
// Positions come from NASA's NSSDCA catalogue and mission pages (see data/machines.json for the source of each entry).
import { h } from './render.js';
import { L, getLang, t } from './i18n.js';

const TX = {
  ja: { title: '今どこにいる？マップ', lead: 'NASAが置いてきた機械は、今もそこにあります。ピンを押すと、その機械の話が出ます。', moon: '月', mars: '火星', deep: 'もっと遠く',
    what: 'どんな機械？ なぜ送った？', found: 'わかったこと', now: '今は', posts: 'この機械の投稿を見る', lost: '遺失物センターで見る', src: '出典', used: '今も使われている', silent: '通信は終わった', approx: 'おおよその位置',
    mapBy: '地図', coords: '位置は NASA の資料（NSSDCA など）の緯度・経度によります。', deepNote: 'ここから先は、地図にのらない場所にいる機械です。', landed: '年' },
  en: { title: 'Where are they now?', lead: 'The machines NASA left behind are still out there. Tap a pin to hear its story.', moon: 'Moon', mars: 'Mars', deep: 'Farther out',
    what: 'What is it? Why was it sent?', found: 'What we learned', now: 'Now', posts: 'See this machine’s posts', lost: 'See it at the Lost & Found', src: 'Sources', used: 'Still in use', silent: 'No longer in contact', approx: 'Approximate position',
    mapBy: 'Map', coords: 'Positions use latitudes and longitudes from NASA sources (NSSDCA and mission pages).', deepNote: 'These machines are in places a map cannot show.', landed: '' }
};

export async function renderMap(view, tab = 'moon') {
  const X = TX[getLang()] || TX.en;
  let data = { maps: {}, machines: [] };
  try { data = await fetch('data/machines.json', { cache: 'no-cache' }).then(r => r.json()); } catch {}
  if (!['moon', 'mars', 'deep'].includes(tab)) tab = 'moon';
  let sel = null;
  const mapBox = h('div', { class: 'mapbox' }), list = h('div', { class: 'maplist' }), note = h('p', { class: 'hint' });
  const chips = h('div', { class: 'chips', role: 'tablist' });
  const page = h('div', { class: 'page mappage' },
    h('div', { class: 'backbar', style: { justifyContent: 'space-between' } }, h('h1', { style: { margin: 0 }, text: X.title }), h('button', { class: 'btn ghost sm', type: 'button', 'data-action': 'lang', text: t('lang') })),
    h('p', { class: 'maplead', text: X.lead }), chips, mapBox, note, list);

  const card = (m, n) => {
    const links = [];
    if (m.link) links.push(h('a', { class: 'btn sm', href: m.link, text: m.link.startsWith('lost') ? X.lost : X.posts }));
    const c = h('article', { class: 'mcard', id: 'm-' + m.id, tabindex: '0' },
      h('div', { class: 'mhead' }, n ? h('span', { class: 'mnum', text: n }) : '', h('h2', { text: L(m.name) }),
        h('span', { class: 'mchip ' + m.status, text: m.status === 'used' ? X.used : X.silent })),
      m.img ? h('img', { class: 'mimg', src: m.img, alt: '', loading: 'lazy' }) : '',
      h('h3', { text: X.what }), h('p', { text: L(m.what) }),
      h('h3', { text: X.found }), h('p', { text: L(m.found) }),
      h('h3', { text: X.now }), h('p', { text: L(m.now) }),
      links.length ? h('p', {}, links) : '',
      h('p', { class: 'msrc' }, X.src + ': ', (m.src || []).flatMap((s, i) => [i ? ' / ' : '', h('a', { href: s.url, target: '_blank', rel: 'noopener', text: s.title })])));
    c.addEventListener('click', e => { if (!e.target.closest('a')) pick(m.id, false); });
    return c;
  };
  function pick(id, scroll = true) {
    sel = id;
    mapBox.querySelectorAll('.pin').forEach(p => p.classList.toggle('on', p.dataset.id === id));
    list.querySelectorAll('.mcard').forEach(c => c.classList.toggle('on', c.id === 'm-' + id));
    if (scroll) document.getElementById('m-' + id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function draw() {
    chips.replaceChildren(...['moon', 'mars', 'deep'].map(k => h('button', { class: 'chip' + (tab === k ? ' on' : ''), type: 'button', role: 'tab', 'aria-selected': tab === k, text: X[k], onclick: () => { tab = k; sel = null; history.replaceState(null, '', '#/map/' + k); draw(); } })));
    const ms = data.machines.filter(m => m.body === tab), mp = data.maps[tab];
    mapBox.replaceChildren(); mapBox.hidden = !mp;
    if (mp) {
      mapBox.style.aspectRatio = `${mp.lon[1] - mp.lon[0]} / ${mp.lat[1] - mp.lat[0]}`;
      mapBox.append(h('img', { src: mp.img, alt: X[tab], draggable: 'false' }));
      ms.forEach((m, i) => {
        const x = (m.lon - mp.lon[0]) / (mp.lon[1] - mp.lon[0]) * 100, y = (mp.lat[1] - m.lat) / (mp.lat[1] - mp.lat[0]) * 100;
        const pin = h('button', { class: 'pin' + (m.status === 'used' ? ' used' : ''), type: 'button', 'data-id': m.id, 'aria-label': L(m.name), text: String(i + 1),
          style: { left: x + '%', top: y + '%', marginLeft: (m.nudge?.[0] || 0) + 'px', marginTop: (m.nudge?.[1] || 0) + 'px' }, onclick: () => pick(m.id) });
        mapBox.append(pin);
      });
      note.replaceChildren(X.mapBy + ': ', h('a', { href: mp.url, target: '_blank', rel: 'noopener', text: mp.credit }), '. ' + X.coords);
    } else note.textContent = X.deepNote;
    list.replaceChildren(...ms.map((m, i) => card(m, mp ? i + 1 : 0)));
  }
  draw();
  view.replaceChildren(page);
}
