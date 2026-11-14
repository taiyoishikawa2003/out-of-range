/* Lunar Lost & Found — static, no build. Apache-2.0. */
(() => {
'use strict';
const IMG = id => `https://images-assets.nasa.gov/image/${id}/${id}~medium.jpg`;
const PAGE = id => `https://images.nasa.gov/details/${id}`;
const MOON_KM = 384400; // average Earth–Moon distance
let lang = (localStorage.getItem('lf-lang') || (navigator.language || 'ja')).startsWith('ja') ? 'ja' : 'en';
try { const q = new URLSearchParams(location.search).get('lang'); if (q === 'en' || q === 'ja') lang = q; } catch (e) {}
const T = o => (o && typeof o === 'object' && 'ja' in o) ? o[lang] : o;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const UI = {
  title: {ja:'月面遺失物センター', en:'Lunar Lost & Found'},
  call: {ja:'呼出番号', en:'Ticket'},
  sources: {ja:'出典', en:'Sources'}, about: {ja:'この作品について', en:'About'},
  hello: {ja:'いらっしゃいませ。<br>何を落とされましたか？', en:'Welcome.<br>What did you lose?'},
  hint: {ja:'さわると、窓口の者がご案内します', en:'Tap an item and I will help you'},
  keeping: {ja:'保管中', en:'In storage'}, picked: {ja:'受け取り済み', en:'Picked up'},
  slip: {ja:'預り票', en:'CLAIM SLIP'},
  k_item: {ja:'品名', en:'Item'}, k_owner: {ja:'落とし主', en:'Owner'}, k_date: {ja:'拾得日', en:'Found'},
  k_place: {ja:'場所', en:'Place'}, k_note: {ja:'状況', en:'Notes'}, k_kept: {ja:'保管', en:'Stored'},
  nextdoor: {ja:'同じ場所でお預かり中の機械', en:'The machine kept next to it'},
  toScience: {ja:'となりの機械を見せてもらう', en:'See the machine next door'},
  pickup: {ja:'受け取り手続きへ', en:'Go to pickup'},
  back: {ja:'‹ 窓口にもどる', en:'‹ Back to the counter'},
  backItem: {ja:'‹ 預り票にもどる', en:'‹ Back to the slip'},
  chooseWay: {ja:'月までの移動手段を選んでください', en:'How will you travel to the Moon?'},
  arrive: {ja:'到着予定', en:'Estimated arrival'},
  assume: {ja:'月までの平均距離 384,400km を、休まず同じ速さで進んだ場合の概算です。', en:'Rough estimate: the average Earth–Moon distance (384,400 km), nonstop at a constant speed.'},
  onlyHere: {ja:'※お渡しは<b>現地のみ</b>です。月の物は「人がここに来た」証拠として、そのまま残されています。', en:'※ Items are handed over <b>on site only</b>. Things on the Moon are left where they are, as evidence that people were there.'},
  srcLabel: {ja:'出典', en:'Sources'},
  photo: {ja:'写真', en:'Photo'},
};

const ITEMS = [
 { id:'golf', no:'0014', img:'s71-20784',
   name:{ja:'ゴルフボール 2個', en:'Two golf balls'},
   cap:{ja:'打った瞬間のテレビ中継（1971年2月6日）', en:'TV broadcast of the shot (6 Feb 1971)'},
   owner:{ja:'アラン・シェパード 様（アポロ14号 船長）', en:'Mr. Alan Shepard (Apollo 14 commander)'},
   date:{ja:'1971年2月6日', en:'6 Feb 1971'},
   place:{ja:'月・フラマウロ高地（アポロ14号）', en:'Fra Mauro highlands, Moon (Apollo 14)'},
   note:{ja:'月の土を拾う道具の柄に、6番アイアンの頭を付けて片手で打った', en:'Hit one-handed with a 6-iron head fixed to a soil-sampling tool handle'},
   since:1971,
   clerk:{ja:'こちらですね。<b>1971年</b>からお預かりしています。<br>実は、このボールの<b>すぐそば</b>に、今も地球と“キャッチボール”をしている機械があるんですよ。', en:'Here it is. We have kept it since <b>1971</b>.<br>Right <b>next to it</b> is a machine that is still playing catch with Earth today.'},
   next:'laser',
   src:[['NASA Image: S71-20784', PAGE('s71-20784')],['Smithsonian NASM: Apollo 14','https://airandspace.si.edu/apollo-missions/apollo-14']] },
 { id:'family', no:'0016', img:'as16-107-17436',
   name:{ja:'家族の写真 1枚', en:'A family photo'},
   cap:{ja:'写真を置いたデューク飛行士が撮った着陸地点（1972年）。家族写真そのものは NASA の記録 AS16-117-18841 に写っています', en:'The landing site, photographed by Duke himself (1972). The family photo is in NASA frame AS16-117-18841'},
   owner:{ja:'チャーリー・デューク 様（アポロ16号）', en:'Mr. Charlie Duke (Apollo 16)'},
   date:{ja:'1972年4月23日', en:'23 Apr 1972'},
   place:{ja:'月・デカルト高地（アポロ16号）', en:'Descartes highlands, Moon (Apollo 16)'},
   note:{ja:'ビニールに包んで地面に置いた。裏には「地球から来た宇宙飛行士デュークの家族です」という言葉', en:'Wrapped in plastic and laid on the ground. The back says it is the family of astronaut Duke from planet Earth'},
   since:1972,
   clerk:{ja:'ご家族は静かにお休み中です。<br>でも<b>お隣さん</b>は、月の“ゆれ”をずっと聞いていたんです。', en:'The family is resting quietly.<br>But the <b>neighbour</b> spent years listening to the Moon shake.'},
   next:'quake',
   src:[['NASA Apollo Lunar Surface Journal: the Duke family portrait (AS16-117-18841)','https://www.nasa.gov/history/alsj/a16/a16.data_trvl.html'],['NASA Image: AS16-107-17436', PAGE('as16-107-17436')]] },
 { id:'bags', no:'0011', img:'as14-66-09278',
   name:{ja:'袋 約96個（中身はご想像に）', en:'About 96 bags (use your imagination)'},
   cap:{ja:'袋が置かれた着陸地点の一つ（アポロ14号）', en:'One of the landing sites where bags were left (Apollo 14)'},
   owner:{ja:'アポロの宇宙飛行士 12名', en:'12 Apollo moonwalkers'},
   date:{ja:'1969〜1972年', en:'1969–1972'},
   place:{ja:'月・着陸地点 6か所', en:'6 landing sites, Moon'},
   note:{ja:'中身：おしっこ・うんち など。帰りに月の石を積むため、置いていった', en:'Contents: pee, poop, etc. Left behind to make room for Moon rocks'},
   since:1969,
   clerk:{ja:'……こちらは、あまり開けたくない落とし物です。<br>でも、なぜ置いていったのか。答えは<b>“重さ”</b>なんです。', en:'…This one we would rather not open.<br>But why was it left? The answer is <b>weight</b>.'},
   next:'weight',
   src:[['History.com: 8 things astronauts left on the Moon (quotes former NASA chief historian)','https://www.history.com/articles/things-moon-astronauts-apollo'],['NASA Image: AS14-66-9278', PAGE('as14-66-09278')]] },
 { id:'surveyor', no:'0003', img:'AS12-48-7134', done:true,
   name:{ja:'サーベイヤー3号のカメラ', en:'Surveyor 3’s camera'},
   cap:{ja:'サーベイヤー3号とアポロ12号の飛行士（1969年11月20日）', en:'Surveyor 3 and an Apollo 12 astronaut (20 Nov 1969)'},
   owner:{ja:'無人探査機 サーベイヤー3号', en:'Robotic lander Surveyor 3'},
   date:{ja:'1967年4月20日 着陸', en:'Landed 20 Apr 1967'},
   place:{ja:'月・嵐の大洋', en:'Ocean of Storms, Moon'},
   note:{ja:'1969年11月、アポロ12号の2人が歩いて受け取りに来た', en:'In Nov 1969, two Apollo 12 astronauts walked over to pick it up'},
   since:null,
   clerk:{ja:'こちらは<b>本当に受け取られた</b>、とてもめずらしい落とし物です。', en:'This is a rare one: it was <b>actually picked up</b>.'},
   next:'surveyor',
   src:[['NSSDCA: Apollo 12 LM / ALSEP (1969-099C)','https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C'],['NASA Science: Surveyor 3','https://science.nasa.gov/mission/surveyor-3/'],['NASA Image: AS12-48-7134', PAGE('AS12-48-7134')]] },
];

const SCI = {
 laser:{ img:'as14-67-09386',
   name:{ja:'月のレーザー反射鏡（アポロ14号）', en:'Laser retroreflector (Apollo 14)'},
   cap:{ja:'ボールと同じアポロ14号が置いた反射鏡', en:'The reflector left by the same Apollo 14 crew'},
   clerk:{ja:'この板は、地球から飛んできた<b>光</b>を、来た方向へそのまま打ち返すんです。<br>ためしに、地球からレーザーを撃ってみませんか？', en:'This panel bounces <b>light</b> from Earth straight back where it came from.<br>Want to fire a laser from Earth?'},
   src:[['NASA: Laser beams reflected between Earth and Moon boost science','https://www.nasa.gov/missions/lro/laser-beams-reflected-between-earth-and-moon-boost-science/'],['NASA GSFC: Measuring the Moon’s distance','https://eclipse.gsfc.nasa.gov/help/ApolloLaser.html'],['NASA Image: AS14-67-9386', PAGE('as14-67-09386')]] },
 quake:{ img:'as16-113-18347',
   name:{ja:'月の地震計（アポロ月面実験装置 ALSEP）', en:'Moon seismometer (ALSEP)'},
   cap:{ja:'アポロ16号が置いた月面実験装置', en:'Experiment package left by Apollo 16'},
   clerk:{ja:'1969年、科学者は使い終わった宇宙船を<b>わざと月に落とし</b>ました。<br>月をたたいたら、どうなったと思います？', en:'In 1969, scientists <b>crashed a used spacecraft into the Moon on purpose</b>.<br>What do you think happened?'},
   src:[['NSSDCA: Apollo 12 LM / ALSEP (1969-099C)','https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C'],['NASA SP-235: Apollo 12 Preliminary Science Report (1970)','https://ntrs.nasa.gov/search?q=SP-235%20Apollo%2012%20Preliminary%20Science%20Report'],['NASA Image: S69-59547 (seismometer record)', PAGE('S69-59547')],['NASA Image: AS16-113-18347', PAGE('as16-113-18347')],['NASA Science: Earth’s Moon','https://science.nasa.gov/moon/']] },
 weight:{ img:'as14-66-09277',
   name:{ja:'着陸船の下半分（いまも月にある）', en:'Lunar Module descent stage (still on the Moon)'},
   cap:{ja:'アポロ14号の着陸船。下半分は今も月にある', en:'Apollo 14’s lander. Its lower half is still there'},
   clerk:{ja:'帰りは、着陸船の<b>上半分だけ</b>が飛び立ちました。下半分は<b>発射台</b>になって、月に残ったんです。', en:'Only the <b>top half</b> of the lander flew home. The bottom half became the <b>launch pad</b> and stayed.'},
   src:[['NASA Image 0101207: Lunar Module configuration (MSFC caption)', PAGE('0101207')],['NASA Image: AS14-66-9277', PAGE('as14-66-09277')],['History.com: 8 things astronauts left on the Moon','https://www.history.com/articles/things-moon-astronauts-apollo']] },
 surveyor:{ img:'AS12-48-7134',
   name:{ja:'サーベイヤー3号（無人探査機）', en:'Surveyor 3 (robotic lander)'},
   cap:{ja:'飛行士がサーベイヤー3号を調べているところ', en:'An astronaut examining Surveyor 3'},
   clerk:{ja:'受け取りに来られた方は、今のところ<b>この1件だけ</b>です。', en:'So far, this is the <b>only</b> pickup we have had.'},
   src:[['NSSDCA: Apollo 12 LM / ALSEP (1969-099C)','https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C'],['NASA Science: Surveyor 3','https://science.nasa.gov/mission/surveyor-3/'],['NASA Image: AS12-48-7134', PAGE('AS12-48-7134')]] },
};

const WAYS = [
 {k:'walk', ja:'歩く（時速4km）', en:'Walk (4 km/h)', h: MOON_KM/4},
 {k:'bike', ja:'自転車（時速15km）', en:'Bicycle (15 km/h)', h: MOON_KM/15},
 {k:'train', ja:'新幹線（時速300km）', en:'Bullet train (300 km/h)', h: MOON_KM/300},
 {k:'apollo', ja:'アポロのロケット', en:'Apollo rocket', h: 3.5*24, note:{ja:'月を回る軌道まで約3〜4日', en:'about 3–4 days to lunar orbit'}},
 {k:'light', ja:'光（レーザー）', en:'Light (laser)', h: 1.28/3600, note:{ja:'片道約1.3秒。ただし人は光になれません', en:'about 1.3 s one way. Sadly, people can’t travel as light'}},
];

const view = document.getElementById('view');
const clerk = html => `<div class="clerk"><div class="face" role="img" aria-label="${lang==='ja'?'窓口の係員':'Counter clerk'}"></div><div class="bubble">${html}</div></div>`;
const img = (id, alt, cls='') => `<img class="${cls}" src="${IMG(id)}" alt="${esc(alt)}" loading="lazy" onerror="this.onerror=null;this.src='${IMG(id).replace('~medium','~thumb')}'">`;
const srcList = arr => `<div class="src">${T(UI.srcLabel)}: ${arr.map(([t,u])=>`<a href="${u}" target="_blank" rel="noopener">${esc(t)}</a>`).join(' / ')}</div>`;
const yearsSince = y => new Date().getFullYear() - y;
const setCall = n => { document.getElementById('callNo').textContent = n; };

function home(){
  setCall('014');
  view.innerHTML = clerk(T(UI.hello)) +
   `<div class="grid">${ITEMS.map(it=>`<a class="item" href="#/item/${it.id}">${img(it.img, T(it.name))}<div class="lbl">${esc(T(it.name))}<br><span class="tag ${it.done?'done':''}">${T(it.done?UI.picked:UI.keeping)}</span></div></a>`).join('')}</div>
    <p class="hint">${T(UI.hint)}</p>`;
}

function item(id){
  const it = ITEMS.find(x=>x.id===id); if(!it) return home();
  const s = SCI[it.next];
  setCall(it.no.slice(1));
  const kept = it.since ? (lang==='ja' ? `月面にて保管中（${yearsSince(it.since)}年）` : `On the Moon (${yearsSince(it.since)} years)`) : (lang==='ja'?'1969年 アポロ12号が約10kgの部品を持ち帰り':'Apollo 12 took about 10 kg of parts home in 1969');
  view.innerHTML = `<a class="back" href="#/">${T(UI.back)}</a>` + clerk(T(it.clerk)) +
   `<div class="slip"><div class="slip-head"><span>${T(UI.slip)}</span><span>No.${it.no}</span></div>
     <figure>${img(it.img, T(it.cap))}<figcaption>${esc(T(it.cap))} — ${T(UI.photo)}: NASA</figcaption></figure>
     <div class="row"><span class="k">${T(UI.k_item)}</span><span class="v big">${esc(T(it.name))}</span></div>
     <div class="row"><span class="k">${T(UI.k_owner)}</span><span class="v">${esc(T(it.owner))}</span></div>
     <div class="row"><span class="k">${T(UI.k_date)}</span><span class="v">${esc(T(it.date))}</span></div>
     <div class="row"><span class="k">${T(UI.k_place)}</span><span class="v">${esc(T(it.place))}</span></div>
     <div class="row"><span class="k">${T(UI.k_note)}</span><span class="v">${esc(T(it.note))}</span></div>
     <div class="row"><span class="k">${T(UI.k_kept)}</span><span class="v">${esc(kept)}</span></div>
     <div class="stampmark ${it.done?'done':''}">${T(it.done?UI.picked:UI.keeping)}</div>
   </div>
   <div class="sec">${it.done ? (lang==='ja'?'受け取りの記録':'The pickup record') : T(UI.nextdoor)}</div>
   <a class="neighbor" href="#/sci/${it.id}">${img(s.img, T(s.name))}<div><div class="t">${esc(T(s.name))}</div><div class="s">${lang==='ja'?'窓口の者がご案内します ›':'Let me show you ›'}</div></div></a>
   <a class="btn" href="#/sci/${it.id}">${it.done ? (lang==='ja'?'どうやって受け取ったか見る':'See how it was picked up') : T(UI.toScience)}</a>
   ${it.done ? '' : `<a class="btn light" href="#/pickup/${it.id}">${T(UI.pickup)}</a>`}
   ${srcList(it.src)}`;
}

/* ---------- science scenes ---------- */
function sci(id){
  const it = ITEMS.find(x=>x.id===id); if(!it) return home();
  const s = SCI[it.next];
  setCall(it.no.slice(1));
  let body = '';
  if (it.next==='laser') body = labLaser();
  if (it.next==='quake') body = labQuake();
  if (it.next==='weight') body = labWeight();
  if (it.next==='surveyor') body = labSurveyor();
  view.innerHTML = `<a class="back" href="#/item/${it.id}">${T(UI.backItem)}</a>` + clerk(T(s.clerk)) +
   `<figure style="margin:0 0 6px">${img(s.img, T(s.cap))}<figcaption>${esc(T(s.name))} — ${esc(T(s.cap))}（NASA）</figcaption></figure>` +
   body + (it.done ? '' : `<a class="btn light" href="#/pickup/${it.id}">${T(UI.pickup)}</a>`) + srcList(s.src);
  wire(it.next);
}

function labLaser(){
  return `<div class="lab"><h3>${lang==='ja'?'実験：月までレーザーを撃つ':'Try it: fire a laser at the Moon'}</h3>
   <svg viewBox="0 0 320 90" aria-hidden="true"><circle cx="30" cy="45" r="22" fill="#3b7dd8"/><circle cx="292" cy="45" r="12" fill="#d9d4c7"/>
   <line x1="52" y1="45" x2="280" y2="45" stroke="#334" stroke-dasharray="3 5"/><circle id="beam" cx="52" cy="45" r="5" fill="#ff4d4d"/></svg>
   <div class="readout" id="lr">0.00 s</div>
   <button class="btn" id="fire" type="button">${lang==='ja'?'レーザー発射！':'Fire!'}</button>
   <div class="reveal" id="lrv"><p>${lang==='ja'
     ? '光が<b>約2.5秒</b>で帰ってきました。光の速さ × 時間 ÷ 2 で、月までの距離が<b>数ミリ〜数センチ</b>の細かさでわかります。'
     : 'The light came back in about <b>2.5 seconds</b>. Speed of light × time ÷ 2 gives the distance to the Moon to within <b>millimetres to centimetres</b>.'}</p></div></div>
   <div class="reveal" id="lr2"><ul class="facts">
    <li><span class="n">1</span><span>${lang==='ja'?'鏡は、3枚の鏡を角で合わせた<b>「コーナーキューブ」100個</b>でできています。どこから光が来ても、来た方向へそのまま返します。':'The panel holds <b>100 “corner cubes”</b>. Light that enters one goes straight back the way it came.'}</span></li>
    <li><span class="n">2</span><span>${lang==='ja'?'50年以上測り続けてわかったこと：<b>月は1年に約3.8cmずつ、地球から遠ざかっています。</b>つめがのびるのと同じくらいの速さです。':'Fifty-plus years of measurements show <b>the Moon drifts about 3.8 cm farther from Earth every year</b> — about as fast as your fingernails grow.'}</span></li>
    <li><span class="n">3</span><span>${lang==='ja'?'電気がいらないので、置いた日から今まで<b>一度も休まず</b>働いています。':'It needs no power, so it has <b>never stopped working</b>.'}</span></li></ul>
   <div class="lab"><label>${lang==='ja'?'あなたは何歳？':'How old are you?'} <input id="age" type="number" min="0" max="120" inputmode="numeric" value="10"></label>
   <div class="readout" id="ageo"></div><p id="agep" style="text-align:center"></p></div></div>`;
}
function labQuake(){
  return `<div class="lab"><h3>${lang==='ja'?'実験：月をコツンとたたく':'Try it: knock on the Moon'}</h3>
   <svg viewBox="0 0 320 150" aria-label="${lang==='ja'?'地球と月のゆれの比較':'Earth vs Moon shaking'}" role="img">
    <text x="4" y="14" fill="#9fb0d8" font-size="11">${lang==='ja'?'地球（ふつうの岩）':'Earth (ordinary rock)'}</text>
    <polyline id="wE" fill="none" stroke="#7fb3ff" stroke-width="1.6" points=""/>
    <text x="4" y="86" fill="#ffd84a" font-size="11">${lang==='ja'?'月':'Moon'}</text>
    <polyline id="wM" fill="none" stroke="#ffd84a" stroke-width="1.6" points=""/>
    <text x="250" y="146" fill="#9fb0d8" font-size="10">${lang==='ja'?'時間 →':'time →'}</text></svg>
   <button class="btn" id="knock" type="button">${lang==='ja'?'コツン！':'Knock!'}</button>
   <div class="reveal" id="qrv"><p>${lang==='ja'
    ? '1969年、アポロ12号の使い終わった船体が月に落ちると、月は<b>約55分</b>もゆれ続けました。まるで<b>鐘</b>のように。地球なら、すぐにおさまります。'
    : 'In 1969, when Apollo 12’s used spacecraft hit the Moon, the Moon kept shaking for <b>about 55 minutes</b> — like a <b>bell</b>. On Earth it would fade quickly.'}</p>
    <p>${lang==='ja'?'なぜ？ 月の中は<b>カラカラに乾いていて</b>、ゆれを吸い取る水がほとんどないからです。（グラフは説明のためのイメージです）':'Why? The inside of the Moon is <b>bone-dry</b>, with almost no water to soak up the shaking. (Graph is an illustration.)'}</p></div></div>
   <div class="reveal" id="q2"><ul class="facts">
    <li><span class="n">1</span><span>${lang==='ja'?'地震計は月の上で<b>1977年9月30日</b>まで、地球へ記録を送り続けました。':'The seismometers sent data to Earth until <b>30 September 1977</b>.'}</span></li>
    <li><span class="n">2</span><span>${lang==='ja'?'ゆれの伝わり方を調べると、月の中は地球と同じように<b>地殻・マントル・核</b>の層に分かれていることがわかってきました。':'From how the shaking travelled, scientists learned the Moon is layered like Earth: <b>crust, mantle and core</b>.'}</span></li></ul>
    <svg viewBox="0 0 200 120" style="width:60%;margin:10px auto;display:block" role="img" aria-label="${lang==='ja'?'月の中の層':'Layers inside the Moon'}">
     <circle cx="60" cy="60" r="55" fill="#cfc3a8" stroke="#3b3326" stroke-width="2"/><circle cx="60" cy="60" r="48" fill="#b98a5a"/><circle cx="60" cy="60" r="16" fill="#b84a3a"/>
     <text x="125" y="20" font-size="12" fill="#3b3326">${lang==='ja'?'地殻':'crust'}</text><text x="125" y="60" font-size="12" fill="#3b3326">${lang==='ja'?'マントル':'mantle'}</text><text x="125" y="100" font-size="12" fill="#3b3326">${lang==='ja'?'核':'core'}</text>
     <line x1="114" y1="16" x2="112" y2="30" stroke="#3b3326"/><line x1="122" y1="56" x2="100" y2="56" stroke="#3b3326"/><line x1="122" y1="96" x2="70" y2="66" stroke="#3b3326"/></svg></div>`;
}
function labWeight(){
  return `<div class="lab"><h3>${lang==='ja'?'実験：月の体重計':'Try it: a Moon bathroom scale'}</h3>
   <label>${lang==='ja'?'地球での体重':'Your weight on Earth'} <input id="kg" type="number" min="1" max="200" inputmode="numeric" value="30"> kg</label>
   <div class="readout" id="kgo"></div>
   <p>${lang==='ja'?'月の重力は地球の<b>約6分の1</b>。月では体重計の数字が6分の1になります。':'Moon gravity is about <b>one-sixth</b> of Earth’s, so a scale reads one-sixth.'}</p>
   <button class="btn" id="why" type="button">${lang==='ja'?'じゃあ、なぜ袋を置いていったの？':'Then why leave the bags?'}</button>
   <div class="reveal" id="wrv"><p>${lang==='ja'
    ? '軽くなっても、月から飛び立つには燃料が要ります。積める重さは決まっていました。<b>袋や道具を置いていくほど、持ち帰れる月の石が増えた</b>のです。'
    : 'Even on the Moon, lifting off takes fuel, and the weight the lander could carry was fixed. <b>Every bag and tool left behind meant more Moon rock could come home.</b>'}</p></div></div>
   <div class="reveal" id="w2"><ul class="facts">
    <li><span class="n">1</span><span>${lang==='ja'?'帰りは着陸船の<b>上半分だけ</b>が飛び立ち、下半分は発射台として月に残りました。':'Only the <b>top half</b> of the lander took off; the bottom half stayed as the launch pad.'}</span></li>
    <li><span class="n">2</span><span>${lang==='ja'?'いま、この袋を<b>取りに行きたい</b>という科学者もいます。中の微生物が、月で50年以上生きのびられたのかを調べるためです。':'Some scientists would <b>love to collect these bags</b> — to see whether any microbes inside survived 50+ years on the Moon.'}</span></li></ul></div>`;
}
function labSurveyor(){
  return `<div class="lab"><h3>${lang==='ja'?'受け取りの記録':'The pickup record'}</h3>
   <ul class="facts" style="color:var(--ink)">
    <li><span class="n">1</span><span>${lang==='ja'?'<b>1967年4月20日</b>　人の乗っていない探査機サーベイヤー3号が着陸。アームで月の土を掘り、<b>ぬれた砂くらいの固さ</b>だと確かめました。':'<b>20 Apr 1967</b> — robotic Surveyor 3 lands, digs the soil with its arm and finds it is about as firm as <b>wet sand</b>.'}</span></li>
    <li><span class="n">2</span><span>${lang==='ja'?'<b>1969年11月</b>　アポロ12号が、わずか<b>約180m</b>はなれた所にねらって着陸。2人が歩いて受け取りに行きました。':'<b>Nov 1969</b> — Apollo 12 lands just <b>about 180 m</b> away, on purpose. Two astronauts walk over.'}</span></li>
    <li><span class="n">3</span><span>${lang==='ja'?'カメラなど<b>約10kg</b>の部品を持ち帰り、地球で調べました。月に<b>2年半</b>置かれた物がどう変わるかを知るためです。':'They bring back about <b>10 kg</b> of parts, including the camera, to study how <b>2½ years</b> on the Moon changed them.'}</span></li></ul>
   <p>${lang==='ja'?'ねらった場所に正確に着陸できることも、この「受け取り」で証明されました。':'This pickup also proved a crew could land exactly where they aimed.'}</p></div>`;
}

function wire(kind){
  const $ = id => document.getElementById(id);
  if (kind==='laser'){
    const beam=$('beam'), lr=$('lr');
    $('fire').onclick = () => {
      $('fire').disabled = true; const t0=performance.now(), D=2500;
      const step = now => { const t=Math.min(1,(now-t0)/D); const x = t<.5 ? 52+456*t : 280-456*(t-.5);
        beam.setAttribute('cx', x); lr.textContent=(2.5*t).toFixed(2)+' s';
        if(t<1) requestAnimationFrame(step); else { $('fire').disabled=false; $('lrv').classList.add('on'); $('lr2').classList.add('on'); age(); } };
      requestAnimationFrame(step);
    };
    const age = () => { const a=Math.max(0,Math.min(120,+$('age').value||0)); const cm=(a*3.8).toFixed(1);
      $('ageo').textContent = '+'+cm+' cm';
      $('agep').textContent = lang==='ja' ? `あなたが生まれてから、月は約${cm}cm遠くなりました。受け取りに来るのが遅いほど、少しずつ遠くなります。` : `Since you were born, the Moon has moved about ${cm} cm farther away. The longer you wait, the longer the trip.`; };
    $('age').oninput = age;
  }
  if (kind==='quake'){
    const draw = (el, base, amp, rise, decay, t) => { let pts=[]; for(let i=0;i<=300*t;i+=2){ const x=10+i; const e = i<rise ? i/rise : Math.exp(-(i-rise)/decay); pts.push(`${x},${(base+Math.sin(i*1.7)*amp*e*(0.6+0.4*Math.sin(i*.37))).toFixed(1)}`);} el.setAttribute('points',pts.join(' ')); };
    $('knock').onclick = () => { const t0=performance.now(), D=3000;
      const step = now => { const t=Math.min(1,(now-t0)/D); draw($('wE'),45,22,4,10,t); draw($('wM'),115,22,40,120,t);
        if(t<1) requestAnimationFrame(step); else { $('qrv').classList.add('on'); $('q2').classList.add('on'); } };
      requestAnimationFrame(step); };
  }
  if (kind==='weight'){
    const f = () => { const kg=Math.max(0,+$('kg').value||0); $('kgo').textContent = (kg/6).toFixed(1)+' kg'; };
    $('kg').oninput=f; f();
    $('why').onclick = () => { $('wrv').classList.add('on'); $('w2').classList.add('on'); };
  }
}

/* ---------- pickup ---------- */
function pickup(id, way){
  const it = ITEMS.find(x=>x.id===id); if(!it || it.done) return home();
  setCall(it.no.slice(1));
  const w = WAYS.find(x=>x.k===way) || WAYS[0];
  const fmt = h => { if (h < 1/60) return (h*3600).toFixed(1)+(lang==='ja'?'秒':' s');
    if (h < 24*2) return Math.round(h)+(lang==='ja'?'時間':' h');
    if (h < 24*365) return Math.round(h/24)+(lang==='ja'?'日':' days');
    return (h/24/365.25).toFixed(1)+(lang==='ja'?'年':' years'); };
  const arr = new Date(Date.now() + w.h*3600*1000);
  const ds = lang==='ja' ? `${arr.getFullYear()}年${arr.getMonth()+1}月${arr.getDate()}日` : arr.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
  view.innerHTML = `<a class="back" href="#/item/${it.id}">${T(UI.backItem)}</a>` +
   clerk(lang==='ja' ? `<b>${esc(T(it.name))}</b>のお受け取りですね。<br>お渡しは<b>月の上</b>になります。` : `Picking up <b>${esc(T(it.name))}</b>?<br>Handover is <b>on the Moon</b>.`) +
   `<div class="sec">${T(UI.chooseWay)}</div>
   ${WAYS.map(x=>`<button class="opt" type="button" aria-pressed="${x.k===w.k}" data-k="${x.k}"><span class="r"></span><span class="m">${T(x)}</span><span class="d">${fmt(x.h)}</span></button>`).join('')}
   <div class="claim"><div>${T(UI.arrive)}</div><div class="y">${ds}</div>
    ${w.note?`<div style="font-size:13px">${esc(T(w.note))}</div>`:''}<small>${T(UI.assume)}</small></div>
   <p class="note">${T(UI.onlyHere)}</p>
   <a class="btn light" href="#/sci/${it.id}">${lang==='ja'?'となりの機械も見ていく':'See the machine next door'}</a>`;
  view.querySelectorAll('.opt').forEach(b => b.onclick = () => { location.hash = `#/pickup/${it.id}/${b.dataset.k}`; });
}

function sources(){
  const all = [];
  ITEMS.forEach(it => { all.push([T(it.name), it.src]); all.push([T(SCI[it.next].name), SCI[it.next].src]); });
  view.innerHTML = `<div class="page"><a class="back" href="#/">${T(UI.back)}</a><h2>${T(UI.sources)}</h2>
   <p>${lang==='ja'?'写真はすべて NASA の公開画像です（NASA Image and Video Library）。NASA はこの作品を推奨・後援していません。':'All photos are public NASA images (NASA Image and Video Library). NASA does not endorse this project.'}</p>
   ${all.map(([n,s])=>`<h3 style="font-size:15px;margin:14px 0 4px">${esc(n)}</h3><ul>${s.map(([t,u])=>`<li><a href="${u}" target="_blank" rel="noopener">${esc(t)}</a></li>`).join('')}</ul>`).join('')}
   <h3 style="font-size:15px;margin:14px 0 4px">${lang==='ja'?'計算の前提':'Assumptions'}</h3><p>${T(UI.assume)} ${lang==='ja'?'光の片道は 384,400km ÷ 秒速約30万km ≒ 1.3秒。':'Light one way: 384,400 km ÷ ~300,000 km/s ≈ 1.3 s.'}</p></div>`;
}
function about(){
  view.innerHTML = `<div class="page"><a class="back" href="#/">${T(UI.back)}</a><h2>${T(UI.about)}</h2>
  ${lang==='ja' ? `<p>NASA Space Apps Challenge 2026「Abandoned but not Forgotten」への作品です（チーム SunSunWorld／串本会場）。</p>
   <p>月に残された物を「落とし物」として窓口で預かっている、という見立てで、子どもがゴルフボールや家族写真から入り、となりに置かれた機械と、その機械がわかったこと（月までの距離、月の地震、重さ）にたどり着けるようにしました。</p>
   <p><b>AI の利用：</b>文章の下書きとプログラムは AI（Anthropic の Claude）の支援で作り、チームが内容を確認しました。写真はすべて NASA の本物で、AI で作った画像は使っていません。事実は出典ページの NASA などの資料で確認しています。</p>
   <p>ソースコード：Apache License 2.0</p>`
  : `<p>An entry for NASA Space Apps Challenge 2026, “Abandoned but not Forgotten” (Team SunSunWorld, Kushimoto).</p>
   <p>The things left on the Moon are treated as items at a lost-and-found counter. Kids come in through a golf ball or a family photo, then meet the machine kept next to it and what that machine discovered: the distance to the Moon, moonquakes, and weight.</p>
   <p><b>Use of AI:</b> Draft text and code were made with help from AI (Anthropic’s Claude) and checked by the team. All photos are real NASA images; no AI-generated images are used. Facts are checked against NASA and other sources listed on the Sources page.</p>
   <p>Source code: Apache License 2.0</p>`}</div>`;
}

function route(){
  document.documentElement.lang = lang;
  document.title = T(UI.title) + (lang==='ja' ? ' — Lunar Lost & Found' : '');
  document.getElementById('signTitle').textContent = T(UI.title);
  document.getElementById('langBtn').textContent = lang==='ja' ? 'EN' : '日本語';
  document.getElementById('callLabel').textContent = T(UI.call);
  document.getElementById('lnkSources').textContent = T(UI.sources);
  document.getElementById('lnkAbout').textContent = T(UI.about);
  const p = location.hash.replace(/^#\/?/,'').split('/');
  if (p[0]==='item') item(p[1]);
  else if (p[0]==='sci') sci(p[1]);
  else if (p[0]==='pickup') pickup(p[1], p[2]);
  else if (p[0]==='sources') sources();
  else if (p[0]==='about') about();
  else home();
  window.scrollTo(0,0); view.focus({preventScroll:true});
}
document.getElementById('langBtn').onclick = () => { lang = lang==='ja'?'en':'ja'; try{localStorage.setItem('lf-lang',lang);}catch(e){} route(); };
window.addEventListener('hashchange', route);
route();
})();
