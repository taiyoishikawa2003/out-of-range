// "Try driving a Mars rover like an RC car." Round 1 lets you feel why a joystick cannot work with a signal delay.
// Round 2 is how rover drivers really did it: plan the day's moves, send them at once, and let the rover check for hazards itself.
// The delay (2 seconds stands for 20 minutes) and the rock positions are made up for the game. The facts are real (sources on the post).
import * as S from '../store.js';

const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const btn = (cls, text, fn) => { const b = el('button', cls, text); b.type = 'button'; b.onclick = fn; return b; };
const LAG = 2000;          // one way, on screen. On the real Mars: 3 to 22 minutes
const V = 0.11, X0 = 0.07, HIT = 0.07, NEAR = 0.13;   // round 1, in fractions of the track width
const ROVER = '<svg viewBox="0 0 40 40" aria-hidden="true"><g fill="#3a3a3a" stroke="#8d8d8d" stroke-width=".7"><rect x="4" y="5" width="6" height="9" rx="2.5"/><rect x="4" y="16" width="6" height="9" rx="2.5"/><rect x="4" y="27" width="6" height="9" rx="2.5"/><rect x="30" y="5" width="6" height="9" rx="2.5"/><rect x="30" y="16" width="6" height="9" rx="2.5"/><rect x="30" y="27" width="6" height="9" rx="2.5"/></g><path d="M12 13h16l5 9-5 12H12L7 22z" fill="#27407a" stroke="#a9bdea" stroke-width="1"/><path d="M11 18h18M9 23h22M11 28h18M20 13v21" stroke="#a9bdea" stroke-width=".6" opacity=".75"/><rect x="15.5" y="3" width="9" height="11" rx="2.5" fill="#eadfc4"/><circle cx="20" cy="8" r="2.6" fill="#fff"/><circle cx="20" cy="8" r="1.1" fill="#1b1b1b"/></svg>';

// Small sounds made by our team (tools/motion/make_sfx.py). They are armed by the first tap so that phones allow them later.
const SND = {};
function arm() {
  if (SND.armed) return; SND.armed = true;
  for (const n of ['send', 'tick', 'thud', 'buzz', 'chime', 'pop']) {
    const a = new Audio(`media/sfx/${n}.mp3`); a.preload = 'auto'; a.muted = true; SND[n] = a;
    const p = a.play(); if (p) p.then(() => { a.pause(); a.currentTime = 0; a.muted = false; }).catch(() => { a.muted = false; });
  }
}
const snd = n => { const a = SND[n]; if (!a || S.isMuted()) return; try { a.currentTime = 0; const p = a.play(); if (p) p.catch(() => {}); } catch {} };
const buzz = ms => { try { if (navigator.vibrate) navigator.vibrate(ms); } catch {} };

