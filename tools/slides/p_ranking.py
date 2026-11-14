"""Ranking: 'It was only supposed to be a short job.' How many times longer than planned did each machine work?"""
from lib import *
DIR = 'ranking'
def rank(n, name_ja, name_en, plan_ja, plan_en, act_ja, act_en, x):
    return col(
      f'<div class="rk">{t(f"{n}<small>位</small>", f"<small>No.</small>{n}")}</div>',
      h(name_ja, name_en, 'md'),
      f'''<div class="plan"><span>{t("予定", "Plan")}</span><div>{t(plan_ja, plan_en)}</div>
          <span>{t("実際", "Actual")}</span><div><em>{t(act_ja, act_en)}</em></div></div>''',
      f'<div class="x">{t(f"約<em>{x}</em>倍", f"about <em>{x}×</em>")}</div>', style='top:300px;gap:20px')
SLIDES = [
 dict(dur=4.5, alt={'ja': 'ランキング：「ちょっとだけでいいよ」と言われた機械たち。予定の何倍はたらいた？TOP5', 'en': 'Ranking: machines that were told “just a short job is fine.” How many times longer than planned did they work? Top 5'},
  html=lambda: bg('PIA04422', '35% 50%', 1.0, 'brightness(.55)') + shade('top') + col(
    tag('ランキング', 'Ranking', 'pink sm'),
    h('「ちょっとだけで<br>いいよ」と言われた<br>機械たち', 'Machines that were<br>told “just a short<br>job is fine”'),
    bx('予定の何倍はたらいた？ TOP5', 'How many times longer did they work? TOP 5', 'sm yellow'))
   + cr('本物の写真：打ち上げ前の火星探査車と、先輩ソジャーナの予備機（NASA/JPL）', 'Real photo: Mars rovers before launch, with a spare of the earlier Sojourner rover (NASA/JPL)')),
 dict(dur=5, alt={'ja': '5位：インジェニュイティ。予定は5回飛ぶこと、実際は72回。約14倍', 'en': 'No. 5: Ingenuity. Plan: 5 flights. Actual: 72 flights. About 14 times'},
  html=lambda: bg('PIA24648', '18% 50%', 1.35, 'brightness(.85)', '15% 45%') + shade('top') +
    rank(5, 'インジェニュイティ', 'Ingenuity', '5回飛ぶ', '5 flights', '72回飛んだ', '72 flights', 14)
   + cr('本物の写真：5回目の飛行を終えたインジェニュイティ（NASA/JPL-Caltech/ASU/MSSS）', 'Real photo: Ingenuity after its 5th flight (NASA/JPL-Caltech/ASU/MSSS)')),
 dict(dur=5, alt={'ja': '4位：パイオニア10号。予定は21か月、実際は30年以上。約18倍', 'en': 'No. 4: Pioneer 10. Plan: 21 months. Actual: over 30 years. About 18 times'},
  html=lambda: bg('ARC-1973-AC73-9019_c', '50% 40%', 1.0, 'brightness(.75)') + shade('top') +
    rank(4, 'パイオニア10号', 'Pioneer 10', '21か月', '21 months', '30年以上', 'over 30 years', 18)
   + cr('本物の写真：組み立て中のパイオニア10号（NASA Ames）', 'Real photo: Pioneer 10 being assembled (NASA Ames)')),
 dict(dur=6, alt={'ja': '2位（ほぼ同点）：スピリットとバイキング1号。どちらも予定は90日、実際は6年以上。約25倍', 'en': 'No. 2 (a near tie): Spirit and Viking 1. Both planned for 90 days, both worked over 6 years. About 25 times'},
  html=lambda: bg('PIA16442', '50% 50%', 1.0, 'brightness(.8)') + shade('top') +
    rank(2, 'スピリット ＆ バイキング1号<br>（ほぼ同点）', 'Spirit &amp; Viking 1<br>(a near tie)', 'どちらも90日', '90 days each', 'どちらも6年以上', 'over 6 years each', 25)
   + cr('本物の写真：スピリットが自分のまわりを撮った写真（NASA/JPL-Caltech/Cornell Univ./Arizona State Univ.）', 'Real photo: Spirit’s view of itself and its surroundings (NASA/JPL-Caltech/Cornell Univ./Arizona State Univ.)')),
 dict(dur=6, alt={'ja': '1位：オポチュニティ。予定は90日、実際は14年以上。約57倍', 'en': 'No. 1: Opportunity. Plan: 90 days. Actual: over 14 years. About 57 times'},
  html=lambda: bg('PIA22928', '50% 50%', 1.0, 'brightness(.8)') + shade('top') +
    rank(1, 'オポチュニティ', 'Opportunity', '90日', '90 days', '14年以上', 'over 14 years', 57)
   + cr('本物の写真：オポチュニティがふり返って撮った自分の車輪のあと（NASA/JPL-Caltech）', 'Real photo: Opportunity looking back at its own tracks (NASA/JPL-Caltech)')),
 dict(dur=6, alt={'ja': '置いていかれたんじゃない。最後まで働いて、そこで止まった。だから今も、火星や宇宙にいる', 'en': 'They were not thrown away. They worked to the very end and stopped right there. That is why they are still out there'},
  html=lambda: bg('PIA22928', '50% 50%', 1.0, 'brightness(.45)') + shade('all') + col(
    h('置いていかれたんじゃない', 'They weren’t thrown away', 'md'),
    h('<em>最後まで働いて</em>、<br>そこで止まった', 'They <em>worked to<br>the very end</em>', 'lg'),
    bx('だから今も、火星や宇宙にいる', 'That’s why they are still out there', 'sm green'), cls='mid')
   + cr('本物の写真：オポチュニティの車輪のあと（NASA/JPL-Caltech）', 'Real photo: Opportunity’s tracks (NASA/JPL-Caltech)')),
]
POST = dict(id='ranking-overtime-1', account='machine_ranking', place='mars', audio='media/music/hyperfun.mp3',
 caption={'ja': '「ちょっとだけでいいよ」と言われた機械たち、予定の何倍はたらいた？TOP5 #ランキング #火星 #オポチュニティ', 'en': 'Told “just a short job is fine.” How many times longer did they work? TOP 5 #ranking #mars #opportunity'},
 tags=['ranking', 'mars', 'opportunity'],
 sound={'ja': 'Kevin MacLeod「Hyperfun」(CC BY 4.0)', 'en': 'Kevin MacLeod – Hyperfun (CC BY 4.0)'},
 comments=pinned('machine_ranking',
"""計算のしかた👇（「何倍」は、わたしたちの計算です）

1位 オポチュニティ（火星）
予定は火星の90日。最後の通信は着陸から5,111日目（火星の日数）。5,111÷90＝約57倍
（NASAは、活動終了の発表までを数えて「60倍」としています）

2位 スピリット（火星）
予定は火星の90日。2004年1月から2010年3月まで、約6年2か月＝約25倍

2位 バイキング1号（火星）
予定は90日。1976年7月20日から1982年11月11日まで、約6年4か月＝約25倍
※スピリットとほとんど同じなので、同点にしました。だから3位はありません。

4位 パイオニア10号（宇宙）
予定は21か月。最後の信号まで約30年11か月＝約18倍

5位 インジェニュイティ（火星）
予定は最大5回の飛行。実際は72回＝約14倍

■ 今はどこに？
5台とも、最後に止まった場所（火星）や、飛んでいった先（宇宙）にあります。

※ランキングは演出です。予定と実際の数字はNASAの資料によります。""",
"""How we did the math 👇 (the "times longer" numbers are our own calculation)

No. 1 Opportunity (Mars)
Planned for 90 Martian days (sols). Its last message came on sol 5,111. 5,111 ÷ 90 ≈ 57×
(NASA, counting up to the end-of-mission announcement, says it exceeded its life expectancy by 60 times.)

No. 2 Spirit (Mars)
Planned for 90 sols. It worked from January 2004 to March 2010, about 6 years 2 months ≈ 25×

No. 2 Viking 1 (Mars)
Planned for 90 days. It worked from July 20, 1976 to Nov. 11, 1982, about 6 years 4 months ≈ 25×
Spirit and Viking 1 are so close that we called it a tie, so there is no No. 3.

No. 4 Pioneer 10 (deep space)
Designed for 21 months. Its last signal came about 30 years 11 months after launch ≈ 18×

No. 5 Ingenuity (Mars)
Planned for up to 5 flights. It made 72 ≈ 14×

■ Where are they now?
All five are still where they stopped (on Mars) or where they flew (deep space).

Note: the ranking is our dramatization. The planned and actual numbers come from NASA sources."""),
 sources=[fact('NASA: Opportunity Rover Mission on Mars Comes to End (designed for 90 Martian days and 1,000 m; exceeded life expectancy by 60 times)', 'https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end/'),
  fact('NASA JSC ARES: Mars Exploration Rovers were designed for a 90-sol mission', 'https://ares.jsc.nasa.gov/missions/mer/'),
  pj('PIA22929', "Opportunity's last data, June 10, 2018 (sol 5,111)", 'NASA/JPL-Caltech/Cornell/ASU'),
  fact('Mars Exploration Rovers Spirit and Opportunity (NASA Science): landings in January 2004, Spirit concluded in 2010', 'https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/'),
  fact('Viking 1 (NASA Science): landed July 20, 1976; stopped Nov. 11, 1982', 'https://science.nasa.gov/mission/viking-1/'),
  fact('NASA APPEL: Viking was originally intended to last 90 days after landing', 'https://appel.nasa.gov/2015/08/14/this-month-in-nasa-history-a-quest-commenced-for-life-on-mars'),
  fact('Pioneer 10 (NASA Science): designed for a 21-month mission; last signal Jan. 23, 2003', 'https://science.nasa.gov/mission/pioneer-10/'),
  fact('Ingenuity (NASA Science): no more than five test flights planned; 72 flights completed', 'https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/'),
  src('calc', 'Ratios: 5,111÷90 sols; Jan 4 2004–Mar 22 2010 (2,269 days) ÷ 92.5 days; Jul 20 1976–Nov 11 1982 (2,305 days) ÷ 90–92.5; 370.7÷21 months; 72÷5 flights', 'https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/'),
  pj('PIA04422', 'Rovers and Sojourner', 'NASA/JPL'), pj('PIA24648', 'Mastcam-Z Views Ingenuity After Fifth Flight', 'NASA/JPL-Caltech/ASU/MSSS'),
  nasa_img('ARC-1973-AC73-9019', 'Pioneer 10 spacecraft final assembly', 'NASA Ames'), pj('PIA16442', 'Spirit Mars Rover in McMurdo Panorama, Polar Projection', 'NASA/JPL-Caltech/Cornell Univ./Arizona State Univ.'),
  pj('PIA22928', 'Looking Back on a Golden Opportunity', 'NASA/JPL-Caltech'), music('Hyperfun')])
