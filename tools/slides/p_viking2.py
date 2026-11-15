"""Viking 2 x room tour: 'Living alone on Mars, year 50. Rent $0, great view, but the floor is tilted.'"""
from lib import *
DIR = 'viking2'
V2 = 'https://science.nasa.gov/mission/viking-2/'
BLUR = 'blur(16px) brightness(.5) saturate(1.1)'
CSS = '''
.ph img.c{object-fit:cover}
.plan{background:#fdfdf8;border-radius:22px;padding:6px 10px 0;box-shadow:0 14px 40px rgba(0,0,0,.6);width:860px}
.plan svg{display:block;width:100%}
.plan text{font-family:'Noto Sans CJK JP','Noto Sans',sans-serif;font-weight:900;fill:#161616}
.info{padding:22px 34px}
.info .row{font-size:38px;padding:12px 0}.info .row span{font-size:31px}
.tilt{background:#fdfdf8;border-radius:22px;box-shadow:0 14px 40px rgba(0,0,0,.6);width:860px}
'''
def photo(nid, cap_ja, cap_en, w=860, rot=-1.5, hgt=None, pos='50% 50%'):
    st = f'height:{hgt}px;object-position:{pos}' if hgt else ''
    return f'<figure class="ph" style="width:{w}px;transform:rotate({rot}deg)"><img class="c" style="{st}" src="file://{ASSETS}/{nid}.jpg"><figcaption>{t(cap_ja, cap_en)}</figcaption></figure>'
