"""Pioneer 11 x photo dump: 'I went to Jupiter and Saturn. Here are my photos. Return ticket: none.'"""
from lib import *
DIR = 'pioneer11'
P11 = 'https://science.nasa.gov/mission/pioneer-11/'
HIST = 'https://www.nasa.gov/history/40-years-ago-pioneer-11-first-to-explore-saturn/'
CSS = '''
.sky{position:absolute;inset:0;background:
 radial-gradient(2px 2px at 12% 18%,#fff 50%,transparent 51%),radial-gradient(2px 2px at 82% 12%,#fff 50%,transparent 51%),
 radial-gradient(3px 3px at 68% 30%,#cfe0ff 50%,transparent 51%),radial-gradient(2px 2px at 30% 72%,#fff 50%,transparent 51%),
 radial-gradient(2px 2px at 90% 64%,#fff 50%,transparent 51%),radial-gradient(3px 3px at 8% 88%,#ffe9c4 50%,transparent 51%),
 radial-gradient(2px 2px at 52% 92%,#fff 50%,transparent 51%),radial-gradient(2px 2px at 44% 8%,#fff 50%,transparent 51%),
 linear-gradient(160deg,#0b0e1a,#161226 60%,#0d1220)}
.pol{background:#fdfdfb;padding:22px 22px 20px;border-radius:6px;box-shadow:0 20px 54px rgba(0,0,0,.75);position:relative}
.pol img{display:block;width:100%;object-fit:cover;background:#000}
.pol .dt{position:absolute;right:42px;font-family:'DejaVu Sans Mono',monospace;font-weight:700;font-size:38px;color:#ff9a2e;text-shadow:0 0 10px rgba(255,120,0,.9);letter-spacing:.04em}
.pol figcaption{font-size:27px;font-weight:700;color:#444;margin-top:14px;line-height:1.3;text-align:left}
'''
def pol(nid, cap_ja, cap_en, w=820, hgt=600, rot=-2, date='', pos='50% 50%'):
    dt = f'<span class="dt" style="top:{hgt - 36}px">{date}</span>' if date else ''
    return (f'<figure class="pol" style="width:{w}px;transform:rotate({rot}deg)"><img style="height:{hgt}px;object-position:{pos}" '
            f'src="file://{ASSETS}/{nid}.jpg">{dt}<figcaption>{t(cap_ja, cap_en)}</figcaption></figure>')
