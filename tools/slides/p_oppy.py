"""Opportunity: 'We sent more than a thousand commands. No reply.' (motion video only; see tools/motion/v_oppy.html)"""
from lib import *
DIR = 'opportunity'
SLIDES = []
POST = dict(id='opportunity-unread-1', account='opportunity_rover', place='mars',
 caption={'ja': '1000回送っても、既読がつかなかった（実話） #既読がつかない #火星 #オポチュニティ', 'en': 'We texted 1,000 times. No reply. (True story) #noreply #mars #opportunity'},
 tags=['opportunity', 'mars', 'chat'],
 sound={'ja': 'Kevin MacLeod「Heartbreaking」「Wholesome」(CC BY 4.0)', 'en': 'Kevin MacLeod – Heartbreaking / Wholesome (CC BY 4.0)'},
 comments=pinned('opportunity_rover',
"""ほんとの話👇

オポチュニティは、2004年から火星を走りつづけた探査車です。太陽の光で電気を作って動いていました。

■ 2018年6月、砂あらし
火星全体をおおう大きな砂あらしが起きて、太陽の光がとどかなくなりました。6月10日の通信が最後になりました。
チャットの中の暗い写真は、そのとき最後に届いた本物のデータです。太陽を撮ろうとしましたが、砂あらしで空が暗く、ほとんど何も写っていません。下が黒いのは、写真を全部送りきる前に通信がとぎれたからです。

■ 1000回以上の呼びかけ
NASAのチームは、通信を取りもどすために1000回以上の命令を送りました。2019年2月12日が最後の呼びかけでした。返事はなく、次の日、NASAは活動の終わりを発表しました。

■ 予定は90日
計画は「火星の90日間はたらいて、1,000m走る」こと。実際は14年以上はたらき、45km以上を走りました。昔の火星に水があった証拠も見つけました。

■ 今は？
今も火星の「パーシビアランス谷」にいます。

※チャットの会話と「未読」の表示は演出です。NASAが送ったのは、文字のメッセージではなく、機械への命令です。""",
"""The real story 👇

Opportunity was a rover that drove on Mars from 2004. It ran on solar power.

■ June 2018: the dust storm
A storm covered the whole planet and blocked the sunlight. Its last message came on June 10.
The dark photo in the chat is the real last data it sent. It tried to photograph the Sun, but the storm had made the sky so dark that almost nothing shows. The bottom is black because contact was lost before the whole picture was sent.

■ More than a thousand calls
NASA's team sent more than a thousand commands to restore contact. The last attempt was on Feb. 12, 2019. No answer came, and the next day NASA announced the mission was over.

■ The plan was 90 days
It was designed to last 90 Martian days and drive 1,000 meters. It worked for more than 14 years and drove over 45 km. It also found evidence that ancient Mars had water.

■ And now?
It is still in Perseverance Valley on Mars.

Note: the chat and the "Not read" labels are our dramatization. What NASA sent were commands to the machine, not text messages."""),
 sources=[fact('NASA: Opportunity Rover Mission on Mars Comes to End (more than a thousand commands; last attempt Feb. 12, 2019; designed for 90 Martian days and 1,000 m)', 'https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end/'),
  pj('PIA22929', "Opportunity's last data, June 10, 2018 (incomplete image)", 'NASA/JPL-Caltech/Cornell/ASU'),
  fact('Mars Exploration Rovers (NASA Science): 45.16 km; last communication June 10, 2018; evidence of past water', 'https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/'),
  pj('PIA22928', 'Looking Back on a Golden Opportunity', 'NASA/JPL-Caltech'), pj('PIA16120', "Opportunity's afternoon shadow at Endeavour Crater", 'NASA/JPL-Caltech'),
  music('Heartbreaking'), music('Wholesome')])
