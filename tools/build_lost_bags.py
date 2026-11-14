#!/usr/bin/env python3
"""Build "96 bags left on the Moon" (4 slides, ja/en) + a team-made dark ambience loop.
Usage: python3 tools/build_lost_bags.py <src_dir> <out_dir>   (src needs as14-66-09277.jpg)
"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
SRC, OUT = sys.argv[1], sys.argv[2]; W, H = 1080, 1920
MIN = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc'; SANS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def f(p, s): return ImageFont.truetype(p, s, index=0)
def cover(im, cx=.5, cy=.5, z=1.0):
    iw, ih = im.size; tw = min(iw, ih * W / H) / z; th = tw * H / W
    if th > ih: th = ih; tw = th * W / H
    x0 = min(max(cx * iw - tw / 2, 0), iw - tw); y0 = min(max(cy * ih - th / 2, 0), ih - th)
    return im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))
def dark(im, b=.42):
    im = ImageEnhance.Color(im).enhance(.15); im = ImageEnhance.Contrast(im).enhance(1.25); im = ImageEnhance.Brightness(im).enhance(b)
    v = Image.new('L', (W, H), 0); ImageDraw.Draw(v).ellipse((-300, -200, W + 300, H + 200), fill=255)
    return Image.composite(im, Image.new('RGB', (W, H)), v.filter(ImageFilter.GaussianBlur(220)))
def lines(d, y, rows):
    for text, font, col in rows:
        w = d.textlength(text, font=font)
        d.text(((W - 110 - w) / 2, y), text, font=font, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))
        y += font.size * 1.35
    return y
WHITE, GREY, RED, GOLD = (236, 233, 228), (175, 175, 175), (220, 32, 32), (255, 196, 0)
T = {
 'ja': [
  [('月には、', f(MIN, 66), WHITE), ('持ち主が名乗り出ない', f(MIN, 66), WHITE), ('落とし物が', f(MIN, 66), WHITE), ('96個ある。', f(MIN, 104), RED)],
  [('置いていったのは', f(MIN, 60), WHITE), ('月を歩いた 12人。', f(MIN, 76), WHITE), ('', f(MIN, 30), WHITE), ('白い袋に入れて、', f(MIN, 48), GREY), ('地面に置いてきた。', f(MIN, 48), GREY)],
  [('中身は……', f(MIN, 60), GREY), ('', f(MIN, 30), WHITE), ('うんち。', f(MIN, 150), RED), ('', f(MIN, 30), WHITE), ('（と、おしっこと、はいたもの）', f(SANS, 40), GREY)],
  [('でも、科学者は', f(MIN, 56), WHITE), ('「取りに行きたい」', f(MIN, 78), GOLD), ('', f(MIN, 30), WHITE), ('50年たった今も', f(SANS, 46), WHITE), ('中の菌は 生きてる？', f(SANS, 46), WHITE), ('', f(MIN, 20), WHITE), ('→ 生き物が宇宙をどこまで', f(SANS, 40), GREY), ('旅できるかの手がかりに', f(SANS, 40), GREY)],
 ],
 'en': [
  [('On the Moon,', f(MIN, 66), WHITE), ('there are lost items', f(MIN, 66), WHITE), ('no one has claimed.', f(MIN, 66), WHITE), ('96 of them.', f(MIN, 104), RED)],
  [('They were left by', f(MIN, 60), WHITE), ('the 12 moonwalkers.', f(MIN, 72), WHITE), ('', f(MIN, 30), WHITE), ('Packed in white bags,', f(MIN, 48), GREY), ('dropped on the ground.', f(MIN, 48), GREY)],
  [("What's inside...", f(MIN, 60), GREY), ('', f(MIN, 30), WHITE), ('poop.', f(MIN, 150), RED), ('', f(MIN, 30), WHITE), ('(and pee, and vomit)', f(SANS, 40), GREY)],
  [('But scientists say', f(MIN, 56), WHITE), ('"We want it back."', f(MIN, 74), GOLD), ('', f(MIN, 30), WHITE), ('After 50 years,', f(SANS, 46), WHITE), ('are the microbes still alive?', f(SANS, 46), WHITE), ('', f(MIN, 20), WHITE), ('A clue to how far life', f(SANS, 40), GREY), ('could travel in space', f(SANS, 40), GREY)],
 ]}
def main():
    os.makedirs(OUT, exist_ok=True)
    lm = Image.open(f'{SRC}/as14-66-09277.jpg').convert('RGB')
    bgs = [dark(cover(lm, .5, .55, 1.15)), dark(cover(lm, .3, .8, 2.2), .35), Image.new('RGB', (W, H), (6, 6, 8)), Image.new('RGB', (W, H), (6, 6, 8))]
    for lang, slides in T.items():
        for i, (bg, rows) in enumerate(zip(bgs, slides)):
            im = bg.copy(); d = ImageDraw.Draw(im)
            total = sum(r[1].size * 1.35 for r in rows)
            lines(d, max(330, 760 - total / 2), rows)
            if i < 2: d.text((40, 1330), {'ja': '写真：アポロ14号の着陸船（NASA）', 'en': 'Photo: Apollo 14 lunar module (NASA)'}[lang], font=f(SANS, 28), fill=(210, 210, 210), stroke_width=3, stroke_fill=(0, 0, 0))
            im.save(f'{OUT}/bags{i + 1}.{lang}.jpg', quality=84)
    # team-made dark ambience: two low detuned tones + filtered noise, 24 s loop
    fc = ("sine=f=98:d=24,volume=0.10,tremolo=f=0.3:d=0.6[a];sine=f=138.6:d=24,volume=0.06,tremolo=f=0.21:d=0.7[b];"
          "anoisesrc=d=24:c=brown:a=0.30,lowpass=f=500[n];[a][b][n]amix=inputs=3:normalize=0,afade=t=in:d=1.5,afade=t=out:st=22.5:d=1.5,alimiter=limit=0.9[o]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-filter_complex', fc, '-map', '[o]', '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '96k', f'{OUT}/dark_ambience.mp3'], check=True)
    print('done')
main()
