"""Phoenix: spot the difference between two real photos taken four days apart (motion video only; see tools/motion/v_phoenix.html)"""
from lib import *
DIR = 'phoenix'
SLIDES = []
CR = 'NASA/JPL-Caltech/University of Arizona/Texas A&M University'
POST = dict(id='phoenix-spot-1', account='phoenix_lander', place='mars',
 caption={'ja': '【激ムズ】4日後、火星の穴から何かが消えた。見つけたら天才（本物の写真） #まちがい探し #火星 #フェニックス',
          'en': 'Very hard: 4 days later, something vanished from a hole on Mars. Can you spot it? (Real photos) #spotthedifference #mars #phoenix'},
 tags=['phoenix', 'mars', 'spot'],
 sound={'ja': 'Kevin MacLeod「Thinking Music」「Wallpaper」(CC BY 4.0)', 'en': 'Kevin MacLeod – Thinking Music / Wallpaper (CC BY 4.0)'},
 comments=pinned('phoenix_lander',
"""答え合わせ（ネタバレ注意）👇

■ 消えたもの
穴の左下、かげの中にあった白いつぶ（サイコロくらいの大きさ）。4日後の写真では、なくなっています。

■ どうして消えた？
白いつぶの正体は、水の氷。ほり出されて空気にふれた氷が、とけて水になる前に、そのまま気体になって消えました（昇華といいます）。

■ なぜすごい？
最初、この白いものは「塩かもしれない」と言われていました。でも、塩は消えません。消えたから氷だとわかった。研究チームは「氷にちがいない」と発表しました。
フェニックスは、火星の地面のすぐ下に水の氷があることをたしかめた機械です。

■ フェニックスはいま
2008年5月25日に火星の北極の平原に着陸。同じ年の11月2日に活動を終えて、いまもそこにあります。

※2枚とも、フェニックスが火星で撮った本物の写真です（2008年6月15日と19日）。かげの形がちがうのは、撮った時刻がちがうから。「まちがい探し」と「ビフォーアフター」は演出です。""",
"""Answer key (spoilers) 👇

■ What vanished
The white bits in the shadow at the lower left of the hole. They were about the size of dice. Four days later they are gone.

■ Why did they vanish?
They were water ice. Once the digging exposed the ice to the air, it turned straight into vapor without melting first. That is called sublimation.

■ Why does it matter?
At first, some people thought the bright material might be salt. But salt does not disappear. Because the bits vanished, the team said, “It must be ice.”
Phoenix confirmed that there is water ice just under the surface of Mars.

■ Where is Phoenix now?
It landed on the arctic plains of Mars on May 25, 2008. Its mission ended on Nov. 2, 2008, and it is still there.

Note: both pictures are real photos taken on Mars by Phoenix (June 15 and 19, 2008). The shadows look different because the photos were taken at different times of day. The “spot the difference” and “before / after” framing is ours.""") + [
  {'user': 'spirit_rover', 'text': {'ja': '3回見たけど、ヒントが出るまでぜんぜんわからなかった', 'en': 'Watched it three times. Had no idea until the hint showed up.'}},
  {'user': 'viking1_lander', 'text': {'ja': 'かげの形もちがうよ、と思ったら、撮った時刻がちがうだけだった', 'en': 'I thought the shadows were the answer. They just took the photos at different times of day.'}}],
 sources=[fact('Phoenix (NASA Science): landed May 25, 2008 on the arctic plains of Mars; end of mission Nov. 2, 2008; verified water ice in the Martian subsurface; bright clumps "had vaporized four days after the scoop"', 'https://science.nasa.gov/mission/phoenix/'),
  fact("NASA/JPL news, June 19, 2008: Bright Chunks at Phoenix Lander's Mars Site Must Have Been Ice (dice-size crumbs vanished; \"Salt can't do that\")", 'https://www.jpl.nasa.gov/news/bright-chunks-at-phoenix-landers-mars-site-must-have-been-ice/'),
  pj('PIA10910', 'Ice on Mars - Now You See It (Sol 20, June 15, 2008)', CR), pj('PIA10911', "Ice on Mars -- Now it's Gone (Sol 24)", CR),
  pj('PIA10906', 'Disappearing Ice (sublimation of ice in the Dodo-Goldilocks trench over four days)', CR),
  pj('PIA11719', 'Phoenix Lander Self Portrait on Mars, Vertical Projection', CR),
  music('Thinking Music'), music('Wallpaper')])
