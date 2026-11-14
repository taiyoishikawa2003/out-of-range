"""NEAR Shoemaker x group chat: the orbiter that was asked to land."""
from lib import *
DIR = 'near'
def chat(*msgs, title=None):
    bar = f'<div class="chbar"><div class="av">🌍</div><div>{t("NEARチーム", "Team NEAR")}<small>{t("地球のみんな、NEAR", "Everyone on Earth, NEAR")}</small></div></div>'
    return '<div class="chatbg"></div>' + bar + '<div class="msgs">' + ''.join(msgs) + '</div>'
def L(ja, en, cls=''): return f'<div class="m l {cls}">{t(ja, en)}</div>'
def R(ja, en, cls=''): return f'<div class="m r {cls}">{t(ja, en)}</div>'
def who(ja, en, side='l'): return f'<div class="who {side if side == "r" else ""}">{t(ja, en)}</div>'
SLIDES = [
 dict(dur=7, alt={'ja': 'チャット。地球：1年間おつかれさま！小惑星エロスを回る仕事は全部おわり。最後にひとつだけ。着陸してみない？ NEAR：は？', 'en': 'Chat. Earth: Great work this year! Your job orbiting asteroid Eros is done. One last thing. Want to try landing? NEAR: What?'},
  html=lambda: chat(
    who('地球', 'Earth'), L('1年間おつかれさま！小惑星エロスを回る仕事、ぜんぶ終わり！', 'Great work this year! Your job orbiting asteroid Eros is all done!'),
    L('で、最後にひとつだけ', 'So, one last thing'),
    L('<b>着陸してみない？</b>', '<b>Want to try landing?</b>', 'big'),
    who('NEAR', 'NEAR', 'r'), R('は？', 'What?', 'big'))
   + col(h('回るために作られた探査機、<br><em>着陸</em>をたのまれる', 'Built to orbit.<br>Asked to <em>land</em>.', 'md'), style='top:1080px')),
 dict(dur=7, alt={'ja': 'NEAR：足ないんですけど。回る用に作られたんですけど。地球：ゆっくり降りれば、いけると思う。降りながら写真もよろしく。NEAR：…やります', 'en': 'NEAR: I have no legs. I was built to orbit. Earth: If you go down slowly, we think it will work. Take photos on the way. NEAR: …OK'},
  html=lambda: chat(
    who('NEAR', 'NEAR', 'r'), R('足、ないんですけど', 'I don’t have legs'),
    R('回る用に作られたんですけど', 'I was built to orbit, not to land'),
    who('地球', 'Earth'), L('ゆっくり降りれば、いけると思う', 'If you go down slowly, we think it’ll work'),
    L('降りながら写真もよろしく📷', 'Take photos on the way down 📷'),
    who('NEAR', 'NEAR', 'r'), R('……やります', '…OK, I’ll do it', 'big'))),
 dict(dur=7.5, alt={'ja': 'NEARが写真を送信。最後の1枚、高さ120mから。下がザーッとなっているのは、送っている途中で着地したから', 'en': 'NEAR sends a photo: the last one, from 120 m up. The streaks at the bottom are there because it touched down while still sending'},
  html=lambda: chat(
    who('NEAR', 'NEAR', 'r'),
    f'<div class="m r img"><img src="file://{ASSETS}/PIA03148.jpg"><div class="imgcap">{t("本物の写真（NASA/JPL/JHUAPL）", "Real photo (NASA/JPL/JHUAPL)")}</div></div>',
    R('最後の1枚。高さ120mから', 'Last photo. From 120 m up'),
    R('下がザーッてなってるのは<br><b>送ってる途中で着地したから</b>', 'The streaks at the bottom?<br><b>I landed while sending it</b>'),
    who('地球', 'Earth'), L('え', 'Wait', 'big'))),
 dict(dur=6.5, alt={'ja': 'NEAR：着いた。歩くくらいの速さ（時速6km）で。生きてる。地球：！？着陸用じゃないのに！？', 'en': 'NEAR: I landed. At walking speed, 6 km/h. I’m alive. Earth: !? But you weren’t built to land!'},
  html=lambda: chat(
    who('NEAR', 'NEAR', 'r'), R('着いた', 'I’m down'),
    R('歩くくらいの速さ（時速6km）で', 'At walking speed (6 km/h)'),
    R('<b>生きてる</b>', '<b>I’m alive</b>', 'big'),
    who('地球', 'Earth'), L('！？！？', '!?!?', 'big'),
    L('着陸用じゃないのに！？', 'But you weren’t built to land!?'))),
 dict(dur=7, alt={'ja': 'ほんとの話：小惑星に着陸した世界で最初の探査機。そのあと約2週間、地面からデータを送りつづけた。最後の通信は2001年2月28日', 'en': 'True story: the first spacecraft ever to land on an asteroid. It kept sending data from the surface for about two weeks. Last contact: February 28, 2001'},
  html=lambda: bg('PIA02467', '50% 50%', 1.25, 'brightness(.9)') + shade('top') + col(
    tag('ほんとの話', 'True story', 'yellow'),
    h('小惑星に着陸した<br><em>世界で最初の探査機</em>', 'The <em>first spacecraft</em><br>to land on an asteroid', 'md'),
    bx('そのあと約2週間、地面からデータを送りつづけた', 'It kept sending data from the surface for about two weeks', 'sm'),
    bx('最後の通信は2001年2月28日。今もエロスの上にいる', 'Last contact: Feb 28, 2001. It is still sitting on Eros', 'sm green'))
   + cr('本物の写真：NEARシューメーカーが撮った小惑星エロス（NASA/JPL/JHUAPL）', 'Real photo: asteroid Eros, taken by NEAR Shoemaker (NASA/JPL/JHUAPL)')),
]
POST = dict(id='near-chat-1', account='near_shoemaker', place='deep', audio='media/music/sneaky_snitch.mp3',
 caption={'ja': '回るために作られたのに「着陸してみない？」と言われた探査機（結果は実話） #無茶ぶり #小惑星 #NEAR', 'en': 'Built to orbit, then asked “want to try landing?” (the ending is real) #groupchat #asteroid #NEAR'},
 tags=['chat', 'asteroid', 'NEAR'],
 sound={'ja': 'Kevin MacLeod「Sneaky Snitch」(CC BY 4.0)', 'en': 'Kevin MacLeod – Sneaky Snitch (CC BY 4.0)'},
 comments=pinned('near_shoemaker',
"""ほんとの話👇

NEARシューメーカーは、小惑星のまわりを回った世界で最初の探査機です。2000年2月から1年間、小惑星エロスを回って調べました。

■ 着陸用には作られていなかった
回って調べるための探査機で、着陸のための足はありません。1年間の仕事のあと、ゆっくりとエロスに降りていきました。

■ 降りながら写真を69枚
最後の1枚は高さ120mから撮ったものです。写真の下がすじになっているのは、送っている途中で着地して、信号がとぎれたからです。

■ 時速約6kmで着地、そして無事
2001年2月12日、歩くくらいの速さで着地しました。こわれずに、そのあと約2週間、地面からデータを送りつづけました。小惑星に着陸した最初の探査機になりました。

■ 最後の通信
2001年2月28日。−173℃の寒さのなかでした。今もエロスの上にあります。

※チャットの会話は、わたしたちが考えた演出です。NEARと地球のチームが、実際にこういう言葉をやりとりしたわけではありません。写真と出来事は本物です。""",
"""The real story 👇

NEAR Shoemaker was the first spacecraft to orbit an asteroid. It studied asteroid Eros from orbit for a year, starting in February 2000.

■ It was not built to land
It was an orbiter with no landing legs. After its year of work, it made a slow, controlled descent to Eros.

■ 69 photos on the way down
The last one was taken from 120 m up. The streaks at the bottom are where the signal was lost as it touched down while still sending the picture.

■ It touched down at about 6 km/h and survived
On Feb. 12, 2001 it landed at walking speed, then kept returning data from the surface for about two weeks. It became the first spacecraft to land on an asteroid.

■ Last contact
Feb. 28, 2001, in cold of minus 173°C. It is still sitting on Eros.

Note: the chat is our dramatization. NEAR and its team never exchanged these words. The photos and events are real."""),
 sources=[fact('NEAR Shoemaker (NASA Science): not designed as a lander, 69 photos, 6.4 km/h touchdown, two weeks of data, last contact Feb. 28, 2001', 'https://science.nasa.gov/mission/near-shoemaker/'),
  pj('PIA03148', 'Final Eros Images: Last, Closest Image of Eros (streaks = loss of signal at touchdown)', 'NASA/JPL/JHUAPL'),
  pj('PIA02467', 'NEAR First Whole-Eros Mosaic from Orbit', 'NASA/JPL/JHUAPL'), music('Sneaky Snitch')])
