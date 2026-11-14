#!/usr/bin/env python3
"""Build the "What did people leave most on the Moon?" quiz (3 slides, ja/en) + BGM.
Usage: python3 tools/build_lost_quiz.py <img_dir> <audio_dir> <out_dir>
  img_dir needs as14-66-09277.jpg; audio_dir needs "Monkeys Spinning Monkeys.mp3" (Kevin MacLeod, incompetech.com, CC BY 4.0).
Counts (from sources in data/posts.json): bags of waste 96, cameras 12, pairs of boots 12, golf balls 2.
"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
IMG, AUD, OUT = sys.argv[1:4]; W, H = 1080, 1920
def F(sz, w='Black'): return ImageFont.truetype(f'/usr/share/fonts/opentype/noto/NotoSansCJK-{w}.ttc', sz, index=0)
def cover(im, cx=.5, cy=.5, z=1.0):
    iw, ih = im.size; tw = min(iw, ih * W / H) / z; th = tw * H / W
    if th > ih: th = ih; tw = th * W / H
    x0 = min(max(cx * iw - tw / 2, 0), iw - tw); y0 = min(max(cy * ih - th / 2, 0), ih - th)
    return im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))
COL = [(255, 64, 129), (60, 140, 255), (255, 150, 0), (40, 190, 90)]
T = {
 'ja': dict(tag='みんなの質問への返信', q=['月に人間が残した物で', 'いちばん数が多いのって', 'なに？'],
            ch=['カメラ', 'ブーツ', 'ゴルフボール', 'うんち'], ans='答え：D うんち（袋96個）',
            rows=[('うんち（袋）', '96個', 3), ('カメラ', '12台', 0), ('ブーツ', '12足', 1), ('ゴルフボール', '2個', 2)],
            why_q=['なんで置いてきたの？'], why=['帰りに月の石をたくさん', '持ち帰るため、', '重さを減らしたから'],
            sci_q=['今も残ってるなら', 'どうなってるの？'], sci=['科学者は「取りに行きたい」', '50年たった菌が生きていたら', '生き物は宇宙の旅にも', '耐えられるかもしれない'],
            note='写真：アポロ14号の着陸船（NASA）',
            s3=[('なんで置いてきたの？', 46, (255, 255, 255), (20, 20, 20), 0), ('月の石をたくさん持ち帰るため', 42, (0, 0, 0), (255, 255, 255), 0), ('重さを減らした', 42, (0, 0, 0), (255, 255, 255), 70),
                ('でも科学者は', 50, (255, 255, 255), (20, 20, 20), 0), ('取りに行きたい！', 76, (255, 206, 0), (20, 20, 20), 70),
                ('50年たった菌が', 46, (0, 0, 0), (255, 255, 255), 0), ('まだ生きていたら…', 46, (0, 0, 0), (255, 255, 255), 0),
                ('生き物は宇宙の旅にも', 48, (40, 190, 90), (255, 255, 255), 0), ('耐えられるかも', 48, (40, 190, 90), (255, 255, 255), 0)]),
 'en': dict(tag='Replying to your question', q=['What did people leave', 'on the Moon the most', 'of?'],
            ch=['Cameras', 'Boots', 'Golf balls', 'Poop'], ans='Answer: D, poop (96 bags)',
            rows=[('Poop (bags)', '96', 3), ('Cameras', '12', 0), ('Boots (pairs)', '12', 1), ('Golf balls', '2', 2)],
            why_q=['Why leave it there?'], why=['To bring lots of', 'Moon rocks home,', 'they had to cut weight'],
            sci_q=['So what is it', 'doing now?'], sci=['Scientists want it back.', 'If microbes survived 50 years,', 'life might survive', 'trips through space'],
            note='Photo: Apollo 14 lunar module (NASA)',
            s3=[('Why leave it there?', 46, (255, 255, 255), (20, 20, 20), 0), ('To bring lots of Moon rocks home', 40, (0, 0, 0), (255, 255, 255), 0), ('they had to cut weight', 40, (0, 0, 0), (255, 255, 255), 70),
                ('But scientists', 50, (255, 255, 255), (20, 20, 20), 0), ('want it back!', 76, (255, 206, 0), (20, 20, 20), 70),
                ('If microbes are still alive', 44, (0, 0, 0), (255, 255, 255), 0), ('after 50 years...', 44, (0, 0, 0), (255, 255, 255), 0),
                ('life might survive', 48, (40, 190, 90), (255, 255, 255), 0), ('trips through space', 48, (40, 190, 90), (255, 255, 255), 0)]),
}
def sticker(d, top, tag, lines, size=44, color=(20, 20, 20)):
    h = 110 + len(lines) * int(size * 1.45)
    d.rounded_rectangle((90, top, 870, top + h), 30, fill=(255, 255, 255))
    d.ellipse((120, top + 28, 180, top + 88), fill=(255, 196, 0)); d.text((200, top + 58), tag, font=F(30, 'Bold'), fill=(120, 120, 120), anchor='lm')
    for i, l in enumerate(lines): d.text((125, top + 120 + i * int(size * 1.45)), l, font=F(size, 'Bold'), fill=color, anchor='lm')
    return top + h
def main():
    os.makedirs(OUT, exist_ok=True)
    lm = Image.open(f'{IMG}/as14-66-09277.jpg').convert('RGB')
    bg1, bg2 = cover(lm, .5, .5, 1.1), cover(lm, .3, .78, 2.0)
    for lang, t in T.items():
        # 1 question
        im = bg1.copy(); d = ImageDraw.Draw(im); sticker(d, 300, t['tag'], t['q'], 48)
        for i, (c, v) in enumerate(zip(COL, t['ch'])):
            y = 960 + i * 128; d.rounded_rectangle((160, y, 870, y + 104), 30, fill=c)
            d.text((210, y + 52), 'ABCD'[i], font=F(56), fill=(255, 255, 255), anchor='lm'); d.text((300, y + 52), v, font=F(54), fill=(255, 255, 255), anchor='lm')
        d.text((40, 1520), t['note'], font=F(26, 'Bold'), fill=(235, 235, 235), stroke_width=3, stroke_fill=(0, 0, 0))
        im.save(f'{OUT}/quiz1.{lang}.jpg', quality=85)
        # 2 answer + ranking
        im = bg1.copy(); d = ImageDraw.Draw(im); b = sticker(d, 300, t['tag'], [t['ans']], 48, (40, 160, 80))
        d.rounded_rectangle((90, b + 30, 870, b + 640), 30, fill=(255, 255, 255))
        for i, (name, n, ci) in enumerate(t['rows']):
            y = b + 70 + i * 140; w = max(70, int(560 * int(''.join(ch for ch in n if ch.isdigit())) / 96))
            d.text((130, y + 30), name, font=F(38, 'Bold'), fill=(20, 20, 20), anchor='lm')
            d.rounded_rectangle((130, y + 64, 130 + w, y + 110), 22, fill=COL[ci] if i == 0 else (195, 195, 195))
            d.text((145 + w, y + 87), n, font=F(40), fill=(20, 20, 20), anchor='lm')
        im.save(f'{OUT}/quiz2.{lang}.jpg', quality=85)
        # 3 science: TikTok-style text pills on the photo
        im = bg2.copy(); d = ImageDraw.Draw(im)
        def pill(cy, text, size, bg, fg):
            f = F(size); w = d.textlength(text, font=f); cx = (W - 110) / 2
            d.rounded_rectangle((cx - w / 2 - 30, cy - size * .75 - 14, cx + w / 2 + 30, cy + size * .75 + 14), 24, fill=bg)
            d.text((cx, cy), text, font=f, fill=fg, anchor='mm')
        y = 360
        for text, size, bg, fg, gap in t['s3']:
            pill(y, text, size, bg, fg); y += size * 1.5 + 28 + gap
        im.save(f'{OUT}/quiz3.{lang}.jpg', quality=85)
    # BGM: Kevin MacLeod "Monkeys Spinning Monkeys" (CC BY 4.0), passed as <audio_dir>/Monkeys Spinning Monkeys.mp3
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{AUD}/Monkeys Spinning Monkeys.mp3', '-map_metadata', '-1', '-af', 'loudnorm=I=-18',
                    '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '128k', f'{OUT}/bgm_monkeys.mp3'], check=True)
    print('done')
main()
