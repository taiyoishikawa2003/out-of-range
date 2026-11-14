// "Which space machine are you?" A just-for-fun quiz. The answers are play; every fact on the result card is real (sources on the post).
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };

const TYPES = {
  opp: { img: 'media/avatars/opportunity_rover.jpg', link: '#/u/opportunity_rover',
    name: { ja: 'オポチュニティ', en: 'Opportunity' }, type: { ja: 'がんばりすぎタイプ', en: 'The one who never stops' },
    facts: { ja: ['予定は90日。実際は14年以上、火星を走りつづけた', '走った距離は45km。フルマラソンより長い'], en: ['Planned for 90 days. It kept driving on Mars for over 14 years', 'It drove 45 km, farther than a full marathon'] } },
  pio: { img: 'media/avatars/pioneer10.jpg', link: '#/u/pioneer10',
    name: { ja: 'パイオニア10号', en: 'Pioneer 10' }, type: { ja: 'マイペースで遠くへタイプ', en: 'The one who goes far, at its own pace' },
    facts: { ja: ['1972年に出発して、今も宇宙を飛びつづけている', '21か月の予定が、30年以上も地球に信号を送ってくれた'], en: ['It left in 1972 and is still flying through space', 'Planned for 21 months, it kept calling home for over 30 years'] } },
  sur: { img: 'media/avatars/surveyor3.jpg', link: '#/u/surveyor3',
    name: { ja: 'サーベイヤー3号', en: 'Surveyor 3' }, type: { ja: 'じっと待てるタイプ', en: 'The patient one' },
    facts: { ja: ['月で2年半、ひとりで待っていたら、宇宙飛行士が会いに来た', '今も月の同じ場所にいる'], en: ['It waited alone on the Moon for 2.5 years, and then astronauts came to visit', 'It is still in the same spot on the Moon'] } },
  near: { img: 'media/avatars/near_shoemaker.jpg', link: '#/u/near_shoemaker',
    name: { ja: 'NEARシューメーカー', en: 'NEAR Shoemaker' }, type: { ja: 'むちゃぶりに強いタイプ', en: 'The one who says “OK, I’ll try”' },
    facts: { ja: ['着陸用に作られていないのに、小惑星に着陸した', '着陸のあとも約2週間、データを送りつづけた'], en: ['It was not built to land, but it landed on an asteroid', 'After landing, it kept sending data for about two weeks'] } },
  spi: { img: 'media/avatars/spirit_rover.jpg', link: '#/u/spirit_rover',
    name: { ja: 'スピリット', en: 'Spirit' }, type: { ja: '転んでもただでは起きないタイプ', en: 'The one who turns trouble into treasure' },
    facts: { ja: ['こわれた車輪を引きずって走ったら、地面から大発見が出てきた', '予定は90日。実際は6年以上はたらいた'], en: ['Dragging a broken wheel, it dug up a major discovery', 'Planned for 90 days. It worked for over 6 years'] } },
  ing: { img: 'media/library/ingenuity.jpg', link: '#/p/ranking-overtime-1',
    name: { ja: 'インジェニュイティ', en: 'Ingenuity' }, type: { ja: 'ちっちゃい挑戦者タイプ', en: 'The small one who goes first' },
    facts: { ja: ['地球ではない星で、初めて空を飛んだヘリコプター', '5回飛ぶ予定が、72回も飛んだ'], en: ['The first helicopter to fly on another planet', 'Planned for 5 flights. It made 72'] } },
  kep: { img: 'media/avatars/kepler_uranai.jpg', link: '#/u/kepler_uranai',
    name: { ja: 'ケプラー', en: 'Kepler' }, type: { ja: 'じっと見つめる観察タイプ', en: 'The quiet observer' },
    facts: { ja: ['9年間、星をじっと見つめつづけた', '太陽系の外にある惑星を、2,600個以上見つけた'], en: ['It stared at the stars for nine years', 'It found more than 2,600 planets beyond our solar system'] } },
  vik: { img: 'media/avatars/viking1_lander.jpg', link: '#/u/viking1_lander',
    name: { ja: 'バイキング1号', en: 'Viking 1' }, type: { ja: 'まじめな報告タイプ', en: 'The reliable reporter' },
    facts: { ja: ['火星から6年間、写真や天気の報告を送りつづけた', '予定は、たったの90日だった'], en: ['It sent photos and weather reports from Mars for six years', 'The plan was only 90 days'] } }
};

