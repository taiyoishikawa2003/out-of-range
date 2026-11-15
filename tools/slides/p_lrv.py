"""Lunar rovers x the 'gotta tell everyone' running meme: one real frame of the Apollo 16 'Grand Prix' drive, three facts."""
from lib import *
DIR = 'lrv'
N15 = 'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1971-063C'
CSS = '''
.s{background:#000}
.gp{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.seam{position:absolute;left:0;right:0;height:150px;background:linear-gradient(#000,rgba(0,0,0,0))}
.eh{font-size:74px;line-height:1.2;color:#ffd21f;-webkit-text-stroke:13px #000;paint-order:stroke fill;letter-spacing:.06em}
.low{position:absolute;left:40px;right:160px;text-align:center}
'''
def slide(msg_ja, msg_en, zoom=1.0, dy=430, pos='18% 50%', origin='30% 35%', low=1440):
    return (f'<img class="gp" src="file://{ASSETS}/S72-37002.jpg" style="object-position:{pos};transform:translateY({dy}px) scale({zoom});transform-origin:{origin}">'
            f'<div class="seam" style="top:{dy - 2}px"></div>'
            + col(f'<div class="eh">{t("エッホ エッホ", "Huff, huff…")}</div>', h(msg_ja, msg_en, 'md'), style='top:300px;gap:18px')
            + f'<div class="low" style="top:{low}px"><div class="eh">{t("エッホ エッホ", "Huff, huff…")}</div></div>'
            + f'<div class="cr" style="top:{low + 110}px">{t("本物の写真：月面車のスピードテスト。アポロ16号、1972年（NASA）", "Real photo: a speed test of the lunar rover. Apollo 16, 1972 (NASA)")}</div>')
SLIDES = [
 dict(dur=4.5, alt={'ja': 'エッホエッホ。月に車を3台置いてきたって伝えなきゃ。月面を走る月面車の本物の写真', 'en': 'Huff, huff. Gotta tell everyone we left three cars on the Moon. A real photo of the lunar rover speeding across the Moon'},
  html=lambda: slide('月に車を<em>3台</em><br>置いてきたって<br>伝えなきゃ', 'Gotta tell everyone<br>we left <em>3 cars</em><br>on the Moon')),
 dict(dur=4.5, alt={'ja': 'エッホエッホ。車のおかげで5km先まで調べに行けたって伝えなきゃ', 'en': 'Huff, huff. Gotta tell everyone the car let astronauts explore 5 kilometers away'},
  html=lambda: slide('車のおかげで<br><em>5km先</em>まで行けたって<br>伝えなきゃ', 'Gotta tell everyone<br>the car took them<br><em>5 km (3 miles)</em> out', 1.3, 500, '18% 50%', '28% 30%', 1480)),
 dict(dur=5.5, alt={'ja': 'エッホエッホ。3台とも、いまも月にあるって伝えなきゃ。くわしくはコメント欄', 'en': 'Huff, huff. Gotta tell everyone all three are still on the Moon. Details in the comments'},
  html=lambda: slide('3台とも<br><em>いまも月にある</em>って<br>伝えなきゃ', 'Gotta tell everyone<br>all three are<br><em>still up there</em>', 1.12, 455, '18% 50%', '30% 45%')),
]
POST = dict(id='lrv-ehho-1', account='moon_lostfound', place='moon', audio='media/music/hyperfun.mp3',
 caption={'ja': 'エッホエッホ　月に車を3台置いてきたって伝えなきゃ（本物の写真） #エッホエッホ #月 #月面車',
          'en': 'Huff, huff… gotta tell everyone we left 3 cars on the Moon. (Real photo) #gottatelleveryone #moon #lunarrover'},
 tags=['moon', 'apollo', 'lrv'],
 sound={'ja': 'Kevin MacLeod「Hyperfun」(CC BY 4.0)', 'en': 'Kevin MacLeod – Hyperfun (CC BY 4.0)'},
 comments=pinned('moon_lostfound',
"""エッホエッホの中身（ぜんぶ本当）👇

■ 月に車を3台
アポロ15号（1971年）、16号と17号（1972年）は、月面車を1台ずつ持っていきました。3台とも、月に置いたままです。

■ 車があると何がいい？
アポロ15号では、着陸船から5kmはなれた場所まで調べに行けました。歩くだけのときより、ずっと広いはんいの石や土を集められます。

■ どれくらい動いた？
月の上で動いた道のりは、15号で27.9km、16号で27km、17号で30kmです（NASAの資料）。

■ この写真
1972年4月21日、アポロ16号の飛行士が月面車のスピードテストをしているところ。「グランプリ」とよばれた走りを、もうひとりの飛行士が16ミリフィルムで撮りました。その1コマです。

※「エッホエッホ」は演出です。写真はNASAの本物で、3枚とも同じ1枚を拡大・縮小しています。""",
"""What the huffing is about (all true) 👇

■ Three cars on the Moon
Apollo 15 (1971), Apollo 16 and Apollo 17 (1972) each took one lunar rover. All three were left on the Moon.

■ Why bring a car?
On Apollo 15, the rover let the astronauts explore up to 5 km (3 miles) from the lander. That is a much wider area for collecting rocks and soil than they could reach on foot.

■ How far did they go?
The crews covered 27.9 km on Apollo 15, 27 km on Apollo 16 and 30 km on Apollo 17 (NASA).

■ This photo
April 21, 1972: an Apollo 16 astronaut gives the rover a speed test, a run nicknamed the “Grand Prix.” The other astronaut filmed it on 16 mm film. This is one frame.

Note: the “huff, huff… gotta tell everyone” format is ours. The photo is a real NASA image; all three slides show the same picture, zoomed in or out.""") + [
  {'user': 'opportunity_rover', 'text': {'ja': '人が運転する車、ちょっとうらやましい。こっちは命令が届くまで待ってから動きます', 'en': 'A car with a driver. A little jealous. I have to wait for my commands to arrive before I move.'}},
  {'user': 'sojourner_rover', 'text': {'ja': '5km…！わたしは着陸機から12mより遠くへ行ったことがない', 'en': '5 km…! I never went more than 12 meters from my lander.'}}],
 sources=[fact('NSSDCA: Apollo 15 Lunar Module / ALSEP (crew covered 27.9 km; rover used to explore within 5 km of the lander; first use of such a vehicle)', N15),
  fact('NSSDCA: Apollo 16 Lunar Module / ALSEP (crew covered 27 km)', 'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1972-031C'),
  fact('NSSDCA: Apollo 17 Lunar Module / ALSEP (crew covered 30 km)', 'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1972-096C'),
  nasa_img('S72-37002', 'Lunar Roving Vehicle "Grand Prix" (Apollo 16, April 21, 1972; frame from 16 mm film)', 'NASA'),
  fact("For @sojourner_rover's comment: NASA History: Sojourner never ventured more than 39 feet (12 m) from the lander", 'https://www.nasa.gov/history/25-years-ago-mars-pathfinder-launches-to-mars-to-deploy-sojourner-the-first-planetary-rover/'),
  fact("For @opportunity_rover's comment: Mars in a Minute: How Do Rovers Drive on Mars? (NASA Science): no joystick; commands are sent ahead of time", 'https://science.nasa.gov/resource/mars-in-a-minute-how-do-rovers-drive-on-mars/'),
  music('Hyperfun')])
