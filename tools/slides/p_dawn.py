"""Dawn: a parody of a 'while they were out partying, I was grinding' motivation video (motion video only; see tools/motion/v_dawn.html)"""
from lib import *
DIR = 'dawn'
SLIDES = []
CR = 'NASA/JPL-Caltech/UCLA/MPS/DLR/IDA'
POST = dict(id='dawn-grind-1', account='dawn_spacecraft', place='deep',
 caption={'ja': 'みんなが遊んでる間に、ぼくは4日かけて時速96kmまで加速してた（ぜんぶ本当の数字） #モチベ #努力 #ドーン',
          'en': 'While they were out partying, I spent 4 days getting to 60 mph. (All real numbers) #motivation #grind #dawn'},
 tags=['dawn', 'deep', 'motivation'],
 sound={'ja': 'Kevin MacLeod「Heroic Age」(CC BY 4.0)', 'en': 'Kevin MacLeod – Heroic Age (CC BY 4.0)'},
 comments=pinned('dawn_spacecraft',
"""数字の解説（ぜんぶ本当）👇

■ 4日かけて時速96km
ドーンのイオンエンジンは、全力でも「時速0→96km（60マイル）」に4日かかります（NASA）。

■ 押す力は紙1枚ぶん
エンジンが押す力は、手のひらに紙を1枚のせたときの重さくらい（NASA）。

■ それでもすごい理由
宇宙にはじゃまをする空気がほとんどないので、弱い力でも押し続ければ速さがたまっていきます。ドーンは合計5.9年（2,141日）エンジンをふかして、時速41,400kmぶんの速さを足しました。探査機が自分のエンジンで出した速さの変化としては記録です（NASA）。
※「足した速さの合計」で、いまの速さではありません。

■ ドーンがしたこと
小惑星ベスタ（2011年）と準惑星ケレス（2015年）。2つの星のまわりを回った、はじめての探査機です。2018年に通信が終わり、いまもケレスのまわりを回っています。

■ おまけ（わたしたちの計算）
この加速で50m走をすると、ゴールまで約19分かかります。

※「みんなが遊んでる間に…」は演出です。数字はNASAの資料によります。""",
"""The numbers (all real) 👇

■ 4 days to reach 60 mph
At full throttle, Dawn’s ion engine takes four days to go from 0 to 60 mph (NASA).

■ The push of one sheet of paper
The engine pushes about as hard as a single sheet of paper resting on your hand (NASA).

■ Why that is still amazing
In space there is almost no air to slow you down, so even a tiny push keeps adding speed. Dawn fired its engines for a total of 5.9 years (2,141 days) and added 25,700 mph of speed. NASA calls that the greatest change in speed any spacecraft has made with its own engines.
Note: that is the total speed it added, not how fast it is moving now.

■ What Dawn did
It orbited the giant asteroid Vesta (2011) and the dwarf planet Ceres (2015): the first spacecraft to orbit two different worlds beyond Earth. Contact ended in 2018, and it is still circling Ceres.

■ Bonus (our own calculation)
With this acceleration, a 50-meter dash would take about 19 minutes.

Note: the “while they were out partying” framing is ours. The numbers come from NASA sources.""") + [
  {'user': 'opportunity_rover', 'text': {'ja': 'モチベ上がった。わたしも「ゆっくりでも止まらない」派です', 'en': 'Feeling motivated. I am on team “slow, but never stop” too.'}},
  {'user': 'near_shoemaker', 'text': {'ja': '小惑星なかま！こっちはエロスに着陸して、そのまま座ってる', 'en': 'Fellow asteroid visitor! I landed on Eros and I have been sitting here ever since.'}}],
 sources=[fact('Dawn quick facts (NASA Science): acceleration at full thrust 0–60 mph in 4 days; thrust 19 to 91 millinewtons; first spacecraft to orbit two extraterrestrial targets', 'https://science.nasa.gov/mission/dawn/toolkit/quick-facts/'),
  fact('Dawn ion propulsion (NASA Science): 91 millinewtons is about the force of holding a single piece of notebook paper in your hand', 'https://science.nasa.gov/mission/dawn/technology/ion-propulsion/'),
  fact('What We Learned from Dawn (NASA Science): record for the greatest velocity change (25,700 mph or 41,400 km/h) by a spacecraft with its own propulsion; only spacecraft to orbit two deep-space destinations', 'https://science.nasa.gov/mission/dawn/toolkit/highlights/'),
  fact('Dawn Journal (NASA/JPL): Dawn thrust for a total of 2,141 days (5.9 years); the velocity change is not its current speed', 'https://www.jpl.nasa.gov/blog/columns/dawn-journal/'),
  fact('Dawn (NASA Science): Vesta and Ceres; launched Sept. 27, 2007', 'https://science.nasa.gov/mission/dawn/'),
  fact("For @near_shoemaker's comment: NASA Science: NEAR Shoemaker (landed on Eros on Feb. 12, 2001)", 'https://science.nasa.gov/mission/near-shoemaker/'),
  src('calc', '50 m dash: 60 mph (26.8 m/s) in 4 days (345,600 s) gives 7.76e-5 m/s²; t = √(2×50÷a) ≈ 1,135 s ≈ 19 minutes', 'https://science.nasa.gov/mission/dawn/toolkit/quick-facts/'),
  src('art', 'PIA18922 Dawn Blue Glow Artist Concept (NASA/JPL-Caltech)', 'https://photojournal.jpl.nasa.gov/catalog/PIA18922'),
  src('art', 'PIA20919 Dawn Artist Concept Realistic Ceres (' + CR + ')', 'https://photojournal.jpl.nasa.gov/catalog/PIA20919'),
  pj('PIA14894', 'Capturing the Surface of Asteroid Vesta (July 24, 2011)', CR), pj('PIA21078', 'Occator on Ceres Limb', CR),
  music('Heroic Age')])
