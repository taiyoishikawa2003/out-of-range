"""Pioneer 10 x navigation app: 'Arrive in about 2 million years.'"""
from lib import *
DIR = 'pioneer'
ART = lambda f='brightness(.75)': bg('ARC-1973-AC73-4247_c', '62% 50%', 1.0, f)
SLIDES = [
 dict(dur=6, alt={'ja': 'パイオニア10号のカーナビを見てみた。目的地：アルデバラン。到着予定：約200万年後。距離68光年', 'en': 'I checked Pioneer 10’s nav app. Destination: Aldebaran. Arrival: in about 2 million years. Distance: 68 light-years'},
  html=lambda: ART() + shade('top') + col(
    h('パイオニア10号の<br>カーナビを見てみた', 'I checked Pioneer 10’s<br>nav app', 'md'),
    f'<div class="navtop"><span style="font-size:54px">📍</span><div><small>{t("目的地", "Destination")}</small>{t("アルデバラン（おうし座の赤い星）", "Aldebaran (red star in Taurus)")}</div></div>',
    f'''<div class="sheet"><div class="lbl">{t("到着予定", "Arrival")}</div><div class="eta">{t("約200万年後", "in ~2 million years")}</div>
      <div class="sub">{t("距離 68光年", "Distance: 68 light-years")}</div><div class="go">{t("案内を開始", "Start")}</div></div>''', style='top:310px')
   + cr('想像図：木星の近くを通るパイオニア10号（NASA Ames／Rick Guidice）', 'Artist’s concept: Pioneer 10 passing Jupiter (NASA Ames / Rick Guidice)')),
 dict(dur=7.5, alt={'ja': 'ほかの行き方。歩く：約180億年。車：約7億年。新幹線：約2.4億年。パイオニア10号：約200万年でいちばん速い。歩くと宇宙の年齢138億年より長い', 'en': 'Other ways to go. Walking: about 18 billion years. Car: about 730 million years. Bullet train: about 240 million years. Pioneer 10: about 2 million years, the fastest. Walking takes longer than the age of the universe, 13.8 billion years'},
  html=lambda: ART('brightness(.5)') + col(
    h('ほかの行き方も調べた', 'I checked other routes', 'md'),
    f'''<div class="modes">
      <div class="mode"><span class="ic">🚶</span><div class="nm">{t("歩く", "Walk")}<small>{t("時速4km・休みなし", "4 km/h, no breaks")}</small></div><span class="tm">{t("約180億年", "~18 billion yr")}</span></div>
      <div class="mode"><span class="ic">🚗</span><div class="nm">{t("車", "Car")}<small>{t("時速100km", "100 km/h")}</small></div><span class="tm">{t("約7億年", "~730 million yr")}</span></div>
      <div class="mode"><span class="ic">🚄</span><div class="nm">{t("新幹線", "Bullet train")}<small>{t("時速300km", "300 km/h")}</small></div><span class="tm">{t("約2.4億年", "~240 million yr")}</span></div>
      <div class="mode best"><span class="ic">🛰️</span><div class="nm">{t("パイオニア10号", "Pioneer 10")}<span class="badge">{t("最速", "FASTEST")}</span></div><span class="tm">{t("約200万年", "~2 million yr")}</span></div></div>''',
    bx('歩くと、宇宙の年齢（138億年）より長い', 'Walking takes longer than the age of the universe (13.8 billion years)', 'sm yellow'), style='top:330px')),
 dict(dur=6, alt={'ja': '現在地：わからない。最後に信号がとどいたのは2003年1月。そのとき地球から約122億km、電波でも11時間20分かかった', 'en': 'Current location: unknown. Its last signal arrived in January 2003, from about 12.2 billion km away. Even radio took 11 hours 20 minutes'},
  html=lambda: bg('ARC-1973-AC73-9019_c', '50% 40%', 1.0, 'brightness(.8)') + shade('top') + col(
    f'<div class="navtop"><span style="font-size:54px">📡</span><div><small>{t("現在地", "Current location")}</small><span style="color:#e5202a">{t("わからない（圏外）", "Unknown (out of range)")}</span></div></div>',
    bx('最後に信号がとどいたのは2003年1月', 'Its last signal arrived in January 2003', 'sm'),
    bx('そのとき地球から約122億km。電波でも11時間20分かかった', 'It was 12.2 billion km away. Even radio took 11 h 20 min', 'sm'))
   + cr('本物の写真：組み立て中のパイオニア10号（NASA Ames）', 'Real photo: Pioneer 10 being assembled (NASA Ames)')),
 dict(dur=6, alt={'ja': 'いちおう名刺は持ってる。だれかに拾われたとき用。地球の場所と人間の絵がかいてある金属の板', 'en': 'It does carry a business card, in case someone finds it: a metal plaque showing where Earth is and what humans look like'},
  html=lambda: ART('blur(12px) brightness(.4)') + col(
    h('いちおう<em>名刺</em>は持ってる', 'It does carry a<br><em>business card</em>', 'md'),
    f'<figure class="ph" style="width:840px;transform:rotate(-1.5deg)"><img src="file://{ASSETS}/ARC-1972-AC72-1338_c.jpg"><figcaption>{t("パイオニア10号にのせた金属の板（NASA Ames）", "The plaque carried by Pioneer 10 (NASA Ames)")}</figcaption></figure>',
    bx('だれかに拾われたとき用', 'In case someone finds it', 'sm'),
    bx('地球の場所と、人間の絵がかいてある', 'It shows where Earth is, and what we look like', 'sm'))),
 dict(dur=6, alt={'ja': 'この先200万年、道なりです。予定は21か月の旅だったが、30年以上信号を送りつづけた。今も飛びつづけている', 'en': 'Continue straight for 2 million years. Planned as a 21-month mission, it kept sending signals for over 30 years. It is still flying'},
  html=lambda: ART() + shade('top') + col(
    f'<div class="turn"><span class="ar">⬆</span><div>{t("この先 200万年、<br>道なりです", "Continue straight<br>for 2 million years")}</div></div>',
    bx('予定は21か月の旅 → 30年以上、信号を送りつづけた', 'Planned: a 21-month trip → it kept calling home for 30+ years', 'sm'),
    bx('今も、だまって飛びつづけてる', 'It is still flying, silently', 'sm green'))
   + cr('想像図：木星の近くを通るパイオニア10号（NASA Ames／Rick Guidice）', 'Artist’s concept: Pioneer 10 passing Jupiter (NASA Ames / Rick Guidice)')),
]
POST = dict(id='pioneer-navi-1', account='pioneer10', place='deep', audio='media/music/local_forecast_elevator.mp3',
 caption={'ja': 'パイオニア10号のカーナビ、到着予定がおかしい #カーナビ #宇宙 #パイオニア10号', 'en': 'Pioneer 10’s nav app has a very strange arrival time #navapp #deepspace #pioneer10'},
 tags=['navi', 'deepspace', 'pioneer10'],
 sound={'ja': 'Kevin MacLeod「Local Forecast - Elevator」(CC BY 4.0)', 'en': 'Kevin MacLeod – Local Forecast - Elevator (CC BY 4.0)'},
 comments=pinned('pioneer10',
"""ほんとの話と、計算のしかた👇

パイオニア10号は1972年に打ち上げられた、NASAで最初に木星より遠くをめざした探査機です。

■ 21か月の予定が30年以上
もともとは木星の近くを通る21か月の計画でした。実際は30年以上、地球に信号を送りつづけました。

■ 最後の信号
2003年1月。地球から約122億kmはなれていて、電波（光と同じ速さ）でも11時間20分かかりました。電気を作る装置の力が弱くなり、今は連絡がとれません。

■ どこへ向かっている？
おうし座の赤い星アルデバランの方向です。アルデバランまでは約68光年。NASAは「200万年以上かかる」としています。

■ 名刺って？
宇宙のだれかに見つけてもらったときのために、地球の場所と人間の絵をかいたアルミの板をのせています。

■ 計算のしかた（わたしたちの計算）
68光年＝約643兆km（1光年＝約9.46兆km）。これを休まずに進んだときの年数にしました。
・歩く（時速4km）：約183億年
・車（時速100km）：約7.3億年
・新幹線（時速300km）：約2.4億年
宇宙の年齢は約138億年です（NASA）。

※カーナビの画面は、わたしたちが作った演出です。パイオニア10号にカーナビはありません。""",
"""The real story, and how we did the math 👇

Pioneer 10 launched in 1972. It was NASA's first mission to the outer planets.

■ Planned for 21 months, lasted over 30 years
It was designed for a 21-month mission to fly by Jupiter. It kept sending signals to Earth for more than 30 years.

■ Last signal
January 2003, from about 12.2 billion km away. Even radio, at the speed of light, took 11 hours 20 minutes. Its power source had become too weak, so we can no longer hear it.

■ Where is it going?
Toward Aldebaran, the red star in Taurus, about 68 light-years away. NASA says it will take more than 2 million years.

■ The "business card"
An aluminum plaque showing where Earth is and what humans look like, in case anyone ever finds it.

■ Our calculation
68 light-years ≈ 643 trillion km (1 light-year ≈ 9.46 trillion km). Travelling nonstop:
・Walking (4 km/h): about 18.3 billion years
・Car (100 km/h): about 730 million years
・Bullet train (300 km/h): about 240 million years
The universe is about 13.8 billion years old (NASA).

Note: the nav app screens are our dramatization. Pioneer 10 has no nav app."""),
 sources=[fact('Pioneer 10 (NASA Science): 21-month design, last signal Jan. 23, 2003, 12.23 billion km, 11 h 20 min, plaque, Aldebaran', 'https://science.nasa.gov/mission/pioneer-10/'),
  fact('NASA: Pioneer 10 Sends Last Signal (Aldebaran is about 68 light-years away; over 2 million years)', 'https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/'),
  fact('NASA: the universe is about 13.8 billion years old', 'https://science.nasa.gov/universe/overview/'),
  src('calc', 'Travel times = 68 light-years (6.43 × 10^14 km) ÷ speed (4, 100, 300 km/h), nonstop, 8,766 hours per year', 'https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/'),
  src('art', 'ARC-1973-AC73-4247 Pioneer 10 passing Jupiter, artist: Rick Guidice (NASA Ames)', 'https://images.nasa.gov/details/ARC-1973-AC73-4247'),
  nasa_img('ARC-1973-AC73-9019', 'Pioneer 10 spacecraft final assembly', 'NASA Ames'), nasa_img('ARC-1972-AC72-1338', 'Pioneer F/G plaque', 'NASA Ames'),
  music('Local Forecast - Elevator')])
