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
JA_STORY = [{'bg': 'astro', 'y': 560, 'note': '写真：アポロ12号の宇宙飛行士（NASA）', 'items': [('pill', 'なんで置いてきたの？', 52, (255, 255, 255), (0, 0, 0)), ('gap', 40), ('pill', '帰りに月の石を', 48, (0, 0, 0), (255, 255, 255)), ('pill', 'たくさん持ち帰るため', 48, (0, 0, 0), (255, 255, 255)), ('gap', 30), ('pill', 'いらない物は置いてきた', 56, (255, 206, 0), (0, 0, 0))]}, {'bg': 'lm', 'y': 600, 'items': [('pill', 'でも今、科学者が', 50, (255, 255, 255), (0, 0, 0)), ('pill', 'いちばん取りに行きたいのは', 50, (255, 255, 255), (0, 0, 0)), ('gap', 60), ('pill', 'うんち', 130, (255, 206, 0), (0, 0, 0))]}, {'bg': 'black', 'y': 560, 'items': [('pill', 'なんで？', 60, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('pill', 'うんちの約半分は', 56, (0, 0, 0), (255, 255, 255)), ('pill', 'おなかの「菌」', 80, (40, 190, 90), (255, 255, 255)), ('gap', 40), ('pill', '生き物が入った袋なんです', 46, (255, 255, 255), (0, 0, 0))]}, {'bg': 'ground', 'y': 430, 'items': [('pill', 'しかも月はこんな場所', 52, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('card', '空気', 'ない', (60, 140, 255)), ('card', '昼の温度', '約100℃', (230, 60, 60)), ('card', '夜の温度', '約−170℃', (60, 140, 255)), ('card', '放射線', 'あびっぱなし', (255, 150, 0)), ('gap', 10), ('pill', '生き物には最悪の場所', 52, (255, 206, 0), (0, 0, 0))]}, {'bg': 'black', 'y': 520, 'items': [('pill', 'そこで50年以上…', 56, (255, 255, 255), (0, 0, 0)), ('pill', 'もし菌が生きていたら', 56, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('pill', '生き物は', 70, (40, 190, 90), (255, 255, 255)), ('pill', '宇宙の旅にも', 70, (40, 190, 90), (255, 255, 255)), ('pill', '耐えられるかも', 70, (40, 190, 90), (255, 255, 255)), ('gap', 70), ('pill', '生きてると思う？ ○か×でコメントしてね', 40, (255, 206, 0), (0, 0, 0))]}]
EN_STORY = [{'bg': 'astro', 'y': 560, 'note': 'Photo: Apollo 12 astronaut (NASA)', 'items': [('pill', 'Why leave things there?', 50, (255, 255, 255), (0, 0, 0)), ('gap', 40), ('pill', 'To carry lots of', 48, (0, 0, 0), (255, 255, 255)), ('pill', 'Moon rocks home', 48, (0, 0, 0), (255, 255, 255)), ('gap', 30), ('pill', "they left what they didn't need", 46, (255, 206, 0), (0, 0, 0))]}, {'bg': 'lm', 'y': 600, 'items': [('pill', 'But what scientists', 50, (255, 255, 255), (0, 0, 0)), ('pill', 'most want back now is', 50, (255, 255, 255), (0, 0, 0)), ('gap', 60), ('pill', 'the poop', 120, (255, 206, 0), (0, 0, 0))]}, {'bg': 'black', 'y': 560, 'items': [('pill', 'Why?', 60, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('pill', 'About half of poop is', 54, (0, 0, 0), (255, 255, 255)), ('pill', 'gut microbes', 80, (40, 190, 90), (255, 255, 255)), ('gap', 40), ('pill', 'Bags full of life', 46, (255, 255, 255), (0, 0, 0))]}, {'bg': 'ground', 'y': 430, 'items': [('pill', 'And the Moon is like this:', 50, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('card', 'Air', 'none', (60, 140, 255)), ('card', 'Daytime', '~100°C', (230, 60, 60)), ('card', 'Night', '~−170°C', (60, 140, 255)), ('card', 'Radiation', 'nonstop', (255, 150, 0)), ('gap', 10), ('pill', 'The worst place for life', 50, (255, 206, 0), (0, 0, 0))]}, {'bg': 'black', 'y': 520, 'items': [('pill', 'After 50+ years there,', 54, (255, 255, 255), (0, 0, 0)), ('pill', 'if the microbes are alive', 54, (255, 255, 255), (0, 0, 0)), ('gap', 50), ('pill', 'life might', 70, (40, 190, 90), (255, 255, 255)), ('pill', 'survive trips', 70, (40, 190, 90), (255, 255, 255)), ('pill', 'through space', 70, (40, 190, 90), (255, 255, 255)), ('gap', 70), ('pill', 'Alive or not? Comment O or X', 42, (255, 206, 0), (0, 0, 0))]}]
COL = [(255, 64, 129), (60, 140, 255), (255, 150, 0), (40, 190, 90)]
T = {
 'ja': dict(tag='みんなの質問への返信', q=['月に人間が残した物で', 'いちばん数が多いのって', 'なに？'],
            ch=['カメラ', 'ブーツ', 'ゴルフボール', 'うんち'], ans='答え：D うんち（袋96個）',
            rows=[('うんち（袋）', '96個', 3), ('カメラ', '12台', 0), ('ブーツ', '12足', 1), ('ゴルフボール', '2個', 2)],
            why_q=['なんで置いてきたの？'], why=['帰りに月の石をたくさん', '持ち帰るため、', '重さを減らしたから'],
            sci_q=['今も残ってるなら', 'どうなってるの？'], sci=['科学者は「取りに行きたい」', '50年たった菌が生きていたら', '生き物は宇宙の旅にも', '耐えられるかもしれない'],
            note='写真：アポロ14号の着陸船（NASA）',
            story=JA_STORY),
 'en': dict(tag='Replying to your question', q=['What did people leave', 'on the Moon the most', 'of?'],
            ch=['Cameras', 'Boots', 'Golf balls', 'Poop'], ans='Answer: D, poop (96 bags)',
            rows=[('Poop (bags)', '96', 3), ('Cameras', '12', 0), ('Boots (pairs)', '12', 1), ('Golf balls', '2', 2)],
            why_q=['Why leave it there?'], why=['To bring lots of', 'Moon rocks home,', 'they had to cut weight'],
            sci_q=['So what is it', 'doing now?'], sci=['Scientists want it back.', 'If microbes survived 50 years,', 'life might survive', 'trips through space'],
            note='Photo: Apollo 14 lunar module (NASA)',
            story=EN_STORY),
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
    from PIL import ImageEnhance
    astro = Image.open(f'{IMG}/AS12-48-7133.jpg').convert('RGB')
    dim = lambda im, k=.45: ImageEnhance.Brightness(im).enhance(k)
    story_bg = {'astro': dim(cover(astro, .55, .6, 1.3), .7), 'ground': dim(cover(lm, .5, .9, 2.6), .55),
                'lm': dim(bg1, .5), 'black': Image.new('RGB', (W, H), (12, 12, 16))}
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
        # 3..7: one idea per slide, TikTok-style text pills
        for k, spec in enumerate(t['story'], start=3):
            im = story_bg[spec['bg']].copy(); d = ImageDraw.Draw(im)
            y = spec.get('y', 520)
            for item in spec['items']:
                kind = item[0]
                if kind == 'pill':
                    _, text, size, bg, fg = item; f = F(size); w = d.textlength(text, font=f); cx = (W - 110) / 2
                    d.rounded_rectangle((cx - w / 2 - 30, y - size * .75 - 14, cx + w / 2 + 30, y + size * .75 + 14), 24, fill=bg)
                    d.text((cx, y), text, font=f, fill=fg, anchor='mm'); y += size * 1.5 + 30
                elif kind == 'gap': y += item[1]
                elif kind == 'card':
                    _, label, value, col = item
                    d.rounded_rectangle((150, y - 60, 820, y + 60), 26, fill=(255, 255, 255))
                    d.rounded_rectangle((150, y - 60, 170, y + 60), 10, fill=col)
                    d.text((200, y), label, font=F(40, 'Bold'), fill=(110, 110, 110), anchor='lm')
                    d.text((790, y), value, font=F(48), fill=(20, 20, 20), anchor='rm'); y += 150
            if spec.get('note'): d.text((40, 1520), spec['note'], font=F(26, 'Bold'), fill=(235, 235, 235), stroke_width=3, stroke_fill=(0, 0, 0))
            im.save(f'{OUT}/quiz{k}.{lang}.jpg', quality=85)
    # BGM: Kevin MacLeod "Monkeys Spinning Monkeys" (CC BY 4.0), passed as <audio_dir>/Monkeys Spinning Monkeys.mp3
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{AUD}/Monkeys Spinning Monkeys.mp3', '-map_metadata', '-1', '-af', 'loudnorm=I=-18',
                    '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '128k', f'{OUT}/bgm_monkeys.mp3'], check=True)
    print('done')
main()