const TX = {
  ja: {
    title: '火星の車を\nラジコンで運転してみた', sub: 'ボタンを押してから車が動くのが見えるまで、往復40分。岩の手前で止められる？', start: 'やってみる', note: '※ゲームでは、20分を2秒にちぢめています',
    earth: '地球', mars: '火星', r1: 'ROUND 1　ラジコン方式', r1task: '岩の手前で止めよう', screen: '火星からの映像（20分おくれ）', real: '本物（いま）',
    go: '進め', stop: '止まれ', ready: '① 「進め」を押す', left: n => `あと ${n}分`, r2go: '② 「まとめて送信」を押す', sending: '「進め」を送った。車が動くのが見えるまで、往復40分',
    driving: '② 岩の手前で「止まれ」を押す', stopping: '「止まれ」を送った。でも、とどくまで車は走りつづける',
    crash: 'ドン！ 岩にぶつかった', crashWhy: '「止まれ」を押しても、すぐには止まらない。とどくまでのあいだ、車は走りつづけた。',
    early: '止まった。でも、岩はまだずっと先', earlyWhy: '早く押しすぎた。40分先を当てるのは、むずかしい。',
    lucky: '止まれた！ …でも、それは運', luckyWhy: '40分先を、かんで当てた。本物の火星で毎回これは、あぶなすぎる。',
    fact1: '本物の火星では、電波は片道3〜22分。だから、ラジコンのようには運転できない。', again: 'もう1回（本物の車の位置も出す）', next: 'じゃあ、どうやって？ ▶',
    r2: 'ROUND 2　NASA 方式', r2task: '道を作って、まとめて送ろう', sol: n => `火星の${n}日目`, r2hint: '① 矢印を押して、★までの道を作る（岩はよける）', count: n => `命令 ${n}/6`,
    send: 'まとめて送信', undo: '1つ消す', dir: { u: '上へ', r: '右へ', d: '下へ', l: '左へ' },
    full: '1日に送れるのは6個まで。「まとめて送信」を押そう', edge: 'そこは地図の外', isRock: 'そこは岩。地図に見えている', already: '★までの道ができた。「まとめて送信」を押そう',
    r2sending: '命令を送信中… 火星にとどくまで20分', running: 'ローバーが、命令を1つずつ進めている',
    hazard: 'ストップ！ カメラが岩を見つけて、自分で止まった', hazard2: '地図にない岩だった。よける道を作って、また送信しよう', dayEnd: '今日の命令はここまで。つづきの道を作って、また送信しよう',
    arrived: n => `到着！ 火星の${n}日目でクリア`, cleared: n => `クリア（火星の${n}日目）`, finTitle: 'これが本当のやり方',
    facts: ['火星ローバーにジョイスティックはない。運転する人は、次の日の命令をまとめて送った', 'ローバーは2つのカメラで岩や坂を見つけて、自分でよけたり、止まったりした'],
    cap: '本物の写真：オポチュニティのタイヤのあと（2011年）。約1.2mごとに向きを変えて、カメラで道を確かめたので、模様がついた（NASA/JPL-Caltech）',
    picAlt: '火星の砂の上につづく2本のタイヤのあと。同じ間かくで模様がついている', retry: 'もう1回', share: 'シェア', copied: 'コピーしました',
    shareText: n => `火星ローバーを「NASA 方式」で運転して、火星の${n}日目でクリアした`,
  },
  en: {
    title: 'I drove a Mars rover\nlike an RC car', sub: 'From pressing a button to seeing the rover move: 40 minutes, there and back. Can you stop before the rock?', start: 'Try it', note: 'In this game, 20 minutes takes 2 seconds',
    earth: 'Earth', mars: 'Mars', r1: 'ROUND 1: RC-car style', r1task: 'Stop before the rock', screen: 'Video from Mars (20 minutes late)', real: 'REAL (now)',
    go: 'GO', stop: 'STOP', ready: '1. Press GO', left: n => `${n} min to go`, r2go: '2. Press “Send them all”', sending: 'GO is on its way. You will see the rover move in 40 minutes, there and back',
    driving: '2. Press STOP before the rock', stopping: 'STOP is on its way. Until it arrives, the rover keeps driving',
    crash: 'CRASH! It hit the rock', crashWhy: 'STOP does not work right away. Until it arrived, the rover kept driving.',
    early: 'It stopped. But the rock is still far away', earlyWhy: 'You pressed too early. Guessing 40 minutes ahead is hard.',
    lucky: 'You stopped in time! …by luck', luckyWhy: 'You guessed 40 minutes ahead and got it right. On the real Mars, doing that every time is far too risky.',
    fact1: 'On the real Mars, a signal takes 3 to 22 minutes each way. That is why nobody can drive a rover like an RC car.', again: 'Again (also show where the real rover is)', next: 'So how did they do it? ▶',
    r2: 'ROUND 2: The NASA way', r2task: 'Plan a path, then send it', sol: n => `Mars day ${n}`, r2hint: '1. Press the arrows to plan a path to the ★ (go around the rocks)', count: n => `Commands ${n}/6`,
    send: 'Send them all', undo: 'Undo', dir: { u: 'Up', r: 'Right', d: 'Down', l: 'Left' },
    full: 'Six commands a day is the limit. Press “Send them all”', edge: 'That is off the map', isRock: 'That is a rock. You can see it on the map', already: 'Your path reaches the ★. Press “Send them all”',
    r2sending: 'Sending the commands… 20 minutes to reach Mars', running: 'The rover is running your commands, one by one',
    hazard: 'STOP! Its cameras spotted a rock, so it stopped itself', hazard2: 'That rock was not on the map. Plan a way around it and send again', dayEnd: 'That is all for today. Plan the rest of the path and send again',
    arrived: n => `Arrived! Cleared on Mars day ${n}`, cleared: n => `Cleared (Mars day ${n})`, finTitle: 'This is how it was really done',
    facts: ['There is no joystick for a Mars rover. Drivers sent the next day’s commands all at once', 'The rover used two cameras to spot rocks and slopes, then steered around them or stopped by itself'],
    cap: 'Real photo: Opportunity’s wheel tracks (2011). About every 1.2 m it turned to check the route with its camera, which left this pattern (NASA/JPL-Caltech)',
    picAlt: 'Two wheel tracks across Martian sand, with a repeating pattern in them', retry: 'Play again', share: 'Share', copied: 'Copied',
    shareText: n => `I drove a Mars rover the NASA way and arrived on Mars day ${n}`,
  },
};

