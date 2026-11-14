// "Try driving a Mars rover like an RC car." Round 1 lets you feel why a joystick cannot work with a signal delay.
// Round 2 is how rover drivers really did it: plan the day's moves, send them at once, and let the rover check for hazards itself.
// The delay (2 seconds stands for 20 minutes) and the rock positions are made up for the game. The facts are real (sources on the post).
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const btn = (cls, text, fn) => { const b = el('button', cls, text); b.type = 'button'; b.onclick = fn; return b; };
const LAG = 2000;          // one way, on screen. On the real Mars: 3 to 22 minutes
const V = 0.11, X0 = 0.07, HIT = 0.07, CAM = 0.2, NEAR = 0.13;   // round 1, in fractions of the track width
const ROVER = '<svg viewBox="0 0 40 40" aria-hidden="true"><g fill="#3a3a3a" stroke="#8d8d8d" stroke-width=".7"><rect x="4" y="5" width="6" height="9" rx="2.5"/><rect x="4" y="16" width="6" height="9" rx="2.5"/><rect x="4" y="27" width="6" height="9" rx="2.5"/><rect x="30" y="5" width="6" height="9" rx="2.5"/><rect x="30" y="16" width="6" height="9" rx="2.5"/><rect x="30" y="27" width="6" height="9" rx="2.5"/></g><path d="M12 13h16l5 9-5 12H12L7 22z" fill="#27407a" stroke="#a9bdea" stroke-width="1"/><path d="M11 18h18M9 23h22M11 28h18M20 13v21" stroke="#a9bdea" stroke-width=".6" opacity=".75"/><rect x="15.5" y="3" width="9" height="11" rx="2.5" fill="#eadfc4"/><circle cx="20" cy="8" r="2.6" fill="#fff"/><circle cx="20" cy="8" r="1.1" fill="#1b1b1b"/></svg>';

