"""Fashion check: what the machines left on the Moon and Mars are 'wearing', and the real reason for each look."""
from lib import *
DIR = 'runway'
def look(n): return f'<div class="look">LOOK {n}</div>'
SLIDES = [
 dict(dur=4.5, alt={'ja': 'NASAの機械ファッションチェック。月と火星に置いてきた機械の、こだわりポイント4つ', 'en': 'NASA machine fashion check: 4 looks from machines left on the Moon and Mars'},
  html=lambda: bg('KSC-as11-40-5927', '50% 30%', 1.0, 'brightness(.85)') + shade('top') + col(
    tag('月・火星コレクション', 'Moon & Mars Collection', 'pink sm'),
    h('NASAの機械<br><em>ファッションチェック</em>', 'NASA machines:<br><em>fashion check</em>'),
    bx('見た目には、ぜんぶ理由がある', 'Every look has a reason', 'sm'))
   + cr('本物の写真：月面のアポロ11号の着陸船（1969年、NASA）', 'Real photo: the Apollo 11 lander on the Moon (1969, NASA)')),
 dict(dur=6.5, alt={'ja': 'LOOK1：月面車の手作りの泥よけ。材料は月の地図とテープとクリップ。泥よけが割れて月の砂をあびたので、その場で直した', 'en': 'Look 1: a handmade fender on the Moon car, made of Moon maps, tape and clamps. The fender broke and Moon dust sprayed everywhere, so the astronauts fixed it on the spot'},
  html=lambda: bg('as17-137-20979', '62% 50%', 1.0) + shade('top') + col(
    look(1), h('手作りの<em>泥よけ</em>', 'A handmade <em>fender</em>'),
    bx('材料：月の地図・テープ・クリップ', 'Made of: Moon maps, tape and clamps', 'sm'),
    bx('泥よけが割れて、月の砂をあびまくった。だからその場で直した', 'The fender broke and Moon dust sprayed everywhere. So they fixed it on the spot', 'sm green'))
   + cr('本物の写真：アポロ17号の月面車（1972年、NASA）。月に置いてきた', 'Real photo: Apollo 17’s lunar rover (1972, NASA). It was left on the Moon')),
 dict(dur=6.5, alt={'ja': 'LOOK2：火星ヘリコプター・インジェニュイティ。太陽電池の下に小さな布きれ。ライト兄弟の飛行機（1903年）のつばさの布', 'en': 'Look 2: the Mars helicopter Ingenuity carries a tiny piece of cloth under its solar panel. It is wing fabric from the Wright brothers’ 1903 airplane'},
  html=lambda: bg('PIA23882', '50% 50%', 1.0, 'brightness(.92)') + shade('top') + col(
    look(2), h('かくし持った<em>布きれ</em>', 'A hidden <em>scrap of cloth</em>'),
    bx('太陽電池の下に、1.3cmの布を1枚', 'One 1.3 cm square, tucked under the solar panel', 'sm'),
    bx('ライト兄弟の飛行機（1903年）のつばさの布。地球で最初の飛行機から、火星で最初のヘリコプターへ', 'Wing fabric from the Wright brothers’ 1903 plane. First airplane on Earth → first helicopter on Mars', 'sm green'),
    )
   + f'<figure class="ph fabric"><img src="file://{ASSETS}/PIA24438.jpg"><figcaption>{t("実物の布（NASA/JPL）", "The actual fabric (NASA/JPL)")}</figcaption></figure>'
   + cr('本物の写真：地球で撮ったインジェニュイティ（NASA/JPL-Caltech）', 'Real photo: Ingenuity, photographed on Earth (NASA/JPL-Caltech)')),
 dict(dur=6.5, alt={'ja': 'LOOK3：火星の着陸機インサイトの全身砂まみれコーデ。2018年はきれい、2022年は砂だらけ。太陽電池に砂がつもると電気が作れず、2022年に通信が終わった', 'en': 'Look 3: the InSight lander’s head-to-toe dust look. Clean in 2018, covered in 2022. Dust on the solar panels meant less power, and contact ended in 2022'},
  html=lambda: f'''<div class="split" style="top:0"><img src="file://{ASSETS}/PIA22876_c.jpg" style="object-position:50% 50%"></div>
     <div class="split" style="top:50%"><img src="file://{ASSETS}/PIA25287_c.jpg" style="object-position:50% 50%"></div>'''
   + shade('top') + f'<div class="yr" style="top:760px">2018</div><div class="yr" style="top:1010px">2022</div>' + col(
    look(3), h('全身<em>砂まみれ</em>コーデ', 'The <em>all-over dust</em> look'),
    bx('太陽電池に砂がつもると、電気が作れない', 'Dust on the solar panels means less power', 'sm green'))
   + cr('本物の写真：インサイトの自撮り。上が2018年、下が2022年（NASA/JPL-Caltech）', 'Real photos: InSight selfies. Top: 2018. Bottom: 2022 (NASA/JPL-Caltech)')),
 dict(dur=6.5, alt={'ja': 'LOOK4：アポロ11号の着陸船。はしごに金属のプレート。「私たちは全人類のために平和のうちに来た」と書いてある。今も月にある', 'en': 'Look 4: the Apollo 11 lander wears a metal plaque on its ladder. It says “We came in peace for all mankind.” It is still on the Moon'},
  html=lambda: bg('as11-40-5899', '50% 50%', 1.0, 'brightness(.85)') + shade('top') + col(
    look(4), h('足もとに<em>メッセージ</em>', 'A <em>message</em> on its leg'),
    bx('はしごに付けた、金属のプレート', 'A metal plaque on the ladder', 'sm'),
    bx('「私たちは全人類のために、平和のうちに来た」と書いてある。今も月にある', 'It says “We came in peace for all mankind.” It is still on the Moon', 'sm green'))
   + cr('本物の写真：アポロ11号の着陸船のはしご（1969年、NASA）', 'Real photo: the ladder of the Apollo 11 lander (1969, NASA)')),
 dict(dur=5, alt={'ja': 'どのLOOKが好き？コメントで教えて', 'en': 'Which look is your favorite? Tell us in the comments'},
  html=lambda: f'''<div class="grid4"><img src="file://{ASSETS}/as17-137-20979.jpg" style="object-position:62% 50%"><img src="file://{ASSETS}/PIA23882.jpg"><img src="file://{ASSETS}/PIA25287_c.jpg"><img src="file://{ASSETS}/as11-40-5899.jpg"></div>'''
   + shade('all') + col(
    h('どのLOOKが好き？', 'Which look is<br>your favorite?', 'lg'),
    bx('1〜4の番号でコメントしてね', 'Comment with a number, 1 to 4', 'sm yellow'), cls='mid')),
]
POST = dict(id='runway-looks-1', account='space_runway', place='moon', audio='media/music/funkorama.mp3',
 caption={'ja': '月と火星に置いてきた機械のファッションチェック。見た目には全部理由がある #ファッションチェック #月 #火星', 'en': 'Fashion check for machines left on the Moon and Mars. Every look has a reason #fashioncheck #moon #mars'},
 tags=['fashioncheck', 'moon', 'mars'],
 sound={'ja': 'Kevin MacLeod「Funkorama」(CC BY 4.0)', 'en': 'Kevin MacLeod – Funkorama (CC BY 4.0)'},
 comments=pinned('space_runway',
"""4つのLOOKの、ほんとの理由👇

LOOK 1　月面車の泥よけ（アポロ17号、1972年）
作業中にハンマーが引っかかって、右うしろの泥よけの一部が取れました。走ると月の砂をあびてしまうので、宇宙飛行士は月の地図をテープでつなぎ、クリップでとめて、代わりの泥よけを作りました。月面車は今も月にあります。

LOOK 2　インジェニュイティの布（火星、2021〜2024年）
1.3cm四方の布は、ライト兄弟が1903年に世界で初めて飛ばした飛行機のつばさに使われていたものです。太陽電池の下のケーブルに付けてあります。インジェニュイティは火星で72回飛びました。

LOOK 3　インサイトの砂（火星、2018〜2022年）
インサイトは太陽の光で電気を作っていました。太陽電池に砂がつもって作れる電気が減り、2022年12月に通信が終わりました。上の写真が着陸してすぐ、下が最後の自撮りです。

LOOK 4　アポロ11号のプレート（月、1969年）
人が初めて月に降りたときの着陸船の、はしごに付いています。「西暦1969年7月、惑星地球から来た人間が、ここに初めて月に足をしるした。私たちは全人類のために、平和のうちに来た」と書かれています。

※「ファッションチェック」は演出です。写真はすべて本物です。""",
"""The real reason behind each look 👇

LOOK 1: the Moon car's fender (Apollo 17, 1972)
A hammer caught the right rear fender and part of it broke off. Driving then sprayed Moon dust over everything, so the astronauts taped lunar maps together and clamped them on as a new fender. The rover is still on the Moon.

LOOK 2: Ingenuity's cloth (Mars, 2021–2024)
The 1.3 cm square is wing fabric from the Wright brothers' Flyer, which made the first powered, controlled flight on Earth in 1903. It is attached to a cable under the solar panel. Ingenuity flew 72 times on Mars.

LOOK 3: InSight's dust (Mars, 2018–2022)
InSight ran on solar power. Dust built up on its panels, power dropped, and contact ended in December 2022. Top: just after landing. Bottom: its final selfie.

LOOK 4: Apollo 11's plaque (Moon, 1969)
It is on the ladder of the first lander to carry people to the Moon. It reads: "Here men from the planet Earth first set foot upon the Moon, July 1969, A.D. We came in peace for all mankind."

Note: the "fashion check" is our dramatization. All photos are real."""),
 sources=[nasa_img('as17-137-20979', 'Close-up of lunar roving vehicle: makeshift fender repair with lunar maps and clamps'),
  nasa_img('7040032', 'Apollo 17: maps taped together and clamped to patch the LRV fender', 'NASA/MSFC'),
  pj('PIA24438', 'Pride of the West — and Mars (Wright brothers fabric on Ingenuity)', 'NASA/JPL-Caltech'), pj('PIA23882', "NASA's Ingenuity Mars Helicopter", 'NASA/JPL-Caltech'),
  fact('Ingenuity Mars Helicopter (NASA Science): 72 flights, 2021–2024', 'https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/'),
  pj('PIA22876', "InSight's First Selfie", 'NASA/JPL-Caltech'), pj('PIA25287', "InSight's Final Selfie (dusty solar panels producing less power)", 'NASA/JPL-Caltech'),
  fact('InSight Lander (NASA Science): mission end, December 2022', 'https://science.nasa.gov/mission/insight/'),
  nasa_img('as11-40-5899', 'View of plaque Apollo 11 astronauts left on the Moon'), nasa_img('S69-39334', 'Replica of the Apollo 11 plaque (wording)'),
  nasa_img('KSC-as11-40-5927', 'Apollo 11 Lunar Module on the Moon'), music('Funkorama')])