export function mount(box, { lang, toast }) {
  const X = TX[lang] || TX.en;
  box.classList.add('lag');
  let raf = 0, timers = [];
  const post = box.closest('.post');
  const play = on => { if (post) post.classList.toggle('app-play', on); };   // while playing, the caption makes room for the game
  const later = (fn, ms) => { timers.push(setTimeout(fn, ms)); };
  const halt = () => { cancelAnimationFrame(raf); timers.forEach(clearTimeout); timers = []; };
  const frame = (...kids) => { halt(); const w = el('div', 'sd-in lg-in'); w.append(...kids); box.replaceChildren(w); return w; };
  const lines = (tag, cls, text) => { const e = el(tag, cls); text.split('\n').forEach((l, i) => { if (i) e.append(document.createElement('br')); e.append(l); }); return e; };
  const say = (e, text) => { if (e._t === text) return e; e._t = text; e.replaceChildren(); if (lang === 'ja') (text.match(/[^、。！？]+[、。！？ 　]*/g) || [text]).forEach(s => e.append(el('span', 'lg-ph', s))); else e.textContent = text; return e; };
  const status = text => { const m = el('p', 'lg-msg'); m.setAttribute('role', 'status'); return say(m, text); };
  const rover = cls => { const r = el('i', cls); r.innerHTML = ROVER; return r; };
  const wire = () => { const w = el('div', 'lg-link'); w.append(el('b', '', X.earth), el('span', 'lg-wire'), el('b', '', X.mars)); return w; };
  const ping = (link, cls, back) => { const d = el('i', 'lg-dot' + (cls ? ' ' + cls : '') + (back ? ' rt' : '')); link.children[1].append(d); later(() => d.remove(), (back ? 2 : 1) * LAG + 60); };   // back: to Mars, then the picture comes back

  function intro() {
    frame(rover('lg-hero'), lines('h2', 'sd-title', X.title), say(el('p', 'sd-sub'), X.sub), btn('sd-start', X.start, () => { arm(); round1(false); }), el('p', 'sd-note', X.note));
    play(false);
    const bg = el('img', 'lg-bg'); bg.src = 'media/lag/tracks.jpg'; bg.alt = ''; box.prepend(bg, el('div', 'sd-shade'));
  }

  // Round 1: what you see is LAG old, and what you press arrives LAG later.
  function round1(ghost) {
    play(true);
    const R = 0.62 + Math.random() * 0.24;   // the rock is on screen from the start
    const scr = el('div', 'lg-scr'), rov = rover('lg-rov'), real = rover('lg-rov lg-real'), rock = el('i', 'lg-rock'), boom = el('i', 'lg-boom', '💥');
    real.append(el('em', '', X.real)); real.hidden = !ghost; boom.hidden = true; rock.style.left = R * 100 + '%';
    scr.append(el('span', 'lg-lab', X.screen), rock, real, rov, boom);
    const link = wire(), msg = status(X.ready), cd = el('p', 'lg-cd'), row = el('div', 'lg-row');
    let cdEnd = 0;
    const go = btn('lg-big go', X.go, () => { snd('send'); go.disabled = true; go.classList.remove('lg-pulse'); tGo = performance.now() + LAG; cdEnd = tGo + LAG; ping(link, '', true); tick(); });
    const st = btn('lg-big stop', X.stop, () => { snd('send'); st.disabled = true; st.classList.remove('lg-pulse'); pressed = true; tStop = performance.now() + LAG; cdEnd = tStop + LAG; ping(link, 'red', true); });
    st.disabled = true; go.classList.add('lg-pulse'); row.append(go, st);
    const w = frame(el('p', 'lg-round', X.r1), el('h2', 'lg-task', X.r1task), scr, link, msg, cd, row);
    let tGo = Infinity, tStop = Infinity, pressed = false;
    const tCrash = () => tGo + (R - HIT - X0) / V * 1000;
    const trueX = t => t <= tGo ? X0 : Math.min(X0 + V * (Math.min(t, tStop) - tGo) / 1000, R - HIT);
    const put = (e, x) => { e.style.left = x * 100 + '%'; };
    put(rov, X0); put(real, X0);
    function tick() {
      const now = performance.now(), end = Math.min(tCrash(), tStop), xs = trueX(now - LAG);
      put(real, trueX(now)); put(rov, xs);
      const seen = now >= tGo + LAG;                                   // the rover is moving on the player's screen
      if (seen && !pressed && st.disabled) { st.disabled = false; st.classList.add('lg-pulse'); }
      say(msg, pressed ? X.stopping : seen ? X.driving : X.sending);
      cd.textContent = cdEnd > now ? X.left(Math.ceil((cdEnd - now) / 100)) : '';
      if (now >= end + LAG) return finish(tStop < tCrash() ? (trueX(tStop) >= R - HIT - NEAR ? 'lucky' : 'early') : 'crash');
      raf = requestAnimationFrame(tick);
    }
    function finish(kind) {
      snd(kind === 'crash' ? 'thud' : kind === 'lucky' ? 'chime' : 'pop'); if (kind === 'crash') buzz(120);
      if (kind === 'crash') { boom.hidden = false; boom.style.left = (R - 0.02) * 100 + '%'; }
      link.remove(); msg.remove(); cd.remove(); row.remove();
      const again = btn('sd-ghost', X.again, () => round1(true));
      w.append(el('h3', 'lg-res ' + kind, X[kind]), say(el('p', 'lg-why'), X[kind + 'Why']), say(el('p', 'lg-fact'), X.fact1), btn('sd-start lg-next', X.next, round2), again);
    }
  }

  // Round 2: plan a path on the map, send it once, and the rover runs it. A rock the map did not show makes the rover stop itself.
  function round2() {
    play(true);
    const N = 5, T = [2, 0], rocks = new Set(['1,2', '2,2', '3,2']), DIRS = { l: [-1, 0, 3, '←'], u: [0, -1, 0, '↑'], d: [0, 1, 2, '↓'], r: [1, 0, 1, '→'] };
    let pos = [2, 4], dir = 0, ang = 0, sol = 1, plan = [], surprise = false, busy = false;
    const board = el('div', 'lg-board'), cells = [], keys = {};
    for (let i = 0; i < N * N; i++) { cells.push(el('i', 'lg-cell')); board.append(cells[i]); }
    const rv = rover('lg-rv'); board.append(rv);
    const solEl = el('p', 'lg-round', ''), msg = status(X.r2hint), chips = el('div', 'lg-chips'), link = wire(), pad = el('div', 'lg-pad');
    for (const k in DIRS) { keys[k] = btn('lg-key', DIRS[k][3], () => add(k)); keys[k].setAttribute('aria-label', X.dir[k]); pad.append(keys[k]); }
    const undo = btn('lg-key lg-undo', '⌫', () => { if (!busy) { plan.pop(); draw(); } }); undo.setAttribute('aria-label', X.undo); pad.append(undo);
    const send = btn('sd-start lg-send', X.send, run);
    frame(solEl, el('h2', 'lg-task', X.r2task), board, chips, link, msg, pad, send).classList.add('lg-r2');
    const path = () => { let [c, r] = pos; return plan.map(k => { c += DIRS[k][0]; r += DIRS[k][1]; return [c, r]; }); };
    const face = d => { ang += ((d - dir + 5) % 4) - 1; dir = d; };
    function draw() {
      solEl.textContent = X.r2 + ' ・ ' + X.sol(sol);
      cells.forEach((d, i) => { const c = i % N, r = (i - c) / N; d.className = 'lg-cell' + (rocks.has(c + ',' + r) ? ' rock' : '') + (c === T[0] && r === T[1] ? ' goal' : ''); d.textContent = ''; });
      path().forEach(([c, r], i) => { const d = cells[r * N + c]; d.classList.add('pl'); if (!d.classList.contains('goal')) d.textContent = i + 1; });
      rv.style.transform = `translate(${pos[0] * 100}%,${pos[1] * 100}%) rotate(${ang * 90}deg)`;
      chips.replaceChildren(...plan.map(k => el('b', '', DIRS[k][3])), el('span', '', X.count(plan.length)));
      send.disabled = undo.disabled = busy || !plan.length;
      const pp = path(), last = pp[pp.length - 1], ready = !busy && plan.length && (plan.length >= 6 || (last[0] === T[0] && last[1] === T[1]));
      send.classList.toggle('lg-pulse', !!ready);
      if (!busy && plan.length) say(msg, ready ? X.r2go : X.r2hint);
      for (const k in keys) keys[k].disabled = busy;
    }
    function add(k) {
      if (busy) return;
      const p = path(), [c0, r0] = p.length ? p[p.length - 1] : pos, c = c0 + DIRS[k][0], r = r0 + DIRS[k][1];
      if (c0 === T[0] && r0 === T[1]) return toast(X.already);
      if (plan.length >= 6) return toast(X.full);
      if (c < 0 || r < 0 || c >= N || r >= N) return toast(X.edge);
      if (rocks.has(c + ',' + r)) return toast(X.isRock);
      plan.push(k); draw(); snd('tick');
    }
    function run() {
      if (busy || !plan.length) return;
      busy = true; draw(); say(msg, X.r2sending); ping(link); snd('send');
      later(function step() {
        if (!plan.length) return nextSol(X.dayEnd);
        const k = plan[0], c = pos[0] + DIRS[k][0], r = pos[1] + DIRS[k][1], goal = c === T[0] && r === T[1];
        face(DIRS[k][2]); say(msg, X.running);
        if (!surprise && pos[1] === 1 && r <= 1 && !goal) {      // just past the wall: a rock the map did not show
          surprise = true; rocks.add(c + ',' + r); plan = []; draw(); cells[r * N + c].classList.add('new'); rv.classList.add('halt'); say(msg, X.hazard); snd('buzz'); buzz(120);
          return later(() => { rv.classList.remove('halt'); nextSol(X.hazard2); }, 2800);
        }
        pos = [c, r]; plan.shift(); draw(); snd(goal ? 'chime' : 'tick');
        if (goal) { say(msg, X.arrived(sol)); return later(() => fin(sol), 1500); }
        later(step, 450);
      }, LAG);
    }
    function nextSol(text) { sol++; busy = false; plan = []; draw(); say(msg, text); }
    draw();
  }

  function fin(sol) {
    const im = el('img', 'lg-pic'); im.src = 'media/lag/tracks.jpg'; im.alt = X.picAlt;
    const ul = el('ul', 'sd-facts'); X.facts.forEach(f => ul.append(el('li', '', f)));
    const row = el('div', 'sd-row');
    const share = btn('sd-ghost', X.share, async () => {
      const text = X.shareText(sol), url = location.origin + location.pathname + '#/p/lag-1';
      try { if (navigator.share) await navigator.share({ text, url }); else { await navigator.clipboard.writeText(text + ' ' + url); toast(X.copied); } } catch {}
    });
    row.append(btn('sd-ghost', X.retry, intro), share);
    frame(el('p', 'lg-round', X.cleared(sol)), el('h2', 'lg-task', X.finTitle), ul, im, el('p', 'lg-cap', X.cap), row);
    try { localStorage.setItem('oor.lag', String(sol)); } catch {}
  }

  intro();
  return { activate() {}, deactivate() { halt(); intro(); } };
}