const QS = [
  { q: { ja: '夏休みの宿題、どうする？', en: 'Summer homework. What do you do?' }, a: [
    [{ ja: '毎日ちょっとずつ、まじめに', en: 'A little every day' }, { vik: 2, kep: 1 }],
    [{ ja: '気づいたら最終日', en: 'Suddenly it’s the last day' }, { near: 2, pio: 1 }],
    [{ ja: 'やり始めたら止まらない', en: 'Once I start, I can’t stop' }, { opp: 2, spi: 1 }]] },
  { q: { ja: '急に「これやって！」と言われたら？', en: 'Someone suddenly says “Do this!”' }, a: [
    [{ ja: 'え、聞いてない。でもやる', en: 'Nobody told me… but OK' }, { near: 2, ing: 1 }],
    [{ ja: 'まず、じっくり様子を見る', en: 'First I watch carefully' }, { kep: 2, sur: 1 }],
    [{ ja: 'とにかく走り出す', en: 'I just start running' }, { pio: 2, opp: 1 }]] },
  { q: { ja: '得意なのは、どれ？', en: 'What are you good at?' }, a: [
    [{ ja: 'じっと待つこと', en: 'Waiting patiently' }, { sur: 2, kep: 1 }],
    [{ ja: '遠くまで行くこと', en: 'Going far' }, { pio: 2, opp: 1 }],
    [{ ja: 'だれもやってないことを最初にやる', en: 'Doing something first' }, { ing: 2, vik: 1 }]] },
  { q: { ja: '自転車がこわれた！どうする？', en: 'Your bike breaks! What now?' }, a: [
    [{ ja: 'こわれたまま、なんとか進む', en: 'Keep going anyway' }, { spi: 3 }],
    [{ ja: '直るまで待つ', en: 'Wait until it’s fixed' }, { sur: 2, vik: 1 }],
    [{ ja: '歩いて行く。遠くても気にしない', en: 'Walk. Far is fine' }, { opp: 2, pio: 1 }]] },
  { q: { ja: 'みんなによく言われるのは？', en: 'What do people say about you?' }, a: [
    [{ ja: '「まじめだね」', en: '“You’re so careful”' }, { vik: 2, kep: 1 }],
    [{ ja: '「ちっちゃいのに、やるね」', en: '“Small, but wow”' }, { ing: 3 }],
    [{ ja: '「むちゃするね」', en: '“You’re a daredevil”' }, { near: 2, spi: 1 }]] }
];

const TX = {
  ja: { title: 'あなたは\nどの探査機タイプ？', sub: '5つの質問でわかる（お遊びです）', start: 'はじめる', youAre: 'あなたは…', see: 'この機械の投稿を見る', again: 'もう一回', share: 'シェア', note: '診断はお遊びです。機械の話は本当です。', copied: 'コピーしました', shareText: (n, ty) => `わたしは「${n}」＝${ty} でした。 #OUTOFRANGE` },
  en: { title: 'Which space machine\nare you?', sub: '5 questions (just for fun)', start: 'Start', youAre: 'You are…', see: 'See this machine’s posts', again: 'Play again', share: 'Share', note: 'The quiz is just for fun. The facts about the machines are real.', copied: 'Copied', shareText: (n, ty) => `I got “${n}”: ${ty}. #OUTOFRANGE` }
};

export function mount(box, { lang, toast }) {
  const X = TX[lang] || TX.en, P = o => o[lang] || o.en;
  box.classList.add('shindan');
  let step = -1, score = {}, last = null;
  const colors = ['c0', 'c1', 'c2'];
  function draw() {
    box.replaceChildren();
    if (step < 0) {
      const mosaic = el('div', 'sd-mosaic'); Object.values(TYPES).forEach(ty => { const i = el('img'); i.src = ty.img; i.alt = ''; mosaic.append(i); });
      const b = el('button', 'sd-start', X.start); b.type = 'button'; b.onclick = () => { step = 0; score = {}; draw(); };
      const t = el('h2', 'sd-title'); X.title.split('\n').forEach((l, i) => { if (i) t.append(document.createElement('br')); t.append(l); });
      box.append(mosaic, el('div', 'sd-shade'), el('div', 'sd-in', null)); box.lastChild.append(t, el('p', 'sd-sub', X.sub), b);
      return;
    }
    if (step < QS.length) {
      const q = QS[step], wrap = el('div', 'sd-in');
      const dots = el('div', 'sd-dots'); QS.forEach((_, i) => dots.append(el('i', i <= step ? 'on' : '')));
      wrap.append(dots, el('h2', 'sd-q', P(q.q)));
      q.a.forEach(([label, pts], i) => { const b = el('button', 'sd-opt ' + colors[i], P(label)); b.type = 'button'; b.onclick = () => { for (const k in pts) score[k] = (score[k] || 0) + pts[k]; last = Object.keys(pts)[0]; step++; draw(); }; wrap.append(b); });
      box.append(wrap); return;
    }
    const best = Object.keys(TYPES).reduce((a, k) => ((score[k] || 0) > (score[a] || 0) || ((score[k] || 0) === (score[a] || 0) && k === last) ? k : a), Object.keys(TYPES)[0]);
    const ty = TYPES[best]; try { localStorage.setItem('oor.shindan', best); } catch {}
    const wrap = el('div', 'sd-in sd-res');
    const im = el('img', 'sd-pic'); im.src = ty.img; im.alt = P(ty.name);
    const facts = el('ul', 'sd-facts'); P(ty.facts).forEach(f => facts.append(el('li', '', f)));
    const see = el('a', 'sd-start', X.see); see.href = ty.link;
    const row = el('div', 'sd-row');
    const again = el('button', 'sd-ghost', X.again); again.type = 'button'; again.onclick = () => { step = -1; draw(); };
    const share = el('button', 'sd-ghost', X.share); share.type = 'button';
    share.onclick = async () => { const text = X.shareText(P(ty.name), P(ty.type)), url = location.origin + location.pathname + '#/p/shindan-1'; try { if (navigator.share) await navigator.share({ text, url }); else { await navigator.clipboard.writeText(text + ' ' + url); toast?.(X.copied); } } catch {} };
    row.append(again, share);
    wrap.append(el('p', 'sd-you', X.youAre), im, el('h2', 'sd-name', P(ty.name)), el('p', 'sd-type', P(ty.type)), facts, see, row, el('p', 'sd-note', X.note));
    box.append(wrap);
  }
  draw();
  return { activate() {}, deactivate() {} };
}
