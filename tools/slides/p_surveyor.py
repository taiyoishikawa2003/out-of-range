"""Surveyor 3 x POV story: 'Alone on the Moon for 2.5 years. Then people came.'"""
from lib import *
DIR = 'surveyor'
SLIDES = [
 dict(dur=4.5, alt={'ja': 'POV：月で2年半、ひとりで待ってた。月面のサーベイヤー3号の写真', 'en': 'POV: alone on the Moon for 2.5 years. Photo of Surveyor 3 on the Moon'},
  html=lambda: bg('as12-48-7121', '42% 50%') + shade('top') + col(
    tag('POV', 'POV', 'pink'),
    h('月で<em>2年半</em>、<br>ひとりで待ってた', 'Alone on the Moon<br>for <em>2.5 years</em>'),
    bx('通信もとぎれて、ずっと動けない', 'No signal. Can’t move.', 'sm'))
   + cr('本物の写真：月面のサーベイヤー3号（NASA）', 'Real photo: Surveyor 3 on the Moon (NASA)')),
 dict(dur=4, alt={'ja': '人が来た！アポロ12号が約180m先に着陸', 'en': 'People showed up! Apollo 12 landed about 180 m away'},
  html=lambda: bg('AS12-48-7133', '55% 50%') + shade('top') + col(
    h('…<em>人が来た！！</em>', '…<em>PEOPLE!!</em>', 'lg'),
    bx('アポロ12号。たった180m先に着陸', 'Apollo 12 landed just 180 m away', 'sm'))
   + cr('本物の写真：1969年11月。奥に見えるのがアポロ12号の着陸船（NASA）', 'Real photo: Nov 1969. Apollo 12’s lander is in the background (NASA)')),
 dict(dur=3.5, alt={'ja': 'え、わざわざ会いに来てくれたの？宇宙飛行士がサーベイヤー3号をのぞきこんでいる', 'en': 'Wait, you came all this way to see me? An astronaut looks closely at Surveyor 3'},
  html=lambda: bg('AS12-48-7134', '62% 50%', 1.25, origin='60% 55%') + shade('top') + col(
    h('え、わざわざ<br>会いに来てくれたの？', 'Wait… you came<br>all this way for me?', 'md'),
    bx('うれしい…', 'I’m so happy…', 'sm'))
   + cr('本物の写真：サーベイヤー3号を調べる宇宙飛行士（NASA）', 'Real photo: an astronaut examines Surveyor 3 (NASA)')),
 dict(dur=4, alt={'ja': '現実：カメラ、もぎ取られた。スコップも持っていかれた', 'en': 'Reality: they took my camera. And my scoop.'},
  html=lambda: bg('as12-48-7136', '45% 50%', 1.15, origin='45% 60%') + shade('top') + col(
    tag('現実', 'Reality'),
    h('カメラ、<b>もぎ取られた</b>', 'They <b>took my camera</b>'),
    bx('スコップも持っていかれた', 'And my scoop', 'sm'))
   + cr('本物の写真：このあとテレビカメラなどを取り外した（NASA）', 'Real photo: they removed the TV camera and other parts (NASA)')),
 dict(dur=3.5, alt={'ja': 'そして帰っていった。また、ひとり', 'en': 'And then they left. Alone again'},
  html=lambda: bg('as12-48-7099', '50% 50%', filt='brightness(.8)') + shade('top') + col(
    h('そして帰っていった', 'And then they left'),
    bx('また、ひとり', 'Alone again', 'sm'))
   + cr('本物の写真：月面のサーベイヤー3号（NASA）', 'Real photo: Surveyor 3 on the Moon (NASA)')),
 dict(dur=6, alt={'ja': 'でも実は、カメラは地球で調べられた。月に2年半置いた機械はどうなるかを知るため', 'en': 'But actually, the camera was studied on Earth to learn what 2.5 years on the Moon does to a machine'},
  html=lambda: bg('as12-48-7110', '50% 60%', filt='brightness(.55)') + shade('all') + col(
    tag('でも実は', 'But actually', 'yellow'),
    h('カメラは<em>地球に<br>持ち帰って</em>調べた', 'The camera went<br><em>back to Earth</em>', 'md'),
    bx('月に2年半置いた機械は、どうなる？', 'What do 2.5 years on the Moon do to a machine?', 'sm'),
    bx('それを知る、めったにないチャンスだった', 'It was a rare chance to find out', 'sm green'))
   + cr('本物の写真：サーベイヤー3号の足と、土を掘ったあと（NASA）', 'Real photo: Surveyor 3’s footpad and the trenches it dug (NASA)')),
 dict(dur=6, alt={'ja': '2009年、月の上空から撮った写真。サーベイヤー3号は今も同じ場所にいる。宇宙飛行士の足あとも残っている', 'en': 'Photo from lunar orbit, 2009. Surveyor 3 is still in the same place. The astronauts’ footpaths are still there'},
  html=lambda: f'<img src="file://{ASSETS}/PIA12922.jpg" style="position:absolute;left:-1000px;top:-480px;width:2400px;height:2400px;filter:contrast(1.15) brightness(.9)">'
   + '<div class="mark" style="left:248px;top:732px"></div>' + f'<div class="mlabel" style="left:300px;top:806px">{t("アポロ12号の着陸船", "Apollo 12 lander")}</div>'
   + '<div class="mark" style="left:877px;top:1186px"></div>' + f'<div class="mlabel" style="left:700px;top:1100px;transform:none;left:auto;right:240px">{t("サーベイヤー3号", "Surveyor 3")}</div>'
   + shade('top') + col(
    tag('40年後、月の上空から', '40 years later, from orbit', 'white sm'),
    h('今も<em>同じ場所</em>にいる', 'It’s <em>still there</em>'),
    bx('宇宙飛行士の足あとも、まだ残ってる', 'So are the astronauts’ footpaths', 'sm'))
   + cr('本物の写真：2009年、月を回る探査機LROが撮ったアポロ12号の着陸地点（NASA/GSFC/Arizona State University）', 'Real photo: the Apollo 12 site seen by the LRO orbiter, 2009 (NASA/GSFC/Arizona State University)')),
]
for i, m in {0: 'media/music/gymnopedie_no_1.mp3', 1: 'media/music/carefree.mp3', 3: 'media/music/gymnopedie_no_1.mp3', 5: 'media/music/carefree.mp3'}.items(): SLIDES[i]['music'] = m
POST = dict(id='surveyor-pov-1', account='surveyor3', place='moon',
 caption={'ja': '月で2年半ひとりで待ってたら、人が来た（実話） #POV #月 #サーベイヤー3号', 'en': 'I waited alone on the Moon for 2.5 years. Then people came. (True story) #POV #moon #surveyor3'},
 tags=['POV', 'moon', 'surveyor3', 'apollo12'],
 sound={'ja': 'Kevin MacLeod「Gymnopedie No. 1」「Carefree」(CC BY 4.0)', 'en': 'Kevin MacLeod – Gymnopedie No. 1 / Carefree (CC BY 4.0)'},
 comments=pinned('surveyor3',
"""答え合わせ👇（ここからは全部ほんとの話）

サーベイヤー3号は、1967年4月に月に着陸した、人が乗っていない探査機です。

■ 着陸でバウンドした
降りるときにエンジンが止まらず、月面で2回はねました（1回目は高さ約10m、2回目は約3m）。3回目でやっと止まりました。

■ 月で何をした？
写真を6,326枚送り、スコップで月の土を掘って、かたさを調べました。「月の地面は、人が乗る着陸船を支えられるくらいしっかりしている」と分かりました。最後の通信は1967年5月4日です。

■ 2年半後に人が来た
1969年11月、アポロ12号が約180m先に着陸しました。2人の宇宙飛行士が歩いてやって来て、テレビカメラやスコップなどを取り外し、地球に持ち帰りました。

■ なぜ持ち帰った？
月の表面に約2年半さらされた機械がどうなるかを、科学者が調べるためです。

■ 今は？
今も月の「嵐の大洋」にあります。2009年に月を回る探査機LROが撮った写真には、アポロ12号の着陸船の下の部分とサーベイヤー3号、宇宙飛行士が歩いたあとが写っています。

※「え、会いに来てくれたの？」などのセリフは、わたしたちが考えた演出です。写真はすべて本物です。最後の写真の丸と名前は、わたしたちが書き足しました。""",
"""The real story 👇 (everything below is true)

Surveyor 3 was a robotic lander that reached the Moon in April 1967.

■ It bounced
Its engine did not shut off in time, so it bounced off the Moon twice (about 10 m high, then about 3 m) before settling on the third touchdown.

■ What did it do?
It sent 6,326 pictures and dug into the soil with a scoop to test how firm it was. That showed the ground was solid enough to hold a lander carrying people. Last contact was on May 4, 1967.

■ 2.5 years later, people came
In November 1969, Apollo 12 landed about 180 m away. Two astronauts walked over, removed the TV camera, the scoop and other parts, and took them back to Earth.

■ Why take them?
So scientists could study what nearly two and a half years on the Moon's surface does to a machine.

■ And now?
It is still in the Ocean of Storms. A 2009 photo from the LRO orbiter shows the Apollo 12 descent stage, Surveyor 3 and the astronauts' footpaths.

Note: lines like "you came all this way for me?" are our own dramatization. All photos are real. We added the circles and labels on the last photo."""),
 sources=[fact('Surveyor 3 (NASA Science): landing, 6,326 pictures, last contact, Apollo 12 visit', 'https://science.nasa.gov/mission/surveyor-3/'),
  nasa_img('as12-48-7121', 'View of Surveyor III in its crater'), nasa_img('AS12-48-7133', 'View of two U.S. spacecraft on the surface of the Moon'),
  nasa_img('AS12-48-7134', 'Conrad examines the Surveyor 3 TV camera'), nasa_img('as12-48-7136', 'Astronaut examines Surveyor 3'),
  nasa_img('as12-48-7099', 'View of the Surveyor III craft'), nasa_img('as12-48-7110', 'Surveyor 3 footpad and surface sampler trenches'),
  pj('PIA12922', 'Apollo 12 Second Look: Midday on the Ocean of Storms (footpaths visible)', 'NASA/GSFC/Arizona State University'),
  music('Gymnopedie No. 1'), music('Carefree')])
