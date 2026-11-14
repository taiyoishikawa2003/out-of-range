// Japanese reading aid: shows furigana (small kana above kanji) on words that younger readers may not know yet.
// The word list (data/furi.json) is built from the app's own text by tools/furigana/build.mjs and checked there.
// Videos and photo slides are pictures, so their text does not change; captions, comments, quizzes, the game, the map and About do.
import { getLang, onLang } from './i18n.js';

const KEY = 'oor.furi';
const SKIP = new Set(['RUBY', 'RT', 'RP', 'SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'SELECT', 'OPTION', 'TITLE']);
const OFF_LIMITS = '.nofuri,.tabbar,.sidenav,.feedtop,.rail,[data-action="furi"]';   // tight navigation labels, and text the user typed
const KANJI = /[一-鿿々]/;
let dict = null, re = null, obs = null, loading = null;

export const furiOn = () => { try { return localStorage.getItem(KEY) === '1'; } catch { return false; } };

function load() {
  if (!loading) loading = fetch('data/furi.json').then(r => r.json()).then(d => {
    dict = d;
    const keys = Object.keys(d).sort((a, b) => b.length - a.length);       // longest word first
    re = new RegExp(keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
  });
  return loading;
}

function ruby(word) {       // "{打|う}ち{上|あ}げ" -> <ruby>打<rt>う</rt></ruby>ち<ruby>上<rt>あ</rt></ruby>げ
  const frag = document.createDocumentFragment();
  dict[word].split(/(\{[^}]+\})/).forEach(part => {
    if (!part) return;
    const m = part.match(/^\{([^|]+)\|([^}]+)\}$/);
    if (!m) { frag.append(part); return; }
    const r = document.createElement('ruby'), rt = document.createElement('rt');
    rt.textContent = m[2]; r.append(m[1], rt); frag.append(r);
  });
  return frag;
}

function blocked(e) {
  for (; e && e.nodeType === 1; e = e.parentNode) if (SKIP.has(e.tagName) || e.classList.contains('furi') || e.matches(OFF_LIMITS) || e.isContentEditable) return true;
  return false;
}

function annotate(node) {
  const text = node.nodeValue, p = node.parentNode;
  if (!text || !p || !KANJI.test(text) || blocked(p)) return;
  re.lastIndex = 0;
  let m, last = 0, frag = null;
  while ((m = re.exec(text))) {
    if (!frag) frag = document.createDocumentFragment();
    if (m.index > last) frag.append(text.slice(last, m.index));
    frag.append(ruby(m[0])); last = re.lastIndex;
  }
  if (!frag) return;
  if (last < text.length) frag.append(text.slice(last));
  const span = document.createElement('span');
  span.className = 'furi'; span.dataset.t = text; span.append(frag);
  p.replaceChild(span, node);
}

function walk(root) {
  if (root.nodeType === 3) { annotate(root); return; }
  if (root.nodeType !== 1 || blocked(root)) return;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), nodes = [];
  for (let n; (n = w.nextNode());) nodes.push(n);
  nodes.forEach(annotate);
}

function start() {
  if (obs) return;
  document.documentElement.classList.add('furi-on');
  walk(document.body);
  obs = new MutationObserver(list => { for (const m of list) { if (m.type === 'characterData') annotate(m.target); else m.addedNodes.forEach(walk); } });
  obs.observe(document.body, { childList: true, subtree: true, characterData: true });
}

function stop() {
  document.documentElement.classList.remove('furi-on');
  if (obs) { obs.disconnect(); obs = null; }
  document.querySelectorAll('span.furi').forEach(s => s.replaceWith(document.createTextNode(s.dataset.t)));
}

async function apply() {
  if (getLang() === 'ja' && furiOn()) { await load(); start(); } else stop();
  document.querySelectorAll('[data-action="furi"]').forEach(label);
}

function label(b) {
  const on = furiOn();
  b.textContent = b.dataset.short ? 'ふりがな' : on ? 'ふりがな：あり' : 'ふりがな：なし';
  if (b.dataset.short) b.setAttribute('aria-label', on ? 'ふりがな：あり' : 'ふりがな：なし');
  b.setAttribute('aria-pressed', on); b.hidden = getLang() !== 'ja';
}

/** A toggle button (shown only in Japanese). Clicks are handled once, in initFuri. */
export function furiButton(cls) {
  const b = document.createElement('button');
  b.type = 'button'; b.className = cls || 'btn ghost sm'; b.dataset.action = 'furi'; if (!cls) b.dataset.short = '1'; label(b);
  return b;
}

export function initFuri() {
  document.addEventListener('click', e => {
    if (!e.target.closest('[data-action="furi"]')) return;
    e.stopPropagation();
    try { localStorage.setItem(KEY, furiOn() ? '0' : '1'); } catch {}
    apply();
  }, true);
  onLang(() => apply());
  return apply();
}
