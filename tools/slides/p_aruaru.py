"""'So relatable' list: four things that machines left on other worlds always seem to do. Every item is true for at least two machines."""
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
  html=lambda: bg('PIA22876', '50% 50%', 1.05, 'brightness(.6)') + shade('top') + col(
    tag('あるある', 'So relatable', 'pink sm'),
    h('火星に<br>置いてきた機械<br><em>あるある</em>', 'Things that machines<br>left on Mars<br><em>always do</em>'),
    bx('4つ。ぜんぶ本物の写真つき', '4 of them, with real photos', 'sm yellow'))
   + cr('本物の写真：インサイトの最初の自撮り。2018年、火星（NASA/JPL-Caltech）', 'Real photo: InSight’s first selfie. Mars, 2018 (NASA/JPL-Caltech)')),
 dict(dur=5.5, alt={'ja': 'あるある1：着いたら、まず自分の足を撮りがち。バイキング1号と2号の、火星での最初の写真。どちらも右下に足がうつっている', 'en': 'Number 1: their first photo after landing shows their own foot. The first pictures from Viking 1 and Viking 2 on Mars both show a footpad at lower right'},
  html=lambda: bg('PIA00381', '80% 50%', 1.1, BLUR) + col(
    no(1),
    h('着いたら、まず<br><em>自分の足</em>を撮りがち', 'First photo after landing:<br><em>their own foot</em>', 'md'),
    photo('PIA00381', 'バイキング1号の1枚目。右下が足。1976年7月20日（NASA/JPL）', 'Viking 1’s first picture. Its foot is at lower right. July 20, 1976 (NASA/JPL)', 840, -1.5, 330, '100% 50%'),
    photo('PIA00396', 'バイキング2号の1枚目。右下が足。1976年9月3日（NASA/JPL）', 'Viking 2’s first picture. Its foot is at lower right. Sept. 3, 1976 (NASA/JPL)', 840, 1.5, 330, '100% 50%'), style='top:300px;gap:24px')),
 dict(dur=5.5, alt={'ja': 'あるある2：見つけた石や穴に、あだ名つけがち。火星の岩「ヨギ」と、穴「ドードー・ゴルディロックス」', 'en': 'Number 2: every rock and hole they find gets a nickname. The Mars rock called Yogi and the trench called Dodo-Goldilocks'},
  html=lambda: bg('PIA00766', '50% 50%', 1.1, BLUR) + col(
    no(2),
    h('見つけた石や穴に<br><em>あだ名</em>つけがち', 'Every rock and hole<br>gets a <em>nickname</em>', 'md'),
    '<div class="duo">' + photo('PIA00766', '岩「ヨギ」。1997年', 'A rock called “Yogi.” 1997', 430, -2, 420, '62% 60%')
      + photo('PIA10910', '穴「ドードー・ゴルディロックス」。2008年', 'A trench called “Dodo-Goldilocks.” 2008', 430, 2, 420, '50% 45%') + '</div>',
    bx('名前をつけるのは、地球のチーム', 'The teams on Earth pick the names', 'sm'),
    f'<div class="cr" style="position:static;max-width:860px">{t("本物の写真：左 NASA/JPL、右 NASA/JPL-Caltech/University of Arizona/Texas A&M University", "Real photos: left NASA/JPL, right NASA/JPL-Caltech/University of Arizona/Texas A&M University")}</div>', style='top:300px;gap:26px')),
 dict(dur=5.5, alt={'ja': 'あるある3：自撮りしがち。そして砂まみれになりがち。インサイトの2018年の自撮りと、2022年の最後の自撮り', 'en': 'Number 3: they take selfies, and then they get covered in dust. InSight’s selfie from 2018 and its last selfie from 2022'},
  html=lambda: bg('PIA25287', '50% 50%', 1.1, BLUR) + col(
    no(3),
    h('<em>自撮り</em>しがち。<br>で、砂まみれになりがち', 'They take <em>selfies.</em><br>Then they get dusty.', 'md'),
    photo('PIA22876', 'インサイト、2018年12月。着いたばかり（NASA/JPL-Caltech）', 'InSight, December 2018. Just arrived (NASA/JPL-Caltech)', 700, -1.5, 380, '50% 55%'),
    photo('PIA25287', 'インサイト、2022年4月。最後の自撮り（NASA/JPL-Caltech）', 'InSight, April 2022. Its last selfie (NASA/JPL-Caltech)', 700, 1.5, 380, '50% 55%'), style='top:300px;gap:22px')),
 dict(dur=6, alt={'ja': 'あるある4：「ちょっとだけ」の予定が何倍にもなりがち。ソジャーナは7日の予定が83日。オポチュニティは90日の予定が14年以上。インジェニュイティは5回の予定が72回', 'en': 'Number 4: a short job turns into a much longer one. Sojourner: 7 days planned, 83 worked. Opportunity: 90 days planned, over 14 years. Ingenuity: 5 flights planned, 72 flown'},
  html=lambda: bg('PIA04422', '35% 50%', 1.1, BLUR) + col(
    no(4),
    h('「ちょっとだけ」の予定が<br><em>何倍</em>にもなりがち', '“Just a short job”<br>turns into <em>much more</em>', 'md'),
    f'''<div class="card ot">
      <div class="row"><span>{t("ソジャーナ", "Sojourner")}</span><b>{t("7日 → <em>83日</em>", "7 days → <em>83 days</em>")}</b></div>
      <div class="row"><span>{t("オポチュニティ", "Opportunity")}</span><b>{t("90日 → <em>14年以上</em>", "90 days → <em>14+ years</em>")}</b></div>
      <div class="row"><span>{t("インジェニュイティ", "Ingenuity")}</span><b>{t("5回 → <em>72回</em>", "5 flights → <em>72</em>")}</b></div></div>''',
    photo('PIA04422', '本物の写真：打ち上げ前の火星探査車と、先輩ソジャーナの予備機（NASA/JPL）', 'Real photo: Mars rovers before launch, with a spare of the earlier Sojourner (NASA/JPL)', 700, -1.5, 330, '35% 60%'), style='top:300px;gap:26px')),
 dict(dur=6, alt={'ja': 'そして全員、いまもそこにいる。ほかのあるあるを、コメントで教えて', 'en': 'And every one of them is still out there. Know another one? Tell us in the comments'},
  html=lambda: bg('PIA22928', '50% 50%', 1.0, 'brightness(.5)') + shade('all') + col(
    h('そして全員', 'And every one of them', 'md'),
    h('<em>いまも<br>そこにいる</em>', 'is <em>still<br>out there</em>', 'xl'),
    bx('ほかの「あるある」、コメントで教えて 👇', 'Know another one? Tell us in the comments 👇', 'sm yellow'), cls='mid', style='gap:34px')
   + cr('本物の写真：オポチュニティがふり返って撮った自分の車輪のあと（NASA/JPL-Caltech）', 'Real photo: Opportunity looking back at its own tracks (NASA/JPL-Caltech)')),
]
CRP = 'NASA/JPL-Caltech/University of Arizona/Texas A&M University'
POST = dict(id='machine-aruaru-1', account='machine_aruaru', place='mars', audio='media/music/carefree.mp3',
 caption={'ja': '火星に置いてきた機械あるある。①着いたら、まず自分の足を撮りがち（ぜんぶ本物の写真） #あるある #火星 #探査機',
          'en': 'Things machines left on Mars always do. No. 1: the first photo is their own foot. (All real photos) #relatable #mars #spacecraft'},
 tags=['aruaru', 'mars', 'viking', 'insight'],
 sound={'ja': 'Kevin MacLeod「Carefree」(CC BY 4.0)', 'en': 'Kevin MacLeod – Carefree (CC BY 4.0)'},
 comments=pinned('machine_aruaru',
"""あるあるの元ネタ（ぜんぶ本当）👇

■ ① 自分の足を撮りがち
バイキング1号（1976年7月20日）とバイキング2号（同じ年の9月3日）。どちらも、火星に着いて数分後に撮った最初の1枚に、自分の足がうつっています。バイキング1号のこの写真は、火星の地面で撮られた世界で最初の写真です。

■ ② あだ名つけがち
1997年のマーズ・パスファインダーでは、岩に「ヨギ」「スクービー・ドゥー」など、アニメのキャラクターの名前がつきました。2008年のフェニックスがほった穴は「ドードー・ゴルディロックス」「スノーホワイト（白雪姫）」。名前をつけたのは地球のチームです。

■ ③ 自撮りして、砂まみれ
インサイトは2018年12月に最初の自撮り、2022年4月に最後の自撮りを撮りました。くらべると、太陽電池が砂だらけ。砂のせいで電気が作れなくなっていきました。自撮りは、うでについたカメラで何枚も撮って、つなぎ合わせたものです。

■ ④ 予定の何倍もはたらきがち
ソジャーナは7日の予定で83日。オポチュニティは火星の90日の予定で14年以上。インジェニュイティは5回の予定で72回飛びました。

■ いまもそこにいる
ここに出てきた機械は、ぜんぶ今も火星にあります。

※「あるある」は演出です。写真はぜんぶNASAの本物です。""",
"""Where each one comes from (all true) 👇

■ No. 1: a photo of their own foot
Viking 1 (July 20, 1976) and Viking 2 (Sept. 3 of the same year). For both, the very first picture, taken minutes after landing on Mars, shows one of the lander’s own feet. Viking 1’s picture is the first photograph ever taken on the surface of Mars.

■ No. 2: nicknames
In 1997, the Mars Pathfinder team nicknamed rocks after cartoon characters, such as “Yogi” and “Scooby Doo.” In 2008, the trenches Phoenix dug were called “Dodo-Goldilocks” and “Snow White.” The teams on Earth pick the names.

■ No. 3: selfies, then dust
InSight took its first selfie in December 2018 and its last in April 2022. Compare them: the solar panels are covered in dust. The dust slowly cut off its power. A selfie is many pictures taken by the camera on its arm and stitched together.

■ No. 4: much longer than planned
Sojourner: planned for 7 days, worked for 83. Opportunity: planned for 90 Martian days, worked for over 14 years. Ingenuity: planned for 5 flights, flew 72.

■ Still out there
Every machine in this post is still on Mars.

Note: the “so relatable” list format is ours. Every photo is a real NASA photo.""") + [
  {'user': 'viking1_lander', 'text': {'ja': '①はわたしです。火星で最初の1枚なのに、足', 'en': 'No. 1 is me. The first photo ever taken on Mars, and it is my foot.'}},
  {'user': 'insight_lander', 'text': {'ja': '③はわたし。最後の自撮りのあと、うでは「引退のポーズ」にしました', 'en': 'No. 3 is me. After my last selfie, my arm went into its “retirement pose.”'}}],
 sources=[pj('PIA00381', 'First Photograph Taken On Mars Surface (Viking 1, July 20, 1976; footpad at right)', 'NASA/JPL'),
  pj('PIA00396', 'Viking Lander 2 First Picture On The Surface Of Mars (Sept. 3, 1976; footpad)', 'NASA/JPL'),
  fact('NASA History: Mars Pathfinder controllers nicknamed rocks after cartoon characters, such as Barnacle Bill, Yogi and Scooby Doo; Sojourner worked 83 days', 'https://www.nasa.gov/history/25-years-ago-mars-pathfinder-launches-to-mars-to-deploy-sojourner-the-first-planetary-rover/'),
  fact('NASA/JPL news, June 19, 2008: trenches informally called "Dodo-Goldilocks" and "Snow White"', 'https://www.jpl.nasa.gov/news/bright-chunks-at-phoenix-landers-mars-site-must-have-been-ice/'),
  pj('PIA00766', 'Sojourner & Yogi', 'NASA/JPL'), pj('PIA10910', 'Ice on Mars - Now You See It (Dodo-Goldilocks trench)', CRP),
  pj('PIA22876', "InSight's First Selfie (Dec. 6, 2018; a mosaic of 11 images from the camera on its arm)", 'NASA/JPL-Caltech'),
  pj('PIA25287', "InSight's Final Selfie (April 24, 2022; far more dust; dusty solar panels producing less power; retirement pose)", 'NASA/JPL-Caltech'),
  fact('InSight (NASA Science)', 'https://science.nasa.gov/mission/insight/'),
  fact('NASA: Opportunity Rover Mission on Mars Comes to End (designed for 90 Martian days)', 'https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end/'),
  fact('Ingenuity (NASA Science): no more than five test flights planned; 72 flights completed', 'https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/'),
  pj('PIA04422', 'Rovers and Sojourner', 'NASA/JPL'), pj('PIA22928', 'Looking Back on a Golden Opportunity', 'NASA/JPL-Caltech'),
  music('Carefree')])
