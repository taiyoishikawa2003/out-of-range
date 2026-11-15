import { h, icon, img, loadImgs, slideText } from './render.js';
import { furiButton } from './furi.js';
import { t, L, getLang } from './i18n.js';
import * as S from './store.js';
import { db, allPosts, account, postsBy, thumbOf, reloadMine } from './data.js';
import { fmt, toast } from './sheets.js';

// Everything that is more than a post, in one place (shown at the top of Discover)
const HUB = [
  ['🎮', '#/p/lag-1', { ja: '火星の車を運転', en: 'Drive a Mars rover' }, { ja: 'ラグ20分のゲーム', en: 'A game with a 20-minute lag' }],
  ['🔮', '#/p/shindan-1', { ja: 'タイプ診断', en: 'Which machine are you?' }, { ja: 'あなたはどの探査機？', en: '5 questions' }],
  ['🗺', '#/map', { ja: '今どこにいる？', en: 'Where are they now?' }, { ja: '月と火星の地図', en: 'Maps of the Moon and Mars' }],
  ['🧾', 'lost/', { ja: '遺失物センター', en: 'Lunar Lost & Found' }, { ja: '月の落とし物の窓口', en: 'Things left on the Moon' }],
  ['✏️', '#/create', { ja: '投稿を作る', en: 'Make a post' }, { ja: '本物の写真で', en: 'With real NASA photos' }],
  ['✅', '#/me', { ja: 'スタンプ', en: 'Fact-check stamps' }, { ja: '出典を開いて集める', en: 'Open sources to collect' }],
];

function tile(p, { onDelete } = {}) {
  const lk = (p.stats?.likes || 0) + (S.isLiked(p.id) ? 1 : 0);
  const a = h('a', { href: '#/p/' + encodeURIComponent(p.id), 'aria-label': `@${p.account}: ${L(p.caption)}` },
    img(thumbOf(p), '', ''),
    p.type !== 'video' ? h('span', { class: 'gt' }, icon('layers')) : null,
    p.mine ? h('span', { class: 'mine', text: t('mine') }) : null,
    h('span', { class: 'gl' }, icon('heart'), fmt(lk)));
  if (onDelete) {
    const wrap = h('div', { style: { position: 'relative' } }, a,
      h('button', { class: 'iconbtn', type: 'button', 'aria-label': t('delete'), style: { position: 'absolute', right: '2px', bottom: '2px', background: 'rgba(0,0,0,.6)' }, onclick: () => onDelete(p) }, icon('x')));
    return wrap;
  }
  return a;
}
const grid = (posts, opt) => { const g = h('div', { class: 'grid' }, posts.map(p => tile(p, opt))); loadImgs(g); return g; };

function searchText(p) {
  const a = account(p.account);
  return [L(p.caption), (p.tags || []).join(' '), p.account, L(a.name), ...(p.slides || []).map(slideText)].join(' ').toLowerCase();
}

export function renderDiscover(view, q = '') {
  let place = 'all';
  const input = h('input', { type: 'search', placeholder: t('disc.search'), 'aria-label': t('disc.search'), value: q });
  const res = h('div', {});
  const chips = h('div', { class: 'chips', role: 'tablist' });
  const places = [['all', 'disc.all'], ['moon', 'disc.moon'], ['mars', 'disc.mars'], ['deep', 'disc.deep']];
  const drawChips = () => chips.replaceChildren(...places.map(([k, l]) => h('button', { class: 'chip' + (place === k ? ' on' : ''), type: 'button', role: 'tab', 'aria-selected': place === k, text: t(l), onclick: () => { place = k; drawChips(); draw(); } })));
  const draw = () => {
    const qq = input.value.trim().toLowerCase();
    const posts = allPosts().filter(p => (place === 'all' || p.place === place) && (!qq || searchText(p).includes(qq)));
    const accs = Object.entries(db.accounts).filter(([k, a]) => !a.hidden && (place === 'all' || a.place === place) && (!qq || (k + ' ' + L(a.name) + ' ' + L(a.bio)).toLowerCase().includes(qq)));
    res.replaceChildren(
      ...((place === 'all' && !qq) ? [h('h2', { class: 'hub-h', text: t('hub.title') }),
        h('div', { class: 'hub' }, HUB.map(([em, href, title, sub]) => h('a', { href }, h('span', { class: 'em', 'aria-hidden': 'true', text: em }), h('span', {}, h('b', { text: L(title) }), h('small', { text: L(sub) })))))] : []),
      ...[['disc.accounts', accs.filter(([, a]) => a.kind === 'machine')], ['disc.channels', accs.filter(([, a]) => a.kind !== 'machine')]].flatMap(([label, list]) => list.length ? [
        h('h2', { text: t(label) }),
        h('div', { class: 'chips' }, list.map(([k, a]) => h('a', { class: 'chip', href: '#/u/' + k, style: { display: 'flex', alignItems: 'center', textDecoration: 'none' }, text: L(a.name) })))] : []),
      h('h2', { text: t('disc.posts') }),
      posts.length ? grid(posts) : h('p', { class: 'hint', text: t('disc.none') }));
  };
  input.addEventListener('input', draw);
  drawChips(); draw();
  view.replaceChildren(h('div', { class: 'page' }, h('div', { class: 'search' }, icon('search'), input), chips, res));
  if (!matchMedia('(pointer:coarse)').matches) input.focus();
}

