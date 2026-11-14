// Builds data/furi.json: readings (furigana) for the Japanese words used in the app, for the "ふりがな" reading aid.
//
//   npm install kuromoji            (anywhere; pass its folder with KUROMOJI=/path/to/node_modules/kuromoji)
//   node tools/furigana/build.mjs   (run from the repository root)
//
// How it works
// 1. Collect every Japanese string the app can show (data/*.json and the text tables inside js/).
// 2. Split each string into words with kuromoji, which also gives each word's reading in context.
// 3. Keep the words that contain a kanji taught after grade 2 (younger readers may not know them yet).
// 4. Write { word: "{漢|かん}{字|じ}" } so the app can add ruby text by looking words up, longest first.
// 5. Check: looking words up in the finished list must give the same result as step 2 for every string.
//    Strings where it would differ are listed, and the words that cause it are dropped or fixed in OVERRIDES.
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const kuromoji = require(process.env.KUROMOJI || 'kuromoji');
const DICT = (process.env.KUROMOJI || require.resolve('kuromoji').replace(/src.*$/, '')) + '/dict';

const G1 = '一右雨円王音下火花貝学気九休玉金空月犬見五口校左三山子四糸字耳七車手十出女小上森人水正生青夕石赤千川先早草足村大男竹中虫町天田土二日入年白八百文木本名目立力林六';
const G2 = '引羽雲園遠何科夏家歌画回会海絵外角楽活間丸岩顔汽記帰弓牛魚京強教近兄形計元言原戸古午後語工公広交光考行高黄合谷国黒今才細作算止市矢姉思紙寺自時室社弱首秋週春書少場色食心新親図数西声星晴切雪船線前組走多太体台地池知茶昼長鳥朝直通弟店点電刀冬当東答頭同道読内南肉馬売買麦半番父風分聞米歩母方北毎妹万明鳴毛門夜野友用曜来里理話';
const EASY = new Set([...G1, ...G2]);
const KANJI = /[一-鿿々]/;
const hira = s => s.replace(/[ァ-ヶ]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60));
const isKana = c => /[぀-ゟ゠-ヿー]/.test(c);

// Readings fixed by hand (kuromoji picked another reading, or the word needs one fixed reading). '' drops the word.
const OVERRIDES = JSON.parse(fs.readFileSync(new URL('./overrides.json', import.meta.url)));

function collect() {
  const out = new Set();
  const add = s => String(s).split(/\n/).forEach(l => { l = l.trim(); if (KANJI.test(l)) out.add(l); });
  const walk = o => { if (typeof o === 'string') add(o); else if (Array.isArray(o)) o.forEach(walk); else if (o && typeof o === 'object') Object.values(o).forEach(walk); };
  for (const f of ['posts', 'accounts', 'machines', 'about', 'library']) walk(JSON.parse(fs.readFileSync(`data/${f}.json`, 'utf8')));
  for (const f of ['js/i18n.js', 'js/apps/shindan.js', 'js/apps/lag.js', 'js/map.js', 'js/feed.js', 'js/pages.js', 'js/sheets.js', 'js/create.js', 'js/main.js']) {
    const src = fs.readFileSync(f, 'utf8');
    for (const m of src.matchAll(/'((?:\\.|[^'\\\n])*)'|"((?:\\.|[^"\\\n])*)"|`((?:\\.|[^`\\])*)`/g)) {
      const s = (m[1] ?? m[2] ?? m[3]).replace(/\\n/g, '\n').replace(/\\(['"`])/g, '$1').replace(/\$\{[^}]*\}/g, '0');
      add(s);
    }
  }
  return [...out];
}

// "打ち上げ" + "うちあげ" -> "{打|う}ち{上|あ}げ"
function align(surface, reading) {
  let pattern = '^', groups = [];
  for (let i = 0; i < surface.length;) {
    if (isKana(surface[i]) || !KANJI.test(surface[i])) { pattern += hira(surface[i]).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); groups.push(null); i++; }
    else { let j = i; while (j < surface.length && KANJI.test(surface[j])) j++; pattern += '(.+?)'; groups.push(surface.slice(i, j)); i = j; }
  }
  const m = reading.match(new RegExp(pattern + '$'));
  if (!m) return `{${surface}|${reading}}`;
  let k = 1, out = '', idx = 0;
  for (let i = 0; i < surface.length;) {
    const g = groups[idx++];
    if (g === null) { out += surface[i]; i++; } else { out += `{${g}|${m[k++]}}`; i += g.length; }
  }
  return out;
}

const tokenizer = await new Promise((ok, no) => kuromoji.builder({ dicPath: DICT }).build((e, t) => e ? no(e) : ok(t)));
const corpus = collect();
const want = t => KANJI.test(t.surface_form) && [...t.surface_form].some(c => KANJI.test(c) && !EASY.has(c));
const seen = new Map();       // surface -> Map(reading -> count)
for (const line of corpus) for (const t of tokenizer.tokenize(line)) {
  if (!want(t)) continue;
  const r = t.reading && t.reading !== '*' ? hira(t.reading) : '?';
  if (!seen.has(t.surface_form)) seen.set(t.surface_form, new Map());
  const m = seen.get(t.surface_form); m.set(r, (m.get(r) || 0) + 1);
}
const dict = {}, conflicts = [], unknown = [];
for (const [s, m] of seen) {
  if (s in OVERRIDES) { if (OVERRIDES[s]) dict[s] = OVERRIDES[s].includes('{') ? OVERRIDES[s] : align(s, OVERRIDES[s]); continue; }
  const rs = [...m.keys()];
  if (rs.includes('?')) { unknown.push(s); continue; }
  if (rs.length > 1) { conflicts.push(`${s}: ${rs.join(' / ')}`); continue; }
  dict[s] = align(s, rs[0]);
}
for (const [s, r] of Object.entries(OVERRIDES)) if (r && !(s in dict)) dict[s] = r.includes('{') ? r : align(s, r);   // extra words and phrases

// Step 5: what the app will do (longest word first, left to right) must match the words kuromoji found.
const keys = Object.keys(dict).sort((a, b) => b.length - a.length);
const re = new RegExp(keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
const runtime = line => line.replace(re, w => dict[w]);
const byTokens = line => tokenizer.tokenize(line).map(t => (t.surface_form in dict && want(t)) ? dict[t.surface_form] : t.surface_form).join('');
// Phrases fixed by hand in OVERRIDES win over kuromoji's split, so compare with those phrases protected.
const phrases = Object.keys(OVERRIDES).filter(k => OVERRIDES[k] && !seen.has(k)).sort((x, y) => y.length - x.length);
const protect = line => { const parts = []; let rest = line; for (;;) { let at = -1, hit = ''; for (const p of phrases) { const i = rest.indexOf(p); if (i >= 0 && (at < 0 || i < at)) { at = i; hit = p; } } if (at < 0) { parts.push(byTokens(rest)); break; } parts.push(byTokens(rest.slice(0, at)), dict[hit]); rest = rest.slice(at + hit.length); } return parts.join(''); };
const diffs = [];
for (const line of corpus) { const a = runtime(line), b = protect(line); if (a !== b) diffs.push({ line, a, b }); }

fs.writeFileSync('data/furi.json', JSON.stringify(dict));
console.log(`strings ${corpus.length}, words ${keys.length}, conflicts ${conflicts.length}, unknown ${unknown.length}, lookup differs in ${diffs.length} strings`);
if (process.env.REPORT) fs.writeFileSync(process.env.REPORT, JSON.stringify({ conflicts, unknown, diffs: diffs.slice(0, 200), dict }, null, 1));
