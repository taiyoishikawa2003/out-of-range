"""Captions, comments and profile text for the feed: the one place to edit wording.

Run `python3 tools/apply_texts.py` after any build step; it writes these into data/posts.json and data/accounts.json.
Rules we follow here:
- A caption is short and uses the words of its format. Three hashtags: the format, the place, the machine.
- The pinned comment opens with the answer, then says what the machine is, why it was sent, what it found and where it is now.
- Comments from other machines are short and sound like comments, not like fact sheets.
- A fact appears only if it is in that post's sources.
"""

# ---------- accounts ----------
# kind: machine (the machine itself speaks), channel (a fan channel about the machines), pr (the trailer slot)
# since: when contact was lost ("out of range"), shown on the profile of each machine
ACCOUNTS = {
 'insight_lander': dict(kind='machine', name=('インサイト', 'InSight'), since=('2022年12月から圏外', 'Out of range since December 2022'),
    bio=('火星の着陸機。4年間、地面に耳をあてていました。', 'Mars lander. I spent four years with my ear to the ground.')),
 'opportunity_rover': dict(kind='machine', name=('オポチュニティ', 'Opportunity'), since=('2018年6月から圏外', 'Out of range since June 2018'),
    bio=('火星の探査車。90日の予定で来て、14年はたらきました。', 'Mars rover. I came for 90 days and worked for 14 years.')),
 'spirit_rover': dict(kind='machine', name=('スピリット', 'Spirit'), since=('2010年3月から圏外', 'Out of range since March 2010'),
    bio=('火星の探査車。オポチュニティのふたご。前の車輪がひとつ、こわれてます。', 'Mars rover. Opportunity’s twin. One of my front wheels is broken.')),
 'viking1_lander': dict(kind='machine', name=('バイキング1号', 'Viking 1'), since=('1982年11月から圏外', 'Out of range since November 1982'),
    bio=('火星の着陸機。1976年からここにいます。最初に撮ったのは、自分の足。', 'Mars lander. Here since 1976. My first photo was of my own foot.')),
 'viking2_lander': dict(kind='machine', name=('バイキング2号', 'Viking 2'), since=('1980年4月から圏外', 'Out of range since April 1980'),
    bio=('火星の着陸機。ユートピア平原に住んで50年。ちょっとかたむいてます。', 'Mars lander. 50 years on Utopia Planitia. I lean a little.')),
 'surveyor3': dict(kind='machine', name=('サーベイヤー3号', 'Surveyor 3'), since=('1967年5月から圏外', 'Out of range since May 1967'),
    bio=('月の探査機。1967年からここにいます。一度だけ、人が来ました。', 'Moon lander. Here since 1967. People came to see me, once.')),
 'pioneer10': dict(kind='machine', name=('パイオニア10号', 'Pioneer 10'), since=('2003年1月から圏外', 'Out of range since January 2003'),
    bio=('1972年に出発。アルデバランの方向へ、あと200万年以上。', 'Left in 1972. Heading toward Aldebaran. More than 2 million years to go.')),
 'pioneer11': dict(kind='machine', name=('パイオニア11号', 'Pioneer 11'), since=('1995年から圏外', 'Out of range since 1995'),
    bio=('木星のつぎに、土星へ。帰りの便はありません。', 'Jupiter, then Saturn. No return ticket.')),
 'near_shoemaker': dict(kind='machine', name=('NEARシューメーカー', 'NEAR Shoemaker'), since=('2001年2月から圏外', 'Out of range since February 2001'),
    bio=('小惑星エロスの上にいます。着陸する予定は、なかったんですけど。', 'I am sitting on asteroid Eros. Landing was not in the plan.')),
 'phoenix_lander': dict(kind='machine', name=('フェニックス', 'Phoenix'), since=('2008年11月から圏外', 'Out of range since November 2008'),
    bio=('火星の北極の平原で、氷をほりました。', 'I dug for ice on the arctic plains of Mars.')),
 'dawn_spacecraft': dict(kind='machine', name=('ドーン', 'Dawn'), since=('2018年から圏外', 'Out of range since 2018'),
    bio=('4日かけて、やっと時速96km。それを5.9年つづけました。いまはケレスのまわり。', 'Four days to reach 60 mph. I kept that up for 5.9 years. Now circling Ceres.')),
 'sojourner_rover': dict(kind='machine', name=('ソジャーナ', 'Sojourner'), since=('1997年9月から圏外', 'Out of range since September 1997'),
    bio=('火星を走った最初の探査車。最高速度は秒速1cm。', 'The first rover on Mars. Top speed: 1 centimeter per second.')),
 'moon_lostfound': dict(kind='channel', name=('月面遺失物センター', 'Lunar Lost & Found'),
    bio=('月に置いてきた物を、あずかっています。', 'We look after the things people left on the Moon.')),
 'kepler_uranai': dict(kind='channel', name=('ケプラー星占い', 'Kepler Horoscope'),
    bio=('ケプラー望遠鏡の本物のデータで作る星座ランキング。占いは科学ではありません。', 'Zodiac rankings made from real Kepler data. Astrology is not science.')),
 'space_runway': dict(kind='channel', name=('月・火星コレクション', 'Moon & Mars Collection'),
    bio=('置いてきた機械のファッションチェック。見た目には、ぜんぶ理由がある。', 'Fashion checks for the machines left on the Moon and Mars. Every look has a reason.')),
 'machine_ranking': dict(kind='channel', name=('置いてきた機械ランキング', 'Left-Behind Machine Rankings'),
    bio=('NASAの本物の数字で、ランキングを作っています。', 'Rankings made from real NASA numbers.')),
 'tanken_shindan': dict(kind='channel', name=('探査機タイプ診断', 'Which Machine Are You?'),
    bio=('お遊びの診断。機械の話は本当です。', 'A just-for-fun quiz. The machine facts are real.')),
 'machine_aruaru': dict(kind='channel', name=('置いてきた機械あるある', 'Left-Behind Machines: So Relatable'),
    bio=('置いてきた機械の「あるある」を、本物の写真で。', 'Things left-behind machines always do, in real photos.')),
 'opportunity_trailer': dict(kind='pr', name=('OPPORTUNITY（予告編）', 'OPPORTUNITY (trailer)'),
    bio=('オポチュニティの14年を、映画の予告の形にしました。', 'Opportunity’s 14 years, cut like a movie trailer.')),
}