SKY = '<div class="sky"></div>'
SLIDES = [
 dict(dur=4.5, alt={'ja': '写真ダンプ：木星と土星に行ってきた。ひとり旅の写真まとめ、1973年から1979年', 'en': 'Photo dump: I went to Jupiter and Saturn. Photos from my solo trip, 1973 to 1979'},
  html=lambda: SKY + col(
    tag('写真ダンプ', 'Photo dump', 'pink sm'),
    h('木星と土星に<br>行ってきた', 'I went to Jupiter<br>and Saturn'),
    pol('P11_saturn_rings', '本物の写真：パイオニア11号が撮った土星（NASA/Ames）', 'Real photo: Saturn, taken by Pioneer 11 (NASA/Ames)', 800, 571, -3, '1979'),
    bx('ひとり旅の写真まとめ（1973〜1979）', 'Photos from my solo trip (1973–1979)', 'sm yellow'), style='top:300px;gap:30px')),
 dict(dur=4.5, alt={'ja': '1枚目：出発。予定は木星まで。1973年4月の打ち上げの写真', 'en': 'Photo 1: leaving home. The plan: go as far as Jupiter. Launch photo from April 1973'},
  html=lambda: SKY + col(
    tag('1枚目', 'Photo 1', 'white sm'),
    pol('P11_pioneer_11_launch_apr_5_1973', '本物の写真：パイオニア11号の打ち上げ（NASA）', 'Real photo: the launch of Pioneer 11 (NASA)', 820, 620, 2, '1973', '40% 50%'),
    h('出発', 'Leaving home', 'lg'),
    bx('予定は「木星まで」', 'The plan: “as far as Jupiter”', 'sm'), style='top:310px;gap:30px')),
 dict(dur=5, alt={'ja': '2枚目：木星。上から見るとこう。木星の北極がわの写真は世界初', 'en': 'Photo 2: Jupiter, seen from above. These were the first pictures of Jupiter’s polar regions'},
  html=lambda: SKY + col(
    tag('2枚目', 'Photo 2', 'white sm'),
    pol('P11_jupiter_pole', '本物の写真：北極の上から見た木星（NASA）', 'Real photo: Jupiter from above its north pole (NASA)', 820, 660, -2, '1974'),
    h('木星。<br>上から見るとこう', 'Jupiter.<br>From above.', 'md'),
    bx('北極がわの写真は、世界初', 'The first pictures of its polar regions', 'sm yellow'), style='top:310px;gap:28px')),
 dict(dur=5.5, alt={'ja': '3枚目：予定変更。木星の重力でぐいっと曲がって、こんどは土星へ。NASAが作った道すじの図', 'en': 'Photo 3: change of plans. Jupiter’s gravity swings it around and sends it on to Saturn. A NASA map of its path'},
  html=lambda: SKY + col(
    tag('3枚目（地図のスクショ）', 'Photo 3 (screenshot of the map)', 'white sm'),
    pol('P11_pioneer_11_trajectory', 'NASAが作った図：パイオニア11号の道すじ（NASA）', 'NASA diagram: the path of Pioneer 11 (NASA)', 860, 452, 1.5),
    h('予定変更。<br>木星の重力でぐいっと', 'Change of plans.<br>Jupiter’s gravity swings me around', 'md'),
    h('こんどは<em>土星</em>へ', 'Next stop: <em>Saturn</em>', 'lg'), style='top:310px;gap:28px')),
 dict(dur=5, alt={'ja': '4枚目：土星に着いた。下の点は月のタイタン。土星に行ったのは、パイオニア11号がはじめて', 'en': 'Photo 4: made it to Saturn. The dot below is its moon Titan. Pioneer 11 was the first spacecraft to visit Saturn'},
  html=lambda: SKY + col(
    tag('4枚目', 'Photo 4', 'white sm'),
    pol('P11_saturn_rings', '本物の写真：土星と、月のタイタン（NASA/Ames）', 'Real photo: Saturn and its moon Titan (NASA/Ames)', 840, 600, -2, '1979'),
    h('着いた。<br>下の点は月（タイタン）', 'Made it.<br>The dot is a moon (Titan)', 'md'),
    bx('土星に行ったのは、ぼくがはじめて', 'I was the first to visit Saturn', 'sm green'), style='top:310px;gap:28px')),
 dict(dur=5, alt={'ja': '5枚目：タイタンのアップ。もやもや。オレンジ色のもやにつつまれた月', 'en': 'Photo 5: a close-up of Titan. Fuzzy. A moon wrapped in orange haze'},
  html=lambda: SKY + col(
    tag('5枚目', 'Photo 5', 'white sm'),
    pol('P11_pioneer_11_saturn_titan', '本物の写真：パイオニア11号が撮ったタイタン（NASA）', 'Real photo: Titan, taken by Pioneer 11 (NASA)', 700, 600, 2.5, '1979'),
    h('タイタンのアップ。<br>…<em>もやもや</em>', 'Titan, up close.<br>…<em>fuzzy</em>', 'md'),
    bx('オレンジ色のもやにつつまれた月', 'A moon wrapped in orange haze', 'sm'), style='top:310px;gap:28px')),
 dict(dur=7, alt={'ja': '最後の1枚：通りすぎてから、ふり返って撮った土星。帰りの便はなし。このまま太陽系の外へ', 'en': 'Last photo: Saturn, looking back after flying past. Return ticket: none. It is heading out of the solar system'},
  html=lambda: SKY + col(
    tag('最後の1枚', 'Last photo', 'white sm'),
    pol('P11_pioneer_11_saturn_post_encounter', '本物の写真：通りすぎたあとに撮った土星（NASA）', 'Real photo: Saturn, taken after the flyby (NASA)', 620, 400, -2),
    h('帰りの便：<em>なし</em>', 'Return ticket: <em>none</em>', 'lg'),
    bx('このまま、太陽系の外へ', 'Heading out of the solar system', 'sm'),
    bx('旅のうら話はコメント欄 👇', 'The story behind the trip: comments 👇', 'sm yellow'), style='top:310px;gap:28px')),
]
POST = dict(id='pioneer11-dump-1', account='pioneer11', place='deep', audio='media/music/wallpaper.mp3',
 caption={'ja': '木星と土星に行ってきた。ひとり旅の写真まとめ。帰りの便はなし（本物の写真） #写真ダンプ #ひとり旅 #パイオニア11号',
          'en': 'I went to Jupiter and Saturn. Photo dump from my solo trip. Return ticket: none. (Real photos) #photodump #solotrip #pioneer11'},
 tags=['pioneer11', 'deep', 'photodump'],
 sound={'ja': 'Kevin MacLeod「Wallpaper」(CC BY 4.0)', 'en': 'Kevin MacLeod – Wallpaper (CC BY 4.0)'},
 comments=pinned('pioneer11',
"""旅のうら話（ぜんぶ本当）👇

■ 予定は木星まで
パイオニア11号の予定は21か月。木星を調べるところまででした。先に木星へ行ったパイオニア10号がうまくいったので、「木星の重力を使って土星まで行こう」と予定が変わりました。

■ 木星（1974年12月）
木星の雲の上、約42,500kmまで近づきました。そのときの速さは時速171,000km以上。当時、人間が作ったものの中でいちばんの速さでした。木星の北極・南極のあたりの写真を、はじめて地球に送りました。

■ 土星（1979年9月1日）
土星に行った、はじめての探査機です。輪のすぐ外側を通りぬけて、土星から約21,000kmまで近づきました。写真を440枚撮り、新しい輪（F環）と新しい月を見つけました。

■ じつは下見
土星のそばで通った道は、あとから来るボイジャー2号が通る予定の道でした。パイオニア11号が先に通って、通れることをたしかめたのです。

■ 帰りの便なし
最後の通信は1995年。打ち上げから22年以上はたらきました。いまも太陽系の外へ向かって飛びつづけていて、約400万年後に、わし座の星の近くを通ると考えられています。宇宙のだれかにあてた、金属の手紙ものせています。

※写真はぜんぶNASAの本物です（打ち上げと、パイオニア11号が撮った木星・土星・タイタン）。3枚目はNASAが作った図。写真のふちと日付、「写真ダンプ」「ひとり旅」は演出です。""",
"""The story behind the trip (all true) 👇

■ The plan was only Jupiter
Pioneer 11 was planned for 21 months, just long enough to reach Jupiter. After Pioneer 10 got there first and all went well, the plan changed: use Jupiter’s gravity to go on to Saturn.

■ Jupiter (December 1974)
It flew about 26,400 miles (42,500 km) above Jupiter’s cloud tops at more than 106,000 mph (171,000 km/h). At the time, that was faster than anything humans had ever made. It sent back the first pictures of Jupiter’s polar regions.

■ Saturn (Sept. 1, 1979)
It was the first spacecraft to visit Saturn. It passed just outside the rings and came within about 13,000 miles (21,000 km) of the planet. It took 440 pictures and discovered a new ring (the F ring) and a new moon.

■ It was also a scout
The path it took past Saturn was the path Voyager 2 would need later. Pioneer 11 went first and showed that the way was clear.

■ No return ticket
The last contact was in 1995, more than 22 years after launch. It is still flying out of the solar system, and in about four million years it is expected to pass near a star in the constellation Aquila. It carries a metal plaque: a letter to anyone out there.

Note: every photo is a real NASA photo (the launch, and Jupiter, Saturn and Titan taken by Pioneer 11). Photo 3 is a NASA diagram. The photo frames, the date stamps, and the “photo dump” and “solo trip” framing are ours.""") + [
  {'user': 'pioneer10', 'text': {'ja': '兄です。木星までは先に行ったけど、土星は弟にゆずりました', 'en': 'Big brother here. I got to Jupiter first, but I left Saturn to my little brother.'}},
  {'user': 'dawn_spacecraft', 'text': {'ja': '時速171,000km…！こっちは4日かけて時速96kmです', 'en': '106,000 mph…! It takes me four days to reach 60.'}}],
 sources=[fact('Pioneer 11 (NASA Science): first spacecraft to fly by Saturn; Jupiter flyby Dec. 3, 1974 at 26,400 miles, more than 106,000 mph; Saturn flyby Sept. 1, 1979 at about 13,000 miles; 440 images; F ring and a new satellite; last contact 1995; near Lambda Aquilae in almost four million years; plaque', P11),
  fact('NASA History: 40 Years Ago: Pioneer 11 First to Explore Saturn (planned for 21 months; retargeted to Saturn in May 1974; pathfinder for Voyager 2; operated more than 22 years)', HIST),
  src('img', 'Saturn and its moon Titan, image by Pioneer 11 (NASA/Ames)', P11), src('img', 'Jupiter as seen from above its north pole by Pioneer 11 in 1974 (NASA)', P11),
  src('img', 'Launch of Pioneer 11; trajectory of Pioneer 11 (diagram); Titan taken by Pioneer 11; Saturn taken by Pioneer 11 after its flyby (NASA)', HIST),
  fact("For @pioneer10's comment: Pioneer 10 (NASA Science): first spacecraft to fly past Jupiter (December 1973)", 'https://science.nasa.gov/mission/pioneer-10/'),
  fact("For @dawn_spacecraft's comment: Dawn quick facts (NASA Science): 0 to 60 mph in 4 days", 'https://science.nasa.gov/mission/dawn/toolkit/quick-facts/'),
  music('Wallpaper')])