export function renderProfile(view, handle) {
  const a = account(handle);
  const posts = postsBy(handle);
  const likes = posts.reduce((n, p) => n + (p.stats?.likes || 0) + (S.isLiked(p.id) ? 1 : 0), 0);
  const fb = h('button', { class: 'btn', type: 'button' });
  const fc = h('b');
  const draw = () => { const on = S.isFollowing(handle); fb.textContent = t(on ? 'following' : 'follow'); fb.className = 'btn' + (on ? ' ghost' : ''); fc.textContent = fmt((a.followers || 0) + (on ? 1 : 0)); };
  fb.addEventListener('click', () => { S.toggleFollow(handle); draw(); });
  draw();
  const page = h('div', { class: 'page' },
    h('div', { class: 'backbar' }, h('button', { class: 'iconbtn', type: 'button', 'aria-label': t('back'), onclick: () => history.back() }, icon('left'))),
    h('div', { class: 'prof' },
      h('div', { class: 'big' }, a.avatar ? h('img', { src: a.avatar, alt: '' }) : (L(a.name) || handle)[0]),
      h('h1', { style: { margin: 0 }, text: L(a.name) || handle }),
      h('div', { class: 'hint' }, '@' + handle, a.kind ? h('span', { class: 'fan', text: t('prof.fan') }) : ''),
      a.since ? h('div', { class: 'since' }, h('span', { class: 'bars', 'aria-hidden': 'true' }, h('i'), h('i'), h('i'), h('i')), L(a.since)) : '',
      h('div', { class: 'stats' }, h('div', {}, h('b', { text: posts.length }), h('span', { text: t('prof.posts') })),
        h('div', {}, fc, h('span', { text: t('prof.followers') })), h('div', {}, h('b', { text: fmt(likes) }), h('span', { text: t('prof.likes') }))),
      fb, a.bio ? h('p', { class: 'bio', text: L(a.bio) }) : '',
      a.kind ? h('p', { class: 'hint pnote', text: t('prof.note.' + a.kind) }) : ''),
    grid(posts));
  loadImgs(page);
  view.replaceChildren(page);
}

/* fact-check stamps: one per post, earned by opening that post's sources */
function stamps() {
  const got = new Set(S.stampIds()), n = db.posts.filter(p => got.has(p.id)).length;
  return h('section', { class: 'stamps', 'aria-label': t('stamp.title') },
    h('h2', { text: `${t('stamp.title')} ${n}/${db.posts.length}` }),
    h('p', { class: 'hint', text: t(n === db.posts.length && n ? 'stamp.all' : 'stamp.how') }),
    h('div', { class: 'stamp-grid' }, db.posts.map(p => {
      const a = account(p.account), on = got.has(p.id);
      return h('a', { class: 'stamp' + (on ? ' on' : ''), href: '#/p/' + encodeURIComponent(p.id), 'aria-label': `@${p.account}: ${t(on ? 'stamp.yes' : 'stamp.no')}` },
        a.avatar ? h('img', { src: a.avatar, alt: '' }) : h('span', { text: '?' }), on ? h('b', { text: '✓' }) : '');
    })));
}