def plan():
    """Our own drawing: a simple top view of the lander, in the style of a floor plan."""
    L = lambda ja, en, x, y, a='middle', s=30: f'<text x="{x}" y="{y}" text-anchor="{a}" font-size="{s}">{t(ja, en)}</text>'
    return f'''<div class="plan"><svg viewBox="0 0 840 500" width="840" height="500">
  <g fill="none" stroke="#161616" stroke-width="7" stroke-linejoin="round">
    <polygon points="420,110 560,190 560,330 420,410 280,330 280,190" fill="#eef3f8"/>
    <line x1="420" y1="410" x2="420" y2="462"/><circle cx="420" cy="472" r="16" fill="#fff"/>
    <line x1="280" y1="190" x2="226" y2="158"/><circle cx="214" cy="151" r="16" fill="#fff"/>
    <line x1="560" y1="190" x2="614" y2="158"/><circle cx="626" cy="151" r="16" fill="#fff"/>
    <circle cx="360" cy="340" r="24" fill="#ffd21f"/><circle cx="480" cy="340" r="24" fill="#ffd21f"/>
    <circle cx="420" cy="230" r="44" fill="#fff"/><line x1="420" y1="186" x2="420" y2="274"/><line x1="376" y1="230" x2="464" y2="230"/>
    <rect x="300" y="170" width="54" height="34" rx="8" fill="#ff8a65"/><rect x="486" y="170" width="54" height="34" rx="8" fill="#ff8a65"/>
    <polyline points="500,372 610,430 700,404" stroke-width="9"/>
  </g>
  <g stroke="#e5202a" stroke-width="4"><line x1="198" y1="62" x2="642" y2="62"/><line x1="198" y1="46" x2="198" y2="78"/><line x1="642" y1="46" x2="642" y2="78"/></g>
  {L('約3m', 'about 3 m (10 ft)', 420, 48, s=34)}
  {L('アンテナ', 'Antenna', 420, 300, s=26)}
  {L('カメラ×2', '2 cameras', 148, 350, 'middle')}<line x1="226" y1="342" x2="334" y2="340" stroke="#161616" stroke-width="3"/>
  {L('原子力電池×2', '2 nuclear batteries', 150, 240, 'middle', t(27, 22))}<line x1="246" y1="222" x2="298" y2="194" stroke="#161616" stroke-width="3"/>
  {L('ロボットアーム', 'Robot arm', 690, 462, 'middle')}
  {L('足×3', '3 legs', 716, 160, 'middle')}
  {L('ワンルーム', 'ONE ROOM', 730, 270, 'middle', 34)}
</svg></div>'''
def tilt():
    """Our own drawing: the lander from the side, tilted on level ground."""
    return f'''<div class="tilt"><svg viewBox="0 0 860 420" width="860" height="420" style="display:block">
  <line x1="40" y1="350" x2="820" y2="350" stroke="#b5532a" stroke-width="10" stroke-linecap="round"/>
  <g transform="rotate(-8.5 430 350)" fill="#fff" stroke="#161616" stroke-width="7" stroke-linejoin="round">
    <line x1="330" y1="262" x2="262" y2="342"/><line x1="530" y1="262" x2="598" y2="342"/>
    <ellipse cx="258" cy="346" rx="30" ry="9"/><ellipse cx="602" cy="346" rx="30" ry="9"/>
    <rect x="296" y="196" width="268" height="70" rx="14" fill="#eef3f8"/>
    <rect x="330" y="140" width="34" height="58" rx="8" fill="#ffd21f"/><rect x="470" y="140" width="34" height="58" rx="8" fill="#ffd21f"/>
    <line x1="430" y1="196" x2="430" y2="120"/><path d="M372 104 Q430 150 488 104 Z"/>
  </g>
  <path d="M700 350 A270 270 0 0 0 697 310" fill="none" stroke="#e5202a" stroke-width="6"/>
  <line x1="430" y1="350" x2="800" y2="295" stroke="#e5202a" stroke-width="4" stroke-dasharray="12 10"/>
  <text x="760" y="262" text-anchor="middle" font-size="54" font-weight="900" fill="#e5202a" font-family="'Noto Sans CJK JP','Noto Sans',sans-serif">8.5°</text>
</svg></div>'''
PHOTO = 'NASA'
SLIDES = [
 dict(dur=5, alt={'ja': 'ルームツアー：火星でひとり暮らし50年目の部屋。家賃0円、築50年、ながめ良し', 'en': 'Room tour: living alone on Mars, year 50. Rent zero dollars, built in 1976, great view'},
  html=lambda: bg('ARC-1976-AC76-1011-2-15_c', '74% 50%', 1.0, 'brightness(.9)') + shade('top') + col(
    tag('ルームツアー', 'Room tour', 'pink sm'),
    h('火星でひとり暮らし<br><em>50年目</em>の部屋', 'Living alone on Mars.<br>My place, <em>year 50</em>'),
    bx('家賃0円・築50年・ながめ良し', 'Rent $0 · Built 1976 · Great view', 'sm yellow'))
   + cr('本物の写真：1976年9月7日、バイキング2号が撮影。手前は自分の体（NASA）', 'Real photo: taken by Viking 2 on Sept. 7, 1976. Its own body is in front (NASA)')),
 dict(dur=7, alt={'ja': '間取り：ワンルーム、直径およそ3メートル。カメラ2台、アンテナ、ロボットアーム、原子力電池2個、足3本。所在地は火星のユートピア平原。築50年（1976年9月3日着陸）。家賃0円', 'en': 'Floor plan: one room, about 3 meters across. Two cameras, an antenna, a robot arm, two nuclear batteries, three legs. Address: Utopia Planitia, Mars. Built in 1976 (landed Sept. 3). Rent: zero dollars'},
  html=lambda: bg('PIA00568', '50% 50%', 1.1, BLUR) + col(
    tag('間取り', 'Floor plan', 'white sm'), plan(),
    f'''<div class="card info">
      <div class="row"><span>{t("所在地", "Address")}</span><b>{t("火星・ユートピア平原", "Utopia Planitia, Mars")}</b></div>
      <div class="row"><span>{t("築年数", "Built")}</span><b>{t("50年（1976年9月3日 着陸）", "1976 (landed Sept. 3)")}</b></div>
      <div class="row"><span>{t("電気", "Power")}</span><b>{t("原子力電池（太陽いらず）", "Nuclear batteries (no sun needed)")}</b></div>
      <div class="row"><span>{t("家賃", "Rent")}</span><b style="color:#e5202a">{t("0円", "$0")}</b></div></div>''',
    f'<div class="cr" style="position:static;max-width:860px">{t("間取り図は、わたしたちが描いたイラストです（位置はだいたい）", "The floor plan is our own drawing (positions are approximate)")}</div>', style='top:300px;gap:22px')),
 dict(dur=5, alt={'ja': '窓からの景色。空はピンク。地平線は、ななめ？', 'en': 'The view from the window. A pink sky. And the horizon looks tilted'},
  html=lambda: bg('PIA00568', '50% 50%', 1.1, BLUR) + col(
    tag('窓からの景色', 'The view', 'white sm'),
    photo('PIA00568', '本物の写真：バイキング2号の最初のカラー写真（NASA/JPL）', 'Real photo: Viking 2’s first color picture (NASA/JPL)', 860, -1.2),
    h('空はピンク。<br>地平線は…<em>ななめ？</em>', 'Pink sky.<br>And the horizon is… <em>tilted?</em>', 'md'), style='top:310px;gap:30px')),
 dict(dur=5.5, alt={'ja': 'ななめなのは家のほう。着陸したら8.5度かたむいていた。本当の地面はほぼ平ら', 'en': 'It is the house that is tilted. The lander came to rest with an 8.5 degree tilt. The real ground is nearly level'},
  html=lambda: bg('PIA00568', '50% 50%', 1.1, BLUR) + col(
    tag('クセあり', 'One quirk', 'red sm'),
    h('ななめなのは<br><em>家のほう</em>', 'It’s the house<br>that is <em>tilted</em>'),
    tilt(),
    bx('着陸したら、8.5度かたむいてた', 'It landed with an 8.5° tilt', 'sm'),
    f'<div class="cr" style="position:static;max-width:860px">{t("わたしたちが描いたイラストです。本当の地面は、ほぼ平ら", "Our own drawing. The real ground is nearly level")}</div>', style='top:310px;gap:26px')),
 dict(dur=5, alt={'ja': '庭。見わたすかぎり岩。右下のまるいものは、自分の足', 'en': 'The yard. Rocks as far as you can see. The round thing at lower right is its own foot'},
  html=lambda: bg('PIA00396', '70% 50%', 1.1, BLUR) + col(
    tag('庭', 'The yard', 'white sm'),
    photo('PIA00396', '本物の写真：着陸して数分後の1枚目。1976年9月3日（NASA/JPL）', 'Real photo: its first picture, minutes after landing on Sept. 3, 1976 (NASA/JPL)', 860, 1.2, 560, '100% 50%'),
    h('見わたすかぎり<em>岩</em>', '<em>Rocks</em> as far as<br>you can see', 'md'),
    bx('右下のまるいのは、自分の足', 'The round thing at lower right is my own foot', 'sm'), style='top:310px;gap:28px')),
 dict(dur=5.5, alt={'ja': '冬。庭が白くなる。うすい水の氷、霜。1979年5月18日の本物の写真', 'en': 'In winter the yard turns white. A thin coat of water ice: frost. A real photo from May 18, 1979'},
  html=lambda: bg('PIA00571', '50% 60%', 1.1, BLUR) + col(
    tag('冬', 'In winter', 'blue sm'),
    photo('PIA00571', '本物の写真：1979年5月18日、バイキング2号が撮影（NASA/JPL）', 'Real photo: taken by Viking 2 on May 18, 1979 (NASA/JPL)', 800, -1.2, 640, '50% 70%'),
    h('庭が<em>白く</em>なる', 'The yard turns <em>white</em>', 'md'),
    bx('うすい水の氷（しも）', 'A thin coat of water ice (frost)', 'sm'), style='top:310px;gap:28px')),
 dict(dur=7, alt={'ja': '住人はバイキング2号。3年7か月、ここで火星を調べた。1980年から返事なし。でも、いまもこの部屋にいる', 'en': 'The resident is Viking 2. It studied Mars from here for 3 years and 7 months. Silent since 1980, but it still lives here'},
  html=lambda: bg('ARC-1976-AC76-1011-2-15_c', '74% 50%', 1.0, 'brightness(.5)') + shade('all') + col(
    h('住人は<br><em>バイキング2号</em>', 'The resident:<br><em>Viking 2</em>'),
    bx('3年7か月、ここで火星を調べた', 'It studied Mars from here for 3 years 7 months', 'sm'),
    bx('1980年から返事なし。<br>でも、いまもこの部屋にいる', 'Silent since 1980.<br>But it still lives here.', 'sm green'),
    bx('内見の質問はコメント欄 👇', 'Questions about the place? Comments 👇', 'sm yellow'), cls='mid', style='gap:30px')
   + f'<div class="cr" style="top:1340px">{t("本物の写真：1976年9月7日、バイキング2号が撮影（NASA）", "Real photo: taken by Viking 2 on Sept. 7, 1976 (NASA)")}</div>'),
]
POST = dict(id='viking2-roomtour-1', account='viking2_lander', place='mars', audio='media/music/local_forecast_elevator.mp3',
 caption={'ja': '火星でひとり暮らし50年目のルームツアー。家賃0円、ながめ良し。ただし床がななめ（実話） #ルームツアー #ひとり暮らし #バイキング2号',
          'en': 'Room tour: 50 years of living alone on Mars. Rent $0, great view. But the floor is tilted. (True story) #roomtour #livingalone #viking2'},
 tags=['viking2', 'mars', 'roomtour'],
 sound={'ja': 'Kevin MacLeod「Local Forecast - Elevator」(CC BY 4.0)', 'en': 'Kevin MacLeod – Local Forecast - Elevator (CC BY 4.0)'},
 comments=pinned('viking2_lander',
"""物件のくわしい説明（ぜんぶ本当）👇

■ 住人
バイキング2号の着陸機。1976年9月3日、火星のユートピア平原に着陸しました。今年で50年です。

■ 床がななめ
着陸したとき、機体が西へ8.5度かたむきました。だから写真の地平線がななめに見えます。本当の地面は、ほぼ平らです。

■ 設備
カメラ2台、土をすくうロボットアーム、地震計、天気をはかる機械、土を調べる実験室。電気は原子力電池2個なので、太陽の光がなくても動きます。大きさは直径およそ3m。

■ 冬の霜
1977年と1979年の冬、まわりの地面にうすい水の氷（霜）がつきました。最初のときは、約100日のこっていたそうです。

■ 何をした？
土をすくって、生き物のしるしを探す実験を3回。結果は「いるとも、いないとも言えない」でした。バイキングの着陸機は、2台あわせて4,500枚の写真を地球に送りました。

■ いまは？
通信は1980年4月12日まで。そのあとは返事がありません。機体は今もユートピア平原にあって、2006年には、火星を回る探査機のカメラが上空から見つけています。

※「家賃0円」と「ルームツアー」は演出です。間取り図とななめの図は、わたしたちのイラスト。写真はぜんぶ、バイキング2号が火星で撮った本物です。""",
"""About this place (all true) 👇

■ The resident
The Viking 2 lander. It landed on Utopia Planitia, Mars, on Sept. 3, 1976. That makes 50 years this year.

■ The tilted floor
When it landed, it came to rest tilted 8.5 degrees to the west. That is why the horizon looks tilted in its photos. The real ground is nearly level.

■ What it has
Two cameras, a robot arm for scooping soil, a seismometer, a weather station and a small lab for testing soil. It runs on two nuclear batteries, so it does not need sunlight. It is about 3 meters (10 feet) across.

■ Frost in winter
In the winters of 1977 and 1979, a thin coat of water ice (frost) covered the ground around it. The first time, it stayed for about 100 days.

■ What did it do?
It scooped up soil three times to look for signs of life. The result: no clear answer either way. Together, the two Viking landers sent 4,500 photos back to Earth.

■ And now?
It kept sending data until April 12, 1980. Since then, silence. It is still on Utopia Planitia, and in 2006 a camera on a Mars orbiter spotted it from above.

Note: “rent $0” and the room-tour format are ours. The floor plan and the tilt picture are our own drawings. Every photo is a real one taken on Mars by Viking 2.""") + [
  {'user': 'viking1_lander', 'text': {'ja': 'うちは6,460kmはなれた別の平原。ご近所ではないです', 'en': 'My place is on another plain, 4,000 miles away. Not exactly neighbors.'}},
  {'user': 'phoenix_lander', 'text': {'ja': 'うちの庭にも氷あります。地面の下だけど', 'en': 'My yard has ice too. Under the ground, though.'}}],
 sources=[fact('Viking 2 (NASA Science): landed Sept. 3, 1976 at Utopia Planitia, about 4,000 miles (6,460 km) from Viking 1; tilted 8.5 degrees to the west; instruments; RTG power; lander data until April 12, 1980; landers returned 4,500 photos', V2),
  pj('PIA00568', 'First Color Image of the Viking Lander 2 Site (pink sky; the horizon appears tilted because the spacecraft is tilted)', 'NASA/JPL'),
  pj('PIA00396', 'Viking Lander 2 First Picture On The Surface Of Mars (Sept. 3, 1976; footpad at lower right)', 'NASA/JPL'),
  pj('PIA00571', 'Ice on Mars Utopia Planitia Again (May 18, 1979; thin coating of water ice; earlier frost remained about 100 days)', 'NASA/JPL'),
  pj('PIA00573', 'Frost at the Viking Lander 2 Site (Sept. 25, 1977)', 'NASA/JPL'),
  pj('PIA01882', 'Viking Lander 2 Imaged from Orbit (lander about 3 meters across; located by the HiRISE camera in 2006)', 'NASA/JPL-Caltech/University of Arizona'),
  nasa_img('ARC-1976-AC76-1011-2-15', 'Viking 2: a utopian bright summer afternoon on Mars (Sept. 7, 1976)', 'NASA'),
  fact("For @phoenix_lander's comment: Phoenix (NASA Science): verified water ice in the Martian subsurface", 'https://science.nasa.gov/mission/phoenix/'),
  src('calc', 'Sept. 3, 1976 to April 12, 1980 is 3 years 7 months; 1976 to 2026 is 50 years', V2),
  music('Local Forecast - Elevator')])