const TX = {
  ja: {
    title: '火星の車を\nラジコンで運転してみた', sub: '電波がとどくまで、片道20分。岩の手前で止められる？', start: 'やってみる', note: '※ゲームでは、20分を2秒にちぢめています',
    earth: '地球', mars: '火星', r1: 'ROUND 1　ラジコン方式', r1task: '岩の手前で「止まれ」を押そう', screen: 'きみの画面（20分前の火星）', real: '本物',
    go: '進め', stop: '止まれ', ready: '「進め」を押すとスタート', sending: '「進め」を送信中… 火星にとどくまで20分', waiting: '本物は走りだした。でも、それが画面にうつるのは20分後',
    driving: '走っている。岩はどこだ…？', stopping: '「止まれ」を送信中… とどくまで20分',
    crash: 'ドン！ 岩にぶつかった', crashWhy: 'きみの画面に岩がうつったとき、本物のローバーは、もうぶつかっていた。',
    early: '止まった。でも、岩はまだ先', earlyWhy: '岩が見える前に止めるしかない。それでは、どこにも行けない。',
    lucky: '止まれた！ …でも、それは運', luckyWhy: '岩が画面にうつる前に「止まれ」を押したはず。岩の場所を知らない本物の火星では、できない。',
    fact1: '本物の火星では、電波は片道3〜22分。だから、ラジコンのようには運転できない。', again: 'もう1回（本物の位置も見る）', next: 'じゃあ、どうやって？ ▶',
    r2: 'ROUND 2　NASA 方式', r2task: '1日分の命令を、まとめて送る', sol: n => `火星の${n}日目`, r2hint: '矢印で道を作って、★の岩まで行こう', count: n => `命令 ${n}/6`,
    send: 'まとめて送信', undo: '1つ消す', dir: { u: '上へ', r: '右へ', d: '下へ', l: '左へ' },
    full: 'このゲームでは、1日に6個まで', edge: 'そこは地図の外', isRock: 'そこは岩。地図に見えている', already: 'もう★に着く道ができている。送信しよう',
    r2sending: '命令を送信中… 火星にとどくまで20分', running: 'ローバーが、命令を1つずつ進めている',
    hazard: 'ストップ！ カメラが岩を見つけて、自分で止まった', hazard2: '地図になかった岩だった。つづきの命令は、次の日に送る', dayEnd: '今日の命令はここまで。つづきは、次の日に送る',
    arrived: n => `到着！ 火星の${n}日目でクリア`, cleared: n => `クリア（火星の${n}日目）`, finTitle: 'これが本当のやり方',
    facts: ['火星ローバーにジョイスティックはない。運転する人は、次の日の命令をまとめて送った', 'ローバーは2つのカメラで岩や坂を見つけて、自分でよけたり、止まったりした'],
    cap: '本物の写真：オポチュニティのタイヤのあと（2011年）。約1.2mごとに向きを変えて、カメラで道を確かめたので、模様がついた（NASA/JPL-Caltech）',
    picAlt: '火星の砂の上につづく2本のタイヤのあと。同じ間かくで模様がついている', retry: 'もう1回', share: 'シェア', copied: 'コピーしました',
    shareText: n => `火星ローバーを「NASA 方式」で運転して、火星の${n}日目でクリアした`,
  },
  en: {
    title: 'I drove a Mars rover\nlike an RC car', sub: 'The signal takes 20 minutes each way. Can you stop before the rock?', start: 'Try it', note: 'In this game, 20 minutes takes 2 seconds',
    earth: 'Earth', mars: 'Mars', r1: 'ROUND 1: RC-car style', r1task: 'Press STOP just before the rock', screen: 'Your screen (Mars, 20 minutes ago)', real: 'REAL',
    go: 'GO', stop: 'STOP', ready: 'Press GO to start', sending: 'Sending GO… 20 minutes to reach Mars', waiting: 'The real rover is moving. Its picture reaches you 20 minutes later',
    driving: 'Driving. Where is the rock…?', stopping: 'Sending STOP… 20 minutes to reach Mars',
    crash: 'CRASH! It hit the rock', crashWhy: 'When the rock showed up on your screen, the real rover had already hit it.',
    early: 'It stopped. But the rock is still far away', earlyWhy: 'The only safe way is to stop before you can see the rock. That gets you nowhere.',
    lucky: 'You stopped in time! …by luck', luckyWhy: 'You must have pressed STOP before the rock showed up. On the real Mars, where nobody knows where the rocks are, that cannot work.',
    fact1: 'On the real Mars, a signal takes 3 to 22 minutes each way. That is why nobody can drive a rover like an RC car.', again: 'Again (show the real rover too)', next: 'So how did they do it? ▶',
    r2: 'ROUND 2: The NASA way', r2task: 'Plan the day, then send', sol: n => `Mars day ${n}`, r2hint: 'Use the arrows to plan a path to the ★ rock', count: n => `Commands ${n}/6`,
    send: 'Send them all', undo: 'Undo', dir: { u: 'Up', r: 'Right', d: 'Down', l: 'Left' },
    full: 'In this game: six commands a day, max', edge: 'That is off the map', isRock: 'That is a rock. You can see it on the map', already: 'Your path already reaches the ★. Send it!',
    r2sending: 'Sending the commands… 20 minutes to reach Mars', running: 'The rover is running your commands, one by one',
    hazard: 'STOP! Its cameras spotted a rock, so it stopped itself', hazard2: 'That rock was not on the map. The next commands go up the next day', dayEnd: 'That is all for today. The next commands go up the next day',
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
  const ping = (link, cls) => { const d = el('i', 'lg-dot' + (cls ? ' ' + cls : '')); link.children[1].append(d); later(() => d.remove(), LAG + 60); };

  function intro() {
    frame(rover('lg-hero'), lines('h2', 'sd-title', X.title), say(el('p', 'sd-sub'), X.sub), btn('sd-start', X.start, () => round1(false)), el('p', 'sd-note', X.note));
    play(false);
    const bg = el('img', 'lg-bg'); bg.src = 'media/lag/tracks.jpg'; bg.alt = ''; box.prepend(bg, el('div', 'sd-shade'));
  }

  // Round 1: what you see is LAG old, and what you press arrives LAG later.
  function round1(ghost) {
    play(true);
    const R = 0.56 + Math.random() * 0.28;
    const scr = el('div', 'lg-scr'), rov = rover('lg-rov'), real = rover('lg-rov lg-real'), rock = el('i', 'lg-rock'), boom = el('i', 'lg-boom', '💥');
    real.append(el('em', '', X.real)); real.hidden = !ghost; rock.hidden = boom.hidden = true; rock.style.left = R * 100 + '%';
    scr.append(el('span', 'lg-lab', X.screen), rock, real, rov, boom);
    const link = wire(), msg = status(X.ready), row = el('div', 'lg-row');
    const go = btn('lg-big go', X.go, () => { go.disabled = true; st.disabled = false; tGo = performance.now() + LAG; ping(link); tick(); });
    const st = btn('lg-big stop', X.stop, () => { st.disabled = true; pressed = true; tStop = performance.now() + LAG; ping(link, 'red'); });
    st.disabled = true; row.append(go, st);
    const w = frame(el('p', 'lg-round', X.r1), el('h2', 'lg-task', X.r1task), scr, link, msg, row);
    let tGo = Infinity, tStop = Infinity, pressed = false;
    const tCrash = () => tGo + (R - HIT - X0) / V * 1000;
    const trueX = t => t <= tGo ? X0 : Math.min(X0 + V * (Math.min(t, tStop) - tGo) / 1000, R - HIT);
    const put = (e, x) => { e.style.left = x * 100 + '%'; };
    put(rov, X0); put(real, X0);
    function tick() {
      const now = performance.now(), end = Math.min(tCrash(), tStop), xs = trueX(now - LAG);
      put(real, trueX(now)); put(rov, xs);
      if (xs >= R - CAM) rock.hidden = false;
      say(msg, pressed ? X.stopping : now < tGo ? X.sending : now < tGo + LAG ? X.waiting : X.driving);
      if (now >= end + LAG) return finish(tStop < tCrash() ? (trueX(tStop) >= R - HIT - NEAR ? 'lucky' : 'early') : 'crash');
      raf = requestAnimationFrame(tick);
    }
    function finish(kind) {
      rock.hidden = false;
      if (kind === 'crash') { boom.hidden = false; boom.style.left = (R - 0.02) * 100 + '%'; }
      link.remove(); msg.remove(); row.remove();
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
      for (const k in keys) keys[k].disabled = busy;
    }
    function add(k) {
      if (busy) return;
      const p = path(), [c0, r0] = p.length ? p[p.length - 1] : pos, c = c0 + DIRS[k][0], r = r0 + DIRS[k][1];
      if (c0 === T[0] && r0 === T[1]) return toast(X.already);
      if (plan.length >= 6) return toast(X.full);
      if (c < 0 || r < 0 || c >= N || r >= N) return toast(X.edge);
      if (rocks.has(c + ',' + r)) return toast(X.isRock);
      plan.push(k); draw();
    }
    function run() {
      if (busy || !plan.length) return;
      busy = true; draw(); say(msg, X.r2sending); ping(link);
      later(function step() {
        if (!plan.length) return nextSol(X.dayEnd);
        const k = plan[0], c = pos[0] + DIRS[k][0], r = pos[1] + DIRS[k][1], goal = c === T[0] && r === T[1];
        face(DIRS[k][2]); say(msg, X.running);
        if (!surprise && pos[1] === 1 && r <= 1 && !goal) {      // just past the wall: a rock the map did not show
          surprise = true; rocks.add(c + ',' + r); plan = []; draw(); cells[r * N + c].classList.add('new'); rv.classList.add('halt'); say(msg, X.hazard);
          return later(() => { rv.classList.remove('halt'); nextSol(X.hazard2); }, 2800);
        }
        pos = [c, r]; plan.shift(); draw();
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
