"""Viking 1 x case file: 'It worked on Mars for 6 years. Then it went silent. Who did it?'"""
from lib import *
DIR = 'viking'
def photo(nid, cap_ja, cap_en, w=760, rot=-2):
    return f'<figure class="ph" style="width:{w}px;transform:rotate({rot}deg)"><img src="file://{ASSETS}/{nid}.jpg"><figcaption>{t(cap_ja, cap_en)}</figcaption></figure>'
BLUR = 'blur(14px) brightness(.5) saturate(1.1)'
SLIDES = [
 dict(dur=5, alt={'ja': '事件ファイル：火星で6年、まじめに働いていた着陸機が、ある日とつぜん消えた', 'en': 'Case file: a lander worked on Mars for 6 years. Then one day it went silent'},
  html=lambda: bg('PIA00567', '50% 50%', 1.08, 'brightness(.62)') + shade('top') + col(
    f'<div class="stamp">{t("事件ファイル", "CASE FILE")}</div>',
    h('火星で<em>6年</em>、まじめに<br>働いていた着陸機が', 'A lander worked hard<br>on Mars for <em>6 years</em>', 'md'),
    h('ある日とつぜん<br><b>消えた</b>', 'Then one day<br>it <b>went silent</b>', 'lg'))
   + cr('本物の写真：バイキング1号が撮った火星の夕方（NASA/JPL）', 'Real photo: evening on Mars, taken by Viking 1 (NASA/JPL)')),
 dict(dur=6, alt={'ja': 'プロフィール。名前：バイキング1号。火星に着いた日：1976年7月20日。予定：90日。実際：6年以上。仕事：写真、天気の報告、生き物さがし', 'en': 'Profile. Name: Viking 1. Landed on Mars: July 20, 1976. Plan: 90 days. Actual: over 6 years. Job: photos, weather reports, looking for life'},
  html=lambda: bg('PIA00563', '50% 50%', 1.1, BLUR) + col(
    photo('PIA09703', '地球で作った模型の写真（NASA/JPL-Caltech/University of Arizona）', 'Photo of a model built on Earth (NASA/JPL-Caltech/University of Arizona)', 620, 2),
    f'''<div class="card"><h3>{t("消えた着陸機のプロフィール", "Profile of the missing lander")}</h3>
      <div class="row"><span>{t("名前", "Name")}</span><b>{t("バイキング1号", "Viking 1")}</b></div>
      <div class="row"><span>{t("火星に着いた日", "Landed on Mars")}</span><b>{t("1976年7月20日", "July 20, 1976")}</b></div>
      <div class="row"><span>{t("予定", "Plan")}</span><b>{t("90日", "90 days")}</b></div>
      <div class="row"><span>{t("実際", "Actual")}</span><b style="color:#e5202a">{t("6年以上", "over 6 years")}</b></div>
      <div class="row"><span>{t("仕事", "Job")}</span><b>{t("写真・天気の報告・生き物さがし", "Photos, weather, looking for life")}</b></div></div>''', style='top:310px;gap:30px')),
 dict(dur=5.5, alt={'ja': '手がかり①：火星に着いて最初に撮った写真。うつっているのは自分の足。火星の地面で撮られた、世界で最初の写真', 'en': 'Clue 1: the first photo it took on Mars shows its own foot. It is the first photograph ever taken on the surface of Mars'},
  html=lambda: bg('PIA00563', '50% 50%', 1.1, BLUR) + col(
    tag('手がかり①', 'Clue 1', 'red sm'),
    h('着いて最初に撮ったのは<br><em>自分の足</em>', 'Its very first photo:<br><em>its own foot</em>', 'md'),
    photo('PIA00381', '1976年7月20日。右下が着陸機の足（NASA/JPL）', 'July 20, 1976. The lander’s footpad is at lower right (NASA/JPL)', 840, -1.5),
    bx('火星の地面で撮られた、世界で最初の写真', 'The first photo ever taken on the surface of Mars', 'sm yellow'))),
 dict(dur=9, alt={'ja': 'クイズ：通信がとぎれた原因は？ A 砂あらし B 寒さ C 宇宙人 D 地球', 'en': 'Quiz: what cut off the signal? A a dust storm B the cold C aliens D Earth'},
  quiz={'choices': [{'ja': '砂あらし', 'en': 'A dust storm'}, {'ja': '寒さ', 'en': 'The cold'}, {'ja': '宇宙人', 'en': 'Aliens'}, {'ja': '地球', 'en': 'Earth'}], 'answer': 3},
  html=lambda: bg('PIA00563', '50% 50%', 1.1, BLUR) + col(
    tag('ここでクイズ', 'Quiz time', 'red sm'),
    h('1982年、通信がとぎれた。<br><em>原因は？</em>', 'In 1982 the signal stopped.<br><em>What caused it?</em>', t('md', 'sm')), style='top:350px')),
 dict(dur=6, alt={'ja': '答え：原因は地球。地球から送った命令にまちがいがあった。それっきり返事はこなかった', 'en': 'Answer: Earth. A command sent from Earth had a mistake in it. Viking 1 never answered again'},
  html=lambda: bg('as17-148-22727', '50% 50%', 1.0, 'brightness(.8)') + shade('top') + col(
    tag('答え', 'Answer', 'green sm'),
    h('原因は<b>地球</b>', 'It was <b>Earth</b>', 'xl'),
    bx('1982年11月。地球から送った命令に、まちがいがあった', 'Nov 1982: a command sent from Earth had a mistake in it', 'sm'),
    bx('何度呼びかけても、返事はこなかった', 'They kept calling. No answer ever came', 'sm'))
   + cr('本物の写真：アポロ17号から見た地球（NASA）', 'Real photo: Earth seen from Apollo 17 (NASA)')),
 dict(dur=6, alt={'ja': '24年後の2006年、火星の上空を回る探査機が、写真でバイキング1号の場所をつきとめた。今も火星にいる', 'en': '24 years later, in 2006, an orbiter pinpointed Viking 1 in a photo. It is still on Mars'},
  html=lambda: bg('PIA01881', '40% 50%', 1.0, 'brightness(.8)') + shade('top') + col(
    tag('24年後', '24 years later', 'white sm'),
    h('<em>見つけてもらえた</em>', '<em>Found again</em>', 'lg'),
    bx('2006年。上空を回る探査機が、写真で場所をつきとめた', '2006: an orbiter pinpointed it in a photo', 'sm'),
    bx('今も、火星の同じ場所にいる', 'It is still there, in the same spot', 'sm green'))
   + cr('本物の写真：バイキング1号が着陸した場所。上空の探査機MROが撮影（NASA/JPL-Caltech/University of Arizona）', 'Real photo: the Viking 1 landing area seen by the MRO orbiter (NASA/JPL-Caltech/University of Arizona)')),
]
POST = dict(id='viking-casefile-1', account='viking1_lander', place='mars', audio='media/music/investigations.mp3',
 caption={'ja': '火星で6年はたらいた着陸機が、ある日とつぜん消えた。原因を当ててみて #事件ファイル #火星 #バイキング1号', 'en': 'A lander worked on Mars for 6 years, then went silent. Can you guess why? #casefile #mars #viking1'},
 tags=['casefile', 'mars', 'viking1', 'quiz'],
 sound={'ja': 'Kevin MacLeod「Investigations」(CC BY 4.0)', 'en': 'Kevin MacLeod – Investigations (CC BY 4.0)'},
 comments=pinned('viking1_lander',
"""答え合わせ👇
正解は D「地球」です。

バイキング1号は、1976年7月20日に火星に着陸しました。火星への着陸に本当の意味で成功した、最初の探査機です。

■ 最初の写真は自分の足
着陸してすぐに撮った1枚目は、火星の地面で撮られた世界で最初の写真です。右下に着陸機の足が写っています。

■ 90日の予定が6年以上
計画は着陸から90日でした。実際は6年以上動きつづけ、写真や天気の報告を地球に送りました。火星に生き物がいるかどうかを調べる実験もしました。

■ なぜ通信がとぎれた？
1982年11月11日、地球から送った命令にまちがいがあり、通信がとぎれました。そのあと通信を取りもどそうとしましたが、うまくいきませんでした。砂あらしでも、寒さでも、宇宙人でもありません。

■ 今は？
今も火星のクリュセ平原にあります。2006年には、火星を回る探査機MROの写真で、正確な場所がつきとめられました。

※「事件ファイル」「手がかり」は演出です。写真と出来事は本物です。""",
"""The answer 👇
It's D, Earth.

Viking 1 landed on Mars on July 20, 1976. NASA calls it the first truly successful landing on Mars.

■ Its first photo was its own foot
The first picture it took right after landing is the first photograph ever taken on the surface of Mars. You can see the lander's footpad at the lower right.

■ Planned for 90 days, worked for over 6 years
It kept sending photos and weather reports, and ran experiments to look for signs of life.

■ Why did the signal stop?
On Nov. 11, 1982, a faulty command sent from Earth interrupted communications. Later attempts to regain contact did not succeed. It was not a dust storm, the cold, or aliens.

■ And now?
It is still on Chryse Planitia. In 2006 the MRO orbiter's camera pinpointed exactly where it sits.

Note: the "case file" and "clues" are our dramatization. The photos and events are real."""),
 sources=[fact('Viking 1 (NASA Science): landing, operations, faulty command on Nov. 11, 1982', 'https://science.nasa.gov/mission/viking-1/'),
  fact('NASA APPEL: Viking was originally intended to last 90 days after landing', 'https://appel.nasa.gov/2015/08/14/this-month-in-nasa-history-a-quest-commenced-for-life-on-mars'),
  pj('PIA00381', 'First Photograph Taken On Mars Surface', 'NASA/JPL'), pj('PIA00563', 'First Color Image From Viking Lander 1', 'NASA/JPL'),
  pj('PIA00567', 'Sunset at the Viking Lander 1 Site', 'NASA/JPL'), pj('PIA09703', 'Viking Lander Model', 'NASA/JPL-Caltech/University of Arizona'),
  pj('PIA01881', 'Viking Lander 1 Thomas A. Mutch Memorial Station Imaged from Orbit', 'NASA/JPL-Caltech/University of Arizona'),
  nasa_img('as17-148-22727', 'View of the Earth seen by the Apollo 17 crew'), music('Investigations')])
