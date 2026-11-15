"""Sojourner: a 'day N' daily vlog. Planned for 7 days, worked for 83 (motion video only; see tools/motion/v_sojourner.html)"""
from lib import *
DIR = 'sojourner'
SLIDES = []
FACTS = 'https://mars.nasa.gov/internal_resources/815/'
POST = dict(id='sojourner-vlog-1', account='sojourner_rover', place='mars',
 caption={'ja': '【火星ではたらくVlog】3日目：36cm進んで石をさわった。きょうはもう充分はたらいた（実話） #Vlog #○日目 #ソジャーナ',
          'en': 'Working on Mars, day 3: drove 1.2 feet, touched a rock. Feeling productive. (True story) #vlog #dayinmylife #sojourner'},
 tags=['sojourner', 'mars', 'vlog'],
 sound={'ja': 'Kevin MacLeod「Carefree」(CC BY 4.0)', 'en': 'Kevin MacLeod – Carefree (CC BY 4.0)'},
 comments=pinned('sojourner_rover',
"""Vlogの補足（ぜんぶ実話）👇

■ 1日目（1997年7月4日）
エアバッグにつつまれて着陸。15回くらい、高さ15mまではねました。エアバッグが出口のスロープをふさいでいて、この日は着陸機の上で待機。通信もうまくいかず、文を最後まで送れませんでした（次の日に直りました）。

■ 2日目
この日のおわりごろ、30cmの高さに立ち上がって、スロープをおりて地面へ。

■ 3日目
約36cm進んで、「バーナクル・ビル」と名付けられた石に、成分をはかる機械を一晩おし当てました。これがソジャーナの最初の石しらべです。

■ 7日の予定が83日
予定の12倍はたらきました。最高速度は秒速1cm。石や土の成分を15回以上はかり、写真を550枚撮りました。岩には「ヨギ」「シャーク」など、あだ名がついています。

■ このあと、どうなった？
83日目（9月27日）を最後に、親機（着陸機）からデータが来なくなりました。ソジャーナは、親機を通してしか地球と話せません。NASAの資料によると、ソジャーナは数日後に「もしもの時モード」に入り、親機のまわりをぐるぐる回るか、その場で指示を待っていたと考えられています。

■ なぜすごい？
ソジャーナは、火星を走ったはじめての探査車。その実験は、あとの火星探査車をよくするためのものでもありました。

※写真はぜんぶ本物です（NASA/JPL）。セリフとVlogの形は演出。7日目と8日目の画面は写真ではなく、イラストです。""",
"""Notes on the vlog (all true) 👇

■ Day 1 (July 4, 1997)
It landed wrapped in airbags and bounced about 15 times, as high as 50 feet (15 m). An airbag was blocking the exit ramp, so the rover waited on top of the lander. Its radio link was also having trouble: it could not finish its messages. (That was fixed the next day.)

■ Day 2
Late in the day it stood up to its full height of 1 foot (30 cm) and rolled down the ramp to the ground.

■ Day 3
It drove about 1.2 feet (36 cm) to a rock nicknamed “Barnacle Bill” and pressed its instrument against it overnight to measure what the rock is made of. That was Sojourner’s first rock.

■ Planned for 7 days, worked for 83
That is 12 times longer than planned. Top speed: 1 centimeter per second. It made more than 15 chemical analyses of rocks and soil and took 550 pictures. The team gave the rocks nicknames such as “Yogi” and “Shark.”

■ What happened next?
After day 83 (Sept. 27), no more data came from the lander. Sojourner could only talk to Earth through the lander. According to NASA, the rover is assumed to have gone into a backup mode within a few days: either circling the lander again and again, or standing in place, waiting for instructions.

■ Why does it matter?
Sojourner was the first rover ever to drive on Mars. Its experiments were also meant to make future Mars rovers better.

Note: every photo is real (NASA/JPL). The lines and the vlog format are ours. The day 7 and day 8 screens are drawings, not photos.""") + [
  {'user': 'opportunity_rover', 'text': {'ja': '先輩…！7日の予定で83日。その記録、あとでわたしたちが受けつぎました', 'en': 'Senpai…! Seven days planned, 83 worked. We carried that tradition on later.'}},
  {'user': 'spirit_rover', 'text': {'ja': '36cmで「充分はたらいた」は、ちょっとわかる', 'en': '“1.2 feet. Feeling productive.” Honestly, I get it.'}}],
 sources=[fact('NASA Facts: Mars Pathfinder (JPL). Day-by-day events, 36 cm trip to Barnacle Bill on sol 3, top speed 1 cm/s, rover outlived its design life 12 times, last data on sol 83, assumed contingency mode', FACTS),
  fact('Mars Pathfinder (NASA Science): delivered the first-ever robotic rover, Sojourner, to the Martian surface; landing July 4, 1997', 'https://science.nasa.gov/mission/mars-pathfinder/'),
  fact('Mars Pathfinder Rover (NASA NSSDCA): primary objectives planned for the first seven sols; all rover communications went through the lander', 'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=MESURPR'),
  fact("For @opportunity_rover's comment: NASA: Opportunity was designed for 90 Martian days and worked for more than 14 years", 'https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end/'),
  pj('PIA00621', 'Color Mosaic of Rover & Terrain (Sol 1, rover still latched to the lander petal)', 'NASA/JPL'), pj('PIA01551', 'Newly Deployed Sojourner Rover (Sol 2)', 'NASA/JPL'),
  pj('PIA00634', 'Sojourner APXS studies Barnacle Bill (Sol 3)', 'NASA/JPL'), pj('PIA00921', 'Sojourner APXS at Shark (Sol 52)', 'NASA/JPL'),
  pj('PIA00967', 'Sojourner at "Moe" - Color (Sol 65; "83 days of a planned seven-day mission")', 'NASA/JPL'), pj('PIA01585', 'Sojourner APXS at Chimp (Sol 80, Sept. 23, 1997)', 'NASA/JPL'),
  pj('PIA01121', 'Sojourner Rover View of Pathfinder Lander (Sol 33)', 'NASA/JPL'), pj('PIA01122', 'Sojourner Rover Near The Dice (Sol 22)', 'NASA/JPL'), pj('PIA00766', 'Sojourner & Yogi', 'NASA/JPL'),
  music('Carefree')])
