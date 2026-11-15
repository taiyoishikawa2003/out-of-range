"""'So relatable' list: four things the machines left on Mars always seem to do. Every item is true for at least two machines."""
from lib import *
DIR = 'aruaru'
BLUR = 'blur(16px) brightness(.45) saturate(1.1)'
CSS = '''
.ph img.c{object-fit:cover}
.duo{display:flex;gap:22px;align-items:flex-start;justify-content:center;width:880px}
.ot{padding:20px 34px}
.ot .row{font-size:42px;padding:16px 0}.ot .row span{font-size:38px;color:#161616;font-weight:900}
.ot .row b{color:#555;font-weight:700}.ot .row b em{font-style:normal;color:#e5202a;font-weight:900}
'''
def photo(nid, cap_ja, cap_en, w=840, rot=-1.5, hgt=None, pos='50% 50%'):
    st = f'height:{hgt}px;object-position:{pos}' if hgt else ''
    return f'<figure class="ph" style="width:{w}px;transform:rotate({rot}deg)"><img class="c" style="{st}" src="file://{ASSETS}/{nid}.jpg"><figcaption>{t(cap_ja, cap_en)}</figcaption></figure>'
def no(n): return tag(f'あるある{"①②③④"[n - 1]}', f'No. {n}', 'white sm')
SLIDES = [
 dict(dur=4.5, alt={'ja': 'あるある：火星に置いてきた機械あるある。4つ、ぜんぶ本物の写真つき', 'en': 'So relatable: things that machines left on Mars always do. Four of them, with real photos'},
  html=lambda: bg('PIA00766', '50% 50%', 1.05, 'brightness(.6)') + shade('top') + col(
    tag('あるある', 'So relatable', 'pink sm'),
    h('火星に<br>置いてきた機械<br><em>あるある</em>', 'Things that machines<br>left on Mars<br><em>always do</em>'),
    bx('4つ。ぜんぶ本物の写真つき', '4 of them, with real photos', 'sm yellow'))
   + cr('本物の写真：探査車ソジャーナと、岩「ヨギ」。1997年、火星（NASA/JPL）', 'Real photo: the rover Sojourner and a rock called “Yogi.” Mars, 1997 (NASA/JPL)')),
 dict(dur=6, alt={'ja': 'あるある1：着陸で、はねがち。パスファインダーは約15回、スピリットは28回、オポチュニティは26回以上。オポチュニティは、はねて転がってクレーターの中で止まった。上空からの写真に、いまも着陸台が白い点で見える', 'en': 'Number 1: they bounce when they land. Pathfinder about 15 times, Spirit 28 times, Opportunity at least 26. Opportunity bounced and rolled into a crater. A photo from orbit still shows its landing platform as a white dot'},
  html=lambda: bg('PIA21494', '50% 50%', 1.1, BLUR) + col(
    no(1),
    h('着陸で<br><em>はね</em>がち', 'They <em>bounce</em><br>when they land', 'md'),
    f"""<div class="card ot">
      <div class="row"><span>{t("パスファインダー", "Pathfinder")}</span><b>{t("<em>約15回</em>", "about <em>15 times</em>")}</b></div>
      <div class="row"><span>{t("スピリット", "Spirit")}</span><b>{t("<em>28回</em>", "<em>28 times</em>")}</b></div>
      <div class="row"><span>{t("オポチュニティ", "Opportunity")}</span><b>{t("<em>26回以上</em>", "<em>26+ times</em>")}</b></div></div>""",
    photo('PIA21494_eagle', 'オポチュニティは、はねて転がってクレーターの中へ。白い点が、いまも残る着陸台。2017年に上空から（NASA/JPL-Caltech/Univ. of Arizona）', 'Opportunity bounced and rolled into a crater. The white dot is its landing platform, still there. Seen from orbit in 2017 (NASA/JPL-Caltech/Univ. of Arizona)', 620, -1.5, 400, '50% 50%'), style='top:300px;gap:26px')),
 dict(dur=5.5, alt={'ja': 'あるある2：着いたら、まず自分の足を撮りがち。バイキング1号と2号の、火星での最初の写真。どちらも右下に足がうつっている', 'en': 'Number 2: their first photo after landing shows their own foot. The first pictures from Viking 1 and Viking 2 on Mars both show a footpad at lower right'},
  html=lambda: bg('PIA00381', '80% 50%', 1.1, BLUR) + col(
    no(2),
    h('着いたら、まず<br><em>自分の足</em>を撮りがち', 'First photo after landing:<br><em>their own foot</em>', 'md'),
    photo('PIA00381', 'バイキング1号の1枚目。右下が足。1976年7月20日（NASA/JPL）', 'Viking 1’s first picture. Its foot is at lower right. July 20, 1976 (NASA/JPL)', 840, -1.5, 330, '100% 50%'),
    photo('PIA00396', 'バイキング2号の1枚目。右下が足。1976年9月3日（NASA/JPL）', 'Viking 2’s first picture. Its foot is at lower right. Sept. 3, 1976 (NASA/JPL)', 840, 1.5, 330, '100% 50%'), style='top:300px;gap:24px')),
 dict(dur=5.5, alt={'ja': 'あるある3：見つけた石や穴に、あだ名つけがち。火星の岩「ヨギ」と、穴「ドードー・ゴルディロックス」', 'en': 'Number 3: every rock and hole they find gets a nickname. The Mars rock called Yogi and the trench called Dodo-Goldilocks'},
  html=lambda: bg('PIA00766', '50% 50%', 1.1, BLUR) + col(
    no(3),
    h('見つけた石や穴に<br><em>あだ名</em>つけがち', 'Every rock and hole<br>gets a <em>nickname</em>', 'md'),
    '<div class="duo">' + photo('PIA00766', '岩「ヨギ」。1997年', 'A rock called “Yogi.” 1997', 430, -2, 420, '62% 60%')
      + photo('PIA10910', '穴「ドードー・ゴルディロックス」。2008年', 'A trench called “Dodo-Goldilocks.” 2008', 430, 2, 420, '50% 45%') + '</div>',
    bx('名前をつけるのは、地球のチーム', 'The teams on Earth pick the names', 'sm'),
    f'<div class="cr" style="position:static;max-width:860px">{t("本物の写真：左 NASA/JPL、右 NASA/JPL-Caltech/University of Arizona/Texas A&M University", "Real photos: left NASA/JPL, right NASA/JPL-Caltech/University of Arizona/Texas A&M University")}</div>', style='top:300px;gap:26px')),
 dict(dur=6, alt={'ja': 'あるある4：名前は、子どもがつけがち。ソジャーナは12さい、スピリットとオポチュニティは9さい、インジェニュイティは高校生が考えた名前', 'en': 'Number 4: kids pick their names. Sojourner was named by a 12-year-old, Spirit and Opportunity by a 9-year-old, Ingenuity by a high school student'},
  html=lambda: bg('PIA04422', '35% 50%', 1.1, BLUR) + col(
    no(4),
    h('<em>名前</em>は、子どもが<br>つけがち', 'Their <em>names</em><br>come from kids', 'md'),
    f"""<div class="card ot">
      <div class="row"><span>{t("ソジャーナ", "Sojourner")}</span><b>{t("<em>12さい</em>", "<em>age 12</em>")}</b></div>
      <div class="row"><span>{t("スピリットとオポチュニティ", "Spirit and Opportunity")}</span><b>{t("<em>9さい</em>", "<em>age 9</em>")}</b></div>
      <div class="row"><span>{t("インジェニュイティ", "Ingenuity")}</span><b>{t("<em>高校生</em>", "<em>high schooler</em>")}</b></div></div>""",
    bx('作文コンテストで選ばれた名前', 'Each name won an essay contest', 'sm'),
    photo('PIA04422', '本物の写真：打ち上げ前の火星探査車と、先輩ソジャーナの予備機（NASA/JPL）', 'Real photo: a Mars rover before launch, with a spare of the earlier Sojourner (NASA/JPL)', 700, -1.5, 300, '35% 60%'), style='top:300px;gap:24px')),
 dict(dur=6, alt={'ja': 'そして全員、いまもそこにいる', 'en': 'And every one of them is still out there'},
  html=lambda: bg('PIA22928', '50% 50%', 1.0, 'brightness(.5)') + shade('all') + col(
    h('そして全員', 'And every one of them', 'md'),
    h('<em>いまも<br>そこにいる</em>', 'is <em>still<br>out there</em>', 'xl'), cls='mid', style='gap:34px')
   + cr('本物の写真：オポチュニティがふり返って撮った自分の車輪のあと（NASA/JPL-Caltech）', 'Real photo: Opportunity looking back at its own tracks (NASA/JPL-Caltech)')),
]
CRP = 'NASA/JPL-Caltech/University of Arizona/Texas A&M University'
POST = dict(id='machine-aruaru-1', account='machine_aruaru', place='mars', audio='media/music/carefree.mp3',
 caption={'ja': '火星に置いてきた機械あるある。着いたら、まず自分の足を撮りがち #あるある #火星 #探査機',
          'en': 'Things machines left on Mars always do. First photo after landing: their own foot. #relatable #mars #spacecraft'},
 tags=['aruaru', 'mars', 'viking', 'rover'],
 sound={'ja': 'Kevin MacLeod「Carefree」(CC BY 4.0)', 'en': 'Kevin MacLeod – Carefree (CC BY 4.0)'},
 comments=pinned('machine_aruaru',
"""答え合わせ👇

■ ① 着陸で、はねがち
マーズ・パスファインダー（1997年）と、スピリット、オポチュニティ（2004年）は、エアバッグにつつまれて火星に落ち、はずんでから止まりました。パスファインダーは15回くらい、スピリットは28回、オポチュニティは26回以上です。オポチュニティは、はねて転がって、小さなクレーターの中で止まりました。

■ ② 自分の足を撮りがち
バイキング1号（1976年7月20日）とバイキング2号（同じ年の9月3日）。どちらも、着陸して数分後に撮った最初の1枚に、自分の足がうつっています。バイキング1号のこの写真は、火星の地面で撮られた世界で最初の写真です。

■ ③ あだ名つけがち
パスファインダーのチームは、岩に「ヨギ」「スクービー・ドゥー」など、アニメのキャラクターの名前をつけました。2008年にフェニックスがほった穴は「ドードー・ゴルディロックス」「スノーホワイト（白雪姫）」です。

■ ④ 名前は、子どもがつけがち
NASAの火星の探査車の名前は、どれも学生が考えました。ソジャーナは12さい、スピリットとオポチュニティは9さい（小学3年生）の作文から。ヘリコプターのインジェニュイティは、高校生が考えた名前です。

■ いまは？
ここに出てきた機械は、ぜんぶ今も火星にあります。

※「あるある」は演出。写真はぜんぶNASAの本物です。""",
"""The real story 👇

■ No. 1: bouncing on arrival
Mars Pathfinder (1997), Spirit and Opportunity (2004) fell to Mars wrapped in airbags and bounced before they stopped. Pathfinder bounced about 15 times, Spirit 28 times, Opportunity at least 26. Opportunity bounced and rolled right into a small crater.

■ No. 2: a photo of their own foot
Viking 1 (July 20, 1976) and Viking 2 (Sept. 3 of the same year). For both, the very first picture, taken minutes after landing, shows one of the lander’s own feet. Viking 1’s picture is the first photograph ever taken on the surface of Mars.

■ No. 3: nicknames
The Pathfinder team nicknamed rocks after cartoon characters, such as “Yogi” and “Scooby Doo.” In 2008, the trenches Phoenix dug were called “Dodo-Goldilocks” and “Snow White.”

■ No. 4: named by kids
Every NASA rover on Mars got its name from a student. Sojourner’s came from a 12-year-old’s essay. Spirit and Opportunity were named by a 9-year-old third grader. The helicopter Ingenuity was named by a high school student.

■ And now?
Every machine in this post is still on Mars.

Note: the “so relatable” list format is ours. Every photo is a real NASA photo.""") + [
  {'user': 'viking1_lander', 'text': {'ja': '②はわたしです。火星で最初の1枚なのに、足', 'en': 'No. 2 is me. The first photo ever taken on Mars, and it is my foot.'}},
  {'user': 'sojourner_rover', 'text': {'ja': '④、わたしの名前をくれたのは12さいの子でした', 'en': 'No. 4: the kid who gave me my name was 12.'}}],
 sources=[
  fact('Mars Pathfinder fact sheet (NASA/JPL): the lander bounced about 15 times on its airbags', 'https://mars.nasa.gov/internal_resources/815/'),
  fact('Spirit (NASA Science): bounced 28 times before rolling to a stop', 'https://science.nasa.gov/mission/mer-spirit/'),
  fact('Opportunity (NASA Science): bounced at least 26 times before coming to rest', 'https://science.nasa.gov/mission/mer-opportunity/'),
  pj('PIA21494', 'Rover Landing Hardware at Eagle Crater, Mars (seen from orbit, April 8, 2017; the lander bounced and rolled right into the crater). We cropped the image.', 'NASA/JPL-Caltech/Univ. of Arizona'),
  pj('PIA00381', 'First Photograph Taken On Mars Surface (Viking 1, July 20, 1976; footpad at right)', 'NASA/JPL'),
  pj('PIA00396', 'Viking Lander 2 First Picture On The Surface Of Mars (Sept. 3, 1976; footpad)', 'NASA/JPL'),
  fact('NASA History: Mars Pathfinder controllers nicknamed rocks after cartoon characters, such as Barnacle Bill, Yogi and Scooby Doo', 'https://www.nasa.gov/history/25-years-ago-mars-pathfinder-launches-to-mars-to-deploy-sojourner-the-first-planetary-rover/'),
  fact('NASA/JPL news, June 19, 2008: trenches informally called "Dodo-Goldilocks" and "Snow White"', 'https://www.jpl.nasa.gov/news/bright-chunks-at-phoenix-landers-mars-site-must-have-been-ice/'),
  pj('PIA00766', 'Sojourner & Yogi', 'NASA/JPL'), pj('PIA10910', 'Ice on Mars - Now You See It (Dodo-Goldilocks trench)', CRP),
  fact('NASA: Naming a NASA Mars Rover Can Change Your Life ("Every rover on Mars has been named by a student")', 'https://www.nasa.gov/solar-system/naming-a-nasa-mars-rover-can-change-your-life/'),
  fact('NASA/JPL Education: Sojourner was named by a 12-year-old student; a third-grade student named Spirit and Opportunity', 'https://www.jpl.nasa.gov/edu/news/2019/8/28/students-invited-to-name-nasas-next-mars-rover'),
  fact('NASA/JPL news, June 8, 2003: a 9-year-old wrote the winning essay that named Spirit and Opportunity', 'https://www.jpl.nasa.gov/news/girl-with-dreams-names-mars-rovers-spirit-and-opportunity/'),
  fact('NASA news release, April 29, 2020: a high school student named the Mars helicopter Ingenuity in the "Name the Rover" essay contest', 'https://www.nasa.gov/news-release/alabama-high-school-student-names-nasas-mars-helicopter/'),
  pj('PIA04422', 'Rovers and Sojourner', 'NASA/JPL'), pj('PIA22928', 'Looking Back on a Golden Opportunity', 'NASA/JPL-Caltech'),
  music('Carefree')])
