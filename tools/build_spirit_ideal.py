#!/usr/bin/env python3
"""Build the 4 slides of "Spirit: expectation vs reality" (ja / en) from NASA images.

Usage: python3 tools/build_spirit_ideal.py <src_dir> <out_dir>
Slide 1 is a NASA artist's concept; slides 2-4 are real photos taken by Spirit on Mars.
Text uses TikTok-style rounded text boxes, kept inside the app's safe area.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
BLACK = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 0)
BOLD = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 0)

def font(spec, sz): return ImageFont.truetype(spec[0], sz, index=spec[1])

def cover(img, cx=.5, cy=.5, zoom=1.0):
    iw, ih = img.size
    tw = min(iw, ih * W / H) / zoom; th = tw * H / W
    if th > ih: th = ih; tw = th * W / H
    x0 = min(max(cx * iw - tw / 2, 0), iw - tw); y0 = min(max(cy * ih - th / 2, 0), ih - th)
    return img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))

def box(d, text, y, f, fg, bg, pad=(26, 14), r=18):
    """TikTok-like text on a rounded box, centred; returns bottom y."""
    lines = text.split('\n'); lh = f.size * 1.25
    widths = [d.textlength(l, font=f) for l in lines]
    w = max(widths) + pad[0] * 2; h = lh * len(lines) + pad[1] * 2
    x = (W - 120 - w) / 2  # keep clear of the right-hand button rail
    d.rounded_rectangle((x, y, x + w, y + h), r, fill=bg)
    for i, (l, lw) in enumerate(zip(lines, widths)):
        d.text((x + (w - lw) / 2, y + pad[1] + i * lh + lh / 2), l, font=f, fill=fg, anchor='lm')
    return y + h

def outline(d, text, y, f, fill=(255, 255, 255), stroke=(0, 0, 0)):
    lines = text.split('\n'); lh = f.size * 1.3
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f)
        d.text(((W - 120 - w) / 2, y + i * lh), l, font=f, fill=fill, stroke_width=max(4, f.size // 11), stroke_fill=stroke)
    return y + lh * len(lines)

TXT = {
  'ja': [
    ('理想', '火星探査機の理想', '6つの車輪で、かっこよく走る'),
    ('現実', '前輪こわれた', '後ろ向きに、引きずって走ってる'),
    ('現実', 'しかも溝から', 'なんか白い土が出てきた'),
    ('でも実は', 'ほぼ純粋な「シリカ」', '温泉や蒸気の跡\n＝生き物がすめたかもしれない証拠'),
  ],
  'en': [
    ('Expectation', 'Mars rover expectations', 'Six wheels, cruising in style'),
    ('Reality', 'Front wheel broke', 'Now driving backwards,\ndragging it along'),
    ('Reality', 'And the rut it dug', 'turned up weird white soil'),
    ('But actually', 'Almost pure silica', 'Left by hot springs or steam\n= a place life could have lived'),
  ],
}

def main():
    os.makedirs(OUT, exist_ok=True)
    concept = Image.open(f'{SRC}/PIA04413.jpg').convert('RGB')
    drag = Image.open(f'{SRC}/PIA11823.jpg').convert('RGB')
    silica = Image.open(f'{SRC}/PIA09491.jpg').convert('RGB')
    bgs = [
        ImageEnhance.Color(cover(concept, .47, .5)).enhance(1.15),
        ImageEnhance.Contrast(cover(drag, .62, .55)).enhance(1.15),
        cover(silica, .55, .5),
        ImageEnhance.Contrast(cover(silica, .6, .55, 1.9)).enhance(1.1),
    ]
    for lang, rows in TXT.items():
        for i, ((tag, head, sub), bg) in enumerate(zip(rows, bgs)):
            im = bg.copy()
            # soft dark band at the top so text reads on any photo
            band = Image.new('L', (W, H), 0); ImageDraw.Draw(band).rectangle((0, 0, W, 900), fill=150)
            band = band.filter(ImageFilter.GaussianBlur(120))
            im = Image.composite(Image.new('RGB', (W, H)), im, band)
            d = ImageDraw.Draw(im)
            if i == 0:   tag_fg, tag_bg = (255, 255, 255), (255, 64, 129)    # ideal: bright pink
            elif i < 3:  tag_fg, tag_bg = (255, 255, 255), (20, 20, 20)      # reality: flat black
            else:        tag_fg, tag_bg = (20, 20, 20), (255, 196, 0)       # twist: yellow
            y = box(d, tag, 400, font(BLACK, 64), tag_fg, tag_bg, pad=(34, 16), r=22)
            y = outline(d, head, y + 40, font(BLACK, 76))
            if i == 3: box(d, sub, y + 30, font(BOLD, 46), (20, 20, 20), (255, 255, 255))
            else: outline(d, sub, y + 20, font(BOLD, 50))
            note = {'ja': 'NASAの想像図', 'en': "NASA artist's concept"}[lang] if i == 0 else {'ja': '火星で撮った本物の写真', 'en': 'Real photo from Mars'}[lang]
            d.text((40, 1330), note, font=font(BOLD, 30), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
            im.save(f'{OUT}/s{i + 1}.{lang}.jpg', quality=84)
    print('done')

main()