export function renderMe(view, tab = 'mine') {
  const tabs = [['mine', 'me.mine'], ['liked', 'me.liked'], ['saved', 'me.saved']];
  const body = h('div', {});
  const tabsEl = h('div', { class: 'tabs2', role: 'tablist' });
  const draw = () => {
    tabsEl.replaceChildren(...tabs.map(([k, l]) => h('button', { type: 'button', role: 'tab', 'aria-selected': tab === k, class: tab === k ? 'on' : '', text: t(l), onclick: () => { tab = k; draw(); } })));
    const byId = new Map(allPosts().map(p => [p.id, p]));
    let posts, opt = {};
    if (tab === 'mine') {
      posts = db.mine;
      opt.onDelete = async p => { await S.deleteMine(p.id); await reloadMine(); toast(t('deleted')); draw(); };
    } else posts = (tab === 'liked' ? S.likedIds() : S.savedIds()).map(id => byId.get(id)).filter(Boolean);
    body.replaceChildren(posts.length ? grid(posts, opt) : h('div', { style: { padding: '30px 0', textAlign: 'center' } },
      h('p', { class: 'hint', text: t(tab === 'mine' ? 'me.noneMine' : 'me.none') }),
      tab === 'mine' ? h('a', { class: 'btn', href: '#/create', text: t('cr.title') }) : ''));
  };
  draw();
  view.replaceChildren(h('div', { class: 'page' }, h('div', { class: 'backbar', style: { justifyContent: 'flex-end', gap: '8px' } }, furiButton(), h('button', { class: 'btn ghost sm', type: 'button', 'data-action': 'lang', text: t('lang') })), h('div', { class: 'prof' }, h('div', { class: 'big', style: { background: '#ffb000', color: '#111' }, text: '★' }), h('h1', { style: { margin: 0 }, text: t('me.title') }),
    h('p', { class: 'hint', text: t('me.local') })), stamps(), tabsEl, body));
}

/* ---------- About (for judges and teachers) ---------- */
export async function renderAbout(view) {
  let about = {};
  try { about = await fetch('data/about.json', { cache: 'no-cache' }).then(r => r.json()); } catch {}
  const lang = getLang();
  const sec = (title, ...kids) => h('section', { class: 'card' }, h('h2', { style: { marginTop: 0 }, text: title }), ...kids);
  const para = v => (Array.isArray(L(v)) ? L(v) : [L(v)]).filter(Boolean).map(x => h('p', { text: x }));
  // all sources used across the curated feed, de-duplicated
  const seen = new Map();
  db.posts.forEach(p => (p.sources || []).forEach(s => { const k = s.url || L(s.title); if (!seen.has(k)) seen.set(k, { ...s, posts: [] }); seen.get(k).posts.push(p.id); }));
  const page = h('div', { class: 'page' },
    h('div', { class: 'backbar', style: { justifyContent: 'space-between' } }, h('h1', { style: { margin: 0 }, text: 'OUT OF RANGE' }), h('div', { style: { display: 'flex', gap: '8px' } }, furiButton(), h('button', { class: 'btn ghost sm', type: 'button', 'data-action': 'lang', text: t('lang') }))),
    ...(about.sections || []).map(s => sec(L(s.title), ...para(s.body),
      s.table ? h('table', { class: 't' }, h('tr', {}, s.table.head.map(x => h('th', { text: L(x) }))), s.table.rows.map(r => h('tr', {}, r.map(c => h('td', { text: L(c) }))))) : '',
      s.list ? h('ul', {}, s.list.map(x => h('li', { text: L(x) }))) : '',
      s.links ? h('p', { style: { display: 'flex', gap: '8px', flexWrap: 'wrap' } }, s.links.map(l => h('a', { class: 'btn ghost sm', href: l.href, text: L(l.label), ...(/^https?:/.test(l.href) ? { target: '_blank', rel: 'noopener' } : {}) }))) : '')),
    sec(lang === 'ja' ? 'この作品で使った NASA などの資料' : 'NASA data and resources used in this project',
      h('ul', { class: 'srclist' }, [...seen.values()].map(s => h('li', {}, s.kind ? h('span', { class: 'k', text: L(s.kind) }) : '',
        s.url ? h('a', { href: s.url, target: '_blank', rel: 'noopener', text: L(s.title) || s.url }) : h('b', { text: L(s.title) }))))),
    h('p', { class: 'hint', text: `Build ${about.version || ''}` }));
  view.replaceChildren(page);
}