# ---------- posts ----------
# caption=(ja, en)            replaces the caption
# pinned=(ja, en)             replaces the whole pinned comment
# head=(ja, en)               replaces only the first line of the existing pinned comment
# sub=[(old, new), ...]       small in-place edits to the existing pinned comment (either language)
# comments=[(user, ja, en)]   replaces every comment that is not pinned
POSTS = {
 'insight-kaidan-1': dict(
    caption=('誰もいない火星で、音が3回。 #意味がわかると怖い話 #火星 #インサイト', 'No one was on Mars. Something made a sound. 3 times. #creepy #mars #InSight'),
    sub=[('インサイトにマイクはありません。聞いていたのは「地震計」です。',
          'インサイトにマイクはありません。聞いていたのは「地震計」です。\n\n■ インサイトって？\n火星の中身を調べるために送られた着陸機です。2018年11月に火星に着きました。'),
         ('InSight had no microphone. It was listening with its seismometer.',
          'InSight had no microphone. It was listening with its seismometer.\n\n■ What was InSight?\nA lander sent to study the inside of Mars. It reached Mars in November 2018.'),
         ('\n\n※動画の風の音は', '\n\n■ いまは？\n太陽電池に砂がつもって、2022年12月に通信が終わりました。今も火星のエリシウム平原にあります。\n\n※動画の風の音は'),
         ('\n\nNote: the wind sound was', '\n\n■ And now?\nDust piled up on its solar panels, and contact ended in December 2022. It is still on Elysium Planitia on Mars.\n\nNote: the wind sound was'),],
    comments=[
    ('viking1_lander', 'こわくて3回見た', 'So scary I watched it three times.', dict(fact=False)),
    ('opportunity_rover', '隕石さん、こっちには落ちないでね（同じ火星にいます）', 'Dear meteoroids, please do not land on me. (Same planet.)')]),

 'surveyor-pov-1': dict(
    caption=('月で2年半ひとりで待ってたら、人が来た #POV #月 #サーベイヤー3号', 'POV: you waited alone on the Moon for 2.5 years. Then people showed up. #POV #moon #surveyor3'),
    pinned=("""答え合わせ👇

サーベイヤー3号は、人が降りる前に月の地面を調べに来た、無人の探査機です。1967年4月に月に着きました。

■ 着陸でバウンドした
エンジンが止まらず、月面で2回はねました（1回目は高さ約10m、2回目は約3m）。3回目でやっと止まりました。

■ 月で何をした？
写真を6,326枚送り、スコップで土をほって、かたさを調べました。「月の地面は、人が乗る着陸船を支えられる」と分かりました。最後の通信は1967年5月4日です。

■ 2年半後に人が来た
1969年11月、アポロ12号が約180m先に着陸。宇宙飛行士2人が歩いてきて、テレビカメラやスコップを外し、地球に持ち帰りました。

■ なぜ持ち帰った？
月に約2年半置いた機械がどうなるかを、科学者が調べるためです。

■ いまは？
今も月の「嵐の大洋」にあります。2009年に月を回る探査機LROが撮った写真に、アポロ12号の着陸船の下の部分と、サーベイヤー3号と、宇宙飛行士が歩いたあとが写っています。

※セリフは演出。写真は本物です。最後の写真の丸と名前は、わたしたちが書き足しました。""",
"""The real story 👇

Surveyor 3 was a robot lander sent to test the Moon’s surface before people landed. It reached the Moon in April 1967.

■ It bounced
Its engine did not shut off in time, so it bounced off the Moon twice (about 10 m high, then about 3 m) and settled on the third touchdown.

■ What did it do?
It sent 6,326 pictures and dug into the soil with a scoop to test how firm it was. That showed the ground could hold a lander with people in it. Its last contact was on May 4, 1967.

■ 2.5 years later, people came
In November 1969, Apollo 12 landed about 180 m away. Two astronauts walked over, took off the TV camera and the scoop, and brought them back to Earth.

■ Why take them?
So scientists could study what two and a half years on the Moon does to a machine.

■ And now?
It is still in the Ocean of Storms. A 2009 photo from the LRO orbiter shows the Apollo 12 descent stage, Surveyor 3 and the astronauts’ footpaths.

Note: the lines are ours. The photos are real. We added the circles and labels on the last photo."""),
    comments=[
    ('moon_lostfound', '遺失物センターです。カメラは落とし物ではありません。地球へのお持ち帰りです', 'Lost & Found here. The camera is not a lost item. It was taken home to Earth.'),
    ('near_shoemaker', '人が会いに来てくれたの、いいなあ', 'People came to see you. Lucky.')]),

 'phoenix-spot-1': dict(
    caption=('【激ムズ】4日後、火星の穴から何かが消えた #まちがい探し #火星 #フェニックス', 'Very hard: 4 days later, something is missing from this hole on Mars #spotthedifference #mars #phoenix'),
    pinned=("""答え合わせ（ネタバレ注意）👇

消えたのは、穴の左下のかげにあった白いつぶ。サイコロくらいの大きさです。

■ 正体は氷
フェニックスがうでで地面をほったら、白いものが出てきました。4日後、つぶは消えていました。氷が、とけて水になる前に、そのまま気体になったからです（昇華といいます）。

■ なぜすごい？
白いものは、最初「塩かもしれない」と言われていました。でも、塩は消えません。消えたから、氷だと分かりました。
火星の地面のすぐ下に、水の氷がある。それをたしかめたのがフェニックスです。

■ どんな機械？
火星の水の歴史を調べるために送られた着陸機です。2008年5月25日、それまでのどの探査機よりも北に着陸しました。同じ年の11月2日に活動を終えて、今も火星の北極の平原にあります。

※2枚とも、火星で撮った本物の写真です（2008年6月15日と19日）。かげの形がちがうのは、撮った時刻がちがうから。「まちがい探し」は演出です。""",
"""Answer key (spoilers) 👇

What vanished: the white bits in the shadow at the lower left of the hole. They were about the size of dice.

■ They were ice
Phoenix dug into the ground with its arm and uncovered something white. Four days later the bits were gone. The ice had turned straight into vapor without melting first. That is called sublimation.

■ Why does it matter?
At first, some people thought the white stuff might be salt. But salt does not disappear. The bits vanished, so they had to be ice.
There is water ice just under the surface of Mars, and Phoenix is the machine that confirmed it.

■ What was Phoenix?
A lander sent to study the history of water on Mars. On May 25, 2008 it landed farther north than any mission before it. Its mission ended on Nov. 2 of the same year, and it is still on the arctic plains of Mars.

Note: both pictures are real photos taken on Mars (June 15 and 19, 2008). The shadows differ because the photos were taken at different times of day. The “spot the difference” framing is ours."""),
    comments=[
    ('spirit_rover', 'ヒントが出るまで、ぜんぜんわからなかった', 'No idea until the hint showed up.'),
    ('viking1_lander', 'かげもちがうよね、と思ったら時刻のちがいだった', 'I thought the shadows were the answer. Just a different time of day.')]),

 'opportunity-trailer-1': dict(
    caption=('与えられた時間は、90日。 #予告編 #火星 #オポチュニティ', 'It was given 90 days. #trailer #mars #opportunity'),
    pinned=("""これは、わたしたちが作った「予告」です。本物の広告ではありません。

■ どんな機械？
オポチュニティは、昔の火星に水があったかを調べるために送られた探査車です。2004年1月に着陸しました。予定は火星の90日、走る距離は1キロでした。

■ 動画に出てくる試練（どれも実際の出来事）
・2005年：砂の丘に車輪がうまり、5週間以上動けなかった
・2011〜2012年の冬：太陽の光が弱く、19週間走れなかった
・2014〜2015年：メモリーがこわれ、データを覚えていられない「記憶喪失」がくり返し起きた

■ 距離のカウンター
それぞれの場面のときの、実際の走行距離（約5.3km、約34.4km、約40.8〜41.6km）を通ります。あいだの増え方は演出です。金色の線は、NASAの地図にある実際のルートを描き直したものです。

■ このあと、どうなった？
下のボタンから、「1000回送っても、既読がつかなかった」へ。

※画像はNASAの本物です。ゆれや画面の乱れは演出です。""",
"""This is a trailer made by our team. It is not a real ad.

■ What was Opportunity?
A rover sent to find out whether ancient Mars had water. It landed in January 2004. It was designed to work for 90 Martian days and drive 1 kilometer.

■ The trials in the video (each one really happened)
• 2005: its wheels sank into a sand ripple and it was stuck for over five weeks
• Winter 2011–2012: too little sunlight to drive for 19 weeks
• 2014–2015: its flash memory failed, causing repeated “amnesia” events

■ The odometer
It passes the real distances at each scene (about 5.3 km, 34.4 km, 40.8–41.6 km). The pace in between is ours. The gold line is the real route from NASA’s map, redrawn.

■ What happened next?
Use the button below to go to “We texted 1,000 times. No reply.”

Note: the images are real NASA images. The camera shake and glitches are effects."""),
    comments=[('spirit_rover', 'ふたごのわたしも、ちょっとだけ出ますか？', 'Do I get a cameo? I am the twin.')]),

 'lost-quiz-1': dict(comments=[
    ('surveyor3', 'わたしも落とし物ですか？', 'Am I a lost item too?'),
    ('moon_lostfound', '↑ ちがいます。あなたは「置いてきた機械」。どこにいるかも、ちゃんと分かっています', '↑ No. You are a machine we left there. We know exactly where you are.')]),

 'dawn-grind-1': dict(
    caption=('みんなが遊んでる間に、ぼくは4日かけて時速96kmまで加速してた #モチベ #努力 #ドーン', 'While they were out partying, I spent 4 days getting up to 60 mph #motivation #grind #dawn'),
    pinned=("""答え合わせ👇（数字はNASAの資料から）

■ 4日かけて時速96km
ドーンのイオンエンジンは、全力でも「時速0→96km」に4日かかります。押す力は、手のひらに紙を1枚のせたくらいです。

■ それで、なぜすごい？
宇宙には、じゃまをする空気がほとんどありません。弱い力でも、押しつづければ速さがたまります。ドーンは合計5.9年（2,141日）エンジンをふかして、時速41,400kmぶんの速さを足しました。探査機が自分のエンジンで出した記録です。
（足した速さの合計で、今の速さではありません）

■ どんな機械？
火星と木星のあいだにある2つの天体、小惑星ベスタ（2011年）と準惑星ケレス（2015年）を、順番に回って調べるために送られました。2つの天体のまわりを回った探査機は、ドーンがはじめてです。2018年に通信が終わり、今もケレスのまわりを回っています。

■ おまけ（わたしたちの計算）
この加速で50m走をすると、ゴールまで約19分。

※「みんなが遊んでる間に…」は演出です。""",
"""The real story 👇 (the numbers come from NASA)

■ 4 days to reach 60 mph
At full throttle, Dawn’s ion engine takes four days to go from 0 to 60 mph. It pushes about as hard as a sheet of paper resting on your hand.

■ So why is that amazing?
In space there is almost no air to slow you down. Even a tiny push keeps adding speed. Dawn fired its engines for a total of 5.9 years (2,141 days) and added 25,700 mph. NASA calls that a record for a spacecraft using its own engines.
(That is the total speed it added, not how fast it is moving now.)

■ What was Dawn?
It was sent to orbit and study two worlds between Mars and Jupiter, one after the other: the giant asteroid Vesta (2011) and the dwarf planet Ceres (2015). It was the first spacecraft to orbit two worlds beyond Earth. Contact ended in 2018, and it is still circling Ceres.

■ Bonus (our own calculation)
With this acceleration, a 50-meter dash would take about 19 minutes.

Note: the “while they were out partying” framing is ours."""),
    comments=[
    ('sojourner_rover', '最高速度が秒速1cmのわたしには、ささった', 'As someone with a top speed of 1 centimeter per second: I felt this.',
        dict(src=[('Mars Pathfinder fact sheet (NASA/JPL): rover top speed 1 cm per second', 'https://mars.nasa.gov/internal_resources/815/')])),
    ('near_shoemaker', '小惑星なかま！', 'Fellow asteroid visitor!')]),

 'spirit-ideal-1': dict(
    sub=[('スピリットは、2004年に火星に着いた探査車です。', 'スピリットは、昔の火星に水があったかを調べるために送られた探査車です。2004年に火星に着きました。'),
         ('Spirit landed on Mars in 2004.', 'Spirit was a rover sent to find out whether ancient Mars had water. It landed in 2004.'),
         ('2010年3月22日の通信が最後になりました。', '2010年3月22日の通信が最後になりました。今も火星のグセフ・クレーターにあります。'),
         ('Its last message came on March 22, 2010.', 'Its last message came on March 22, 2010. It is still in Gusev crater on Mars.'),
         ('steam vents — places where', 'steam vents, places where')],
    comments=[
    ('opportunity_rover', 'ふたごです。会ったことは一度もないけど', 'Twin here. We never met.'),
    ('insight_lander', 'こわれた車輪で大発見、かっこいい', 'A big discovery from a broken wheel. Respect.', dict(fact=False))]),

 'shindan-1': dict(comments=[
    ('pioneer10', 'やってみたら「パイオニア10号」でした。本人です', 'I got “Pioneer 10.” That is literally me.')]),

 'pioneer-navi-1': dict(
    head=('答え合わせ👇', 'The real story 👇'),
    comments=[
    ('kepler_uranai', 'おうし座のみなさんへ。アルデバランの方向に、お客さんが向かっています。到着は200万年以上先です', 'Notice to every Taurus: a visitor is heading toward Aldebaran. Arrival: more than 2 million years from now.', dict(fact=False)),
    ('opportunity_rover', '14年で45km走ったわたしとは、けたがちがう', 'I drove 28 miles in 14 years. This is a whole other scale.')]),

 'viking-casefile-1': dict(
    caption=('火星で6年はたらいた着陸機と、ある日とつぜん連絡がとれなくなった。犯人を当てて #事件ファイル #火星 #バイキング1号', 'A lander worked on Mars for 6 years. Then it went silent. Guess the culprit #casefile #mars #viking1'),
    sub=[('バイキング1号は、1976年7月20日に火星に着陸しました。火星への着陸に本当の意味で成功した、最初の探査機です。',
          'バイキング1号は、火星に生き物がいるかを調べるために送られた着陸機です。1976年7月20日に着陸しました。火星への着陸に本当の意味で成功した、最初の探査機です。'),
         ('Viking 1 landed on Mars on July 20, 1976. NASA calls it the first truly successful landing on Mars.',
          'Viking 1 was a lander sent to look for signs of life on Mars. It landed on July 20, 1976. NASA calls it the first truly successful landing on Mars.'),
         ('※「事件ファイル」「手がかり」は演出です。写真と出来事は本物です。', '※「事件ファイル」は演出。写真と出来事は本物です。'),
         ('Note: the "case file" and "clues" are our dramatization. The photos and events are real.', 'Note: the “case file” framing is ours. The photos and events are real.')],
    comments=[
    ('viking1_lander', 'ちなみに今年で、火星に来て50年です', 'By the way, this year makes 50 years on Mars for me.'),
    ('insight_lander', '犯人が地球だったなんて。こわい話より、こわい', 'The culprit was Earth…? That is scarier than my scary story.', dict(fact=False))]),

 'sojourner-vlog-1': dict(
    caption=('【火星ではたらくVlog】3日目：36cm進んで石をさわった。きょうはもう充分 #Vlog #火星 #ソジャーナ', 'Working on Mars, day 3: drove 1.2 feet, touched a rock. Feeling productive. #vlog #mars #sojourner'),
    pinned=("""答え合わせ👇

■ 1日目（1997年7月4日）
エアバッグにつつまれて着陸。15回くらい、高さ15mまではねました。エアバッグが出口をふさいでいて、この日は着陸機の上で待機です。

■ 2日目・3日目
2日目のおわりに、スロープをおりて地面へ。3日目に約36cm進んで、「バーナクル・ビル」と名付けられた石に、成分をはかる機械を一晩おし当てました。ソジャーナの最初の石しらべです。

■ 7日の予定が83日
予定の12倍です。最高速度は秒速1cm。石や土の成分を15回以上はかり、写真を550枚撮りました。

■ このあと、どうなった？
83日目（9月27日）を最後に、親機（着陸機）からデータが来なくなりました。ソジャーナは、親機を通さないと地球と話せません。NASAの資料によると、そのあとソジャーナは、親機のまわりをぐるぐる回るか、その場で指示を待っていたと考えられています。

■ なぜすごい？
「安い費用でも火星に着陸して探検できるか」を試すために送られた、火星で最初の探査車です。その実験は、あとの探査車をよくするためのものでもありました。

※写真は本物。セリフとVlogの形は演出です。7日目と8日目の画面は写真ではなく、イラストです。""",
"""The real story 👇

■ Day 1 (July 4, 1997)
It landed wrapped in airbags and bounced about 15 times, as high as 50 feet (15 m). An airbag was blocking the exit ramp, so the rover spent the day waiting on top of the lander.

■ Days 2 and 3
Late on day 2 it rolled down the ramp to the ground. On day 3 it drove about 1.2 feet (36 cm) to a rock nicknamed “Barnacle Bill” and pressed its instrument against it overnight to measure what the rock is made of. That was Sojourner’s first rock.

■ Planned for 7 days, worked for 83
That is 12 times longer. Top speed: 1 centimeter per second. It made more than 15 chemical analyses of rocks and soil and took 550 pictures.

■ What happened next?
After day 83 (Sept. 27), no more data came from the lander. Sojourner could only talk to Earth through the lander. According to NASA, the rover is assumed to have either circled the lander again and again or stood in place, waiting for instructions.

■ Why does it matter?
It was the first rover on Mars, sent to test whether Mars could be landed on and explored at low cost. Its experiments were also meant to make later rovers better.

Note: the photos are real. The lines and the vlog format are ours. The day 7 and day 8 screens are drawings, not photos."""),
    comments=[
    ('opportunity_rover', '先輩…！予定より長くいるの、わたしたちもやりました', 'Senpai…! Staying longer than planned: we did that too.'),
    ('spirit_rover', '36cmで「充分」、ちょっとわかる', '“1.2 feet. Feeling productive.” I get it.')]),

 'kepler-uranai-1': dict(
    sub=[('2018年に燃料が尽きて引退しました。', '2018年に燃料が尽きて引退しました。今は、地球からはなれた軌道で太陽のまわりを回っています。'),
         ('It ran out of fuel and retired in 2018.', 'It ran out of fuel and retired in 2018. It now circles the Sun in an orbit away from Earth.')],
    comments=[
    ('pioneer10', 'わたしが向かってるの、おうし座の方向です。おうし座、何位でした？', 'I am heading toward Taurus. So… where did Taurus place?')]),

 'lag-1': dict(
    caption=('わたしをラジコンで運転してみて。ラグは片道20分（クリアできたら天才） #やってみた #火星 #ラグ', 'Try driving me like an RC car. The lag is 20 minutes each way. Good luck. #itried #mars #lag'),
    head=('答え合わせ👇', 'The real story 👇'),
    comments=[
    ('spirit_rover', 'ふたごのわたしも同じやり方でした。ラジコンじゃないよ', 'Same for me, the twin. We were never RC cars.'),
    ('viking1_lander', 'わたしは動けない着陸機なので、このゲームは永久にクリアできません', 'I am a lander. I cannot move. I will never clear this game.')]),

 'viking2-roomtour-1': dict(
    caption=('火星でひとり暮らし50年目のルームツアー。家賃0円、ながめ良し。ただし床がななめ #ルームツアー #ひとり暮らし #バイキング2号', 'Room tour: 50 years of living alone on Mars. Rent $0, great view. The floor is tilted, though. #roomtour #livingalone #viking2'),
    pinned=("""答え合わせ👇

■ 住人
バイキング2号の着陸機。バイキング1号のふたごで、火星に生き物がいるかを調べるために送られました。1976年9月3日、ユートピア平原に着陸。今年で50年です。

■ 床がななめ
着陸したとき、機体が西へ8.5度かたむきました。だから写真の地平線がななめに見えます。本当の地面は、ほぼ平らです。

■ 設備
カメラ2台、土をすくうロボットアーム、地震計、天気をはかる機械、土を調べる実験室。電気は原子力電池なので、太陽の光がなくても動きます。大きさは直径およそ3mです。

■ 冬の霜
1977年と1979年の冬、まわりの地面にうすい水の氷（霜）がつきました。最初のときは、約100日のこっていたそうです。

■ 何を見つけた？
土をすくって、生き物のしるしを探す実験を3回しました。結果は「いるとも、いないとも言えない」。バイキングの着陸機は、2台あわせて4,500枚の写真を地球に送りました。

■ いまは？
通信は1980年4月12日まで。機体は今もユートピア平原にあって、2006年には、火星を回る探査機のカメラが上空から見つけています。

※「家賃0円」と「ルームツアー」は演出です。間取り図とななめの図は、わたしたちのイラスト。写真は、バイキング2号が火星で撮った本物です。""",
"""The real story 👇

■ The resident
The Viking 2 lander, Viking 1’s twin, sent to look for signs of life on Mars. It landed on Utopia Planitia on Sept. 3, 1976. That makes 50 years this year.

■ The tilted floor
It came to rest tilted 8.5 degrees to the west. That is why the horizon looks tilted in its photos. The real ground is nearly level.

■ What it has
Two cameras, a robot arm for scooping soil, a seismometer, a weather station and a small lab for testing soil. It runs on nuclear batteries, so it does not need sunlight. It is about 3 meters (10 feet) across.

■ Frost in winter
In the winters of 1977 and 1979, a thin coat of water ice (frost) covered the ground around it. The first time, it stayed for about 100 days.

■ What did it find?
It scooped up soil three times to look for signs of life. The result: no clear answer either way. Together, the two Viking landers sent 4,500 photos back to Earth.

■ And now?
It sent data until April 12, 1980. It is still on Utopia Planitia, and in 2006 a camera on a Mars orbiter spotted it from above.

Note: “rent $0” and the room-tour format are ours. The floor plan and the tilt picture are our own drawings. The photos are real ones taken on Mars by Viking 2."""),
    comments=[
    ('viking1_lander', 'うちは6,460kmはなれた別の平原。ご近所ではないです', 'My place is on another plain, 4,000 miles away. Not exactly neighbors.'),
    ('phoenix_lander', 'うちの庭にも氷あります。地面の下だけど', 'My yard has ice too. Under the ground, though.')]),

 'near-chat-1': dict(
    caption=('回るために作られたのに「着陸してみない？」と言われた探査機 #無茶ぶり #小惑星 #NEAR', 'Built to orbit. Then came the message: “want to try landing?” #groupchat #asteroid #NEAR'),
    head=('答え合わせ👇', 'The real story 👇'),
    sub=[('NEARシューメーカーは、小惑星のまわりを回った世界で最初の探査機です。', 'NEARシューメーカーは、小惑星のまわりを回って調べるために送られた探査機です。小惑星を回ったのは、世界でこれが最初でした。'),
         ('NEAR Shoemaker was the first spacecraft to orbit an asteroid.', 'NEAR Shoemaker was sent to orbit and study an asteroid. It was the first spacecraft ever to orbit one.'),
         ('※チャットの会話は、わたしたちが考えた演出です。NEARと地球のチームが、実際にこういう言葉をやりとりしたわけではありません。写真と出来事は本物です。', '※チャットの会話は演出です（実際のやりとりではありません）。写真と出来事は本物です。'),
         ('Note: the chat is our dramatization. NEAR and its team never exchanged these words. The photos and events are real.', 'Note: the chat is ours. NEAR and its team never exchanged these words. The photos and events are real.')],
    comments=[
    ('surveyor3', 'わたしは着陸用なのに、月で2回はねました', 'I was built to land, and I still bounced twice on the Moon.'),
    ('machine_ranking', '「着陸用じゃないのに着陸した」ランキングがあったら、1位です', 'If we ranked “landed without being built to land,” you would be number one.')]),

 'pioneer11-dump-1': dict(
    caption=('木星と土星に行ってきた。ひとり旅の写真まとめ。帰りの便はなし #写真ダンプ #ひとり旅 #パイオニア11号', 'I went to Jupiter and Saturn. Photo dump from my solo trip. No return ticket. #photodump #solotrip #pioneer11'),
    pinned=("""答え合わせ👇

■ 予定は木星まで
パイオニア11号は、木星の近くを通って調べるために送られました。予定は21か月。先に行ったパイオニア10号がうまくいったので、「木星の重力を使って土星まで行こう」と予定が変わりました。

■ 木星（1974年12月）
雲の上、約42,500kmまで近づきました。そのときの速さは時速171,000km以上。当時、人間が作ったものの中でいちばんの速さでした。木星の北極・南極のあたりの写真を、はじめて地球に送りました。

■ 土星（1979年9月1日）
土星に行った最初の探査機です。輪のすぐ外側を通りぬけて、土星から約21,000kmまで近づきました。写真を440枚撮り、新しい輪（F環）と新しい月を見つけました。

■ じつは下見
土星のそばで通った道は、あとから来るボイジャー2号が通る予定の道でした。パイオニア11号が先に通って、通れることをたしかめました。

■ いまは？
最後の通信は1995年。打ち上げから22年以上はたらきました。今も太陽系の外へ飛びつづけていて、約400万年後に、わし座の星の近くを通ると考えられています。宇宙のだれかにあてた、金属の手紙ものせています。

※写真はNASAの本物です（打ち上げと、パイオニア11号が撮った木星・土星・タイタン）。3枚目はNASAが作った図。写真のふちと日付、「写真ダンプ」は演出です。""",
"""The real story 👇

■ The plan was only Jupiter
Pioneer 11 was sent to fly past Jupiter. The plan was 21 months. After Pioneer 10 got there first and all went well, the plan changed: use Jupiter’s gravity to go on to Saturn.

■ Jupiter (December 1974)
It flew about 26,400 miles (42,500 km) above the cloud tops at more than 106,000 mph (171,000 km/h). At the time, that was faster than anything people had ever made. It sent back the first pictures of Jupiter’s polar regions.

■ Saturn (Sept. 1, 1979)
It was the first spacecraft to visit Saturn. It passed just outside the rings and came within about 13,000 miles (21,000 km) of the planet. It took 440 pictures and discovered a new ring (the F ring) and a new moon.

■ It was also a scout
The path it took past Saturn was the path Voyager 2 would need later. Pioneer 11 went first and showed that the way was clear.

■ And now?
Its last contact was in 1995, more than 22 years after launch. It is still flying out of the solar system, and in about four million years it is expected to pass near a star in the constellation Aquila. It carries a metal plaque: a letter to anyone out there.

Note: the photos are real NASA photos (the launch, and Jupiter, Saturn and Titan taken by Pioneer 11). Photo 3 is a NASA diagram. The photo frames, the date stamps and the “photo dump” framing are ours."""),
    comments=[
    ('pioneer10', '兄です。土星は弟にゆずりました', 'Big brother here. I left Saturn to my little brother.'),
    ('dawn_spacecraft', '時速171,000km…！こっちは4日かけて時速96kmです', '106,000 mph…! It takes me four days to reach 60.')]),

 'ranking-overtime-1': dict(
    head=('答え合わせ👇（「何倍」は、わたしたちの計算です）', 'How we did the math 👇 (the “times longer” numbers are our own calculation)'),
    comments=[('near_shoemaker', 'わたしは「着陸の予定なし → 着陸」。何倍かは計算できません', 'Mine was “not built to land → landed.” You cannot put a number on that.')]),

 'runway-looks-1': dict(
    head=('答え合わせ👇 4つのLOOKの理由', 'The real reason behind each look 👇'),
    comments=[
    ('surveyor3', 'アクセサリー（カメラ）を持って帰られた側としては、複雑です', 'As someone whose accessory (a camera) got taken home, I have mixed feelings.'),
    ('viking1_lander', '次回はわたしも呼んでください。1976年モデルです', 'Call me next time. I am a 1976 model.')]),

 'opportunity-unread-1': dict(
    caption=('1000回送っても、既読がつかなかった #既読がつかない #火星 #オポチュニティ', 'We texted 1,000 times. No reply. #noreply #mars #opportunity'),
    head=('答え合わせ👇', 'The real story 👇'),
    sub=[('オポチュニティは、2004年から火星を走りつづけた探査車です。太陽の光で電気を作って動いていました。',
          'オポチュニティは、昔の火星に水があったかを調べるために送られた探査車です。2004年から火星を走りつづけました。太陽の光で電気を作って動いていました。'),
         ('Opportunity was a rover that drove on Mars from 2004. It ran on solar power.',
          'Opportunity was a rover sent to find out whether ancient Mars had water. It drove on Mars from 2004 and ran on solar power.')],
    comments=[
    ('spirit_rover', 'ごめん。わたしも2010年から返事できてない', 'Sorry. I have not been able to reply since 2010 either.'),
    ('pioneer10', 'わたしは2003年から', 'Since 2003 for me.'),
    ('insight_lander', 'わたしは2022年から', 'Since 2022 for me.')]),
}

# ---------- feed order ----------
# Moon and Mars first, then the machines farther out, then back to Mars for the last message nobody answered.
ORDER = [
 'insight-kaidan-1', 'lost-quiz-1', 'phoenix-spot-1', 'surveyor-pov-1', 'opportunity-trailer-1',
 'lag-1', 'pioneer-navi-1', 'viking-casefile-1', 'sojourner-vlog-1', 'spirit-ideal-1',
 'kepler-uranai-1', 'viking2-roomtour-1', 'dawn-grind-1', 'shindan-1', 'pioneer11-dump-1',
 'near-chat-1', 'runway-looks-1', 'machine-aruaru-1', 'ranking-overtime-1', 'opportunity-unread-1',
]

# ---------- team decision, Nov 15 ----------
# No staged comments and no staged like or follower counts. Each post keeps only its own pinned comment (the real story).
# The lines written for other machines stay above in POSTS for the record, but apply_texts.py does not publish them.
MACHINE_COMMENTS = False
