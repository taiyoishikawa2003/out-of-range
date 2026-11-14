#!/usr/bin/env python3
"""Kepler zodiac fortune video (TOP5, No.1 revealed in comments).
Ranking = K2 campaign fields whose centre lies in each zodiac constellation (STScI K2 campaign table),
tie-broken by total observed days. Builds media/kepler/uranai.{ja,en}.mp4 + posters.
Inputs: NASA images in /home/claude/nasa_dl/kepler, BGM "Heartwarming" (Kevin MacLeod, CC BY 4.0)."""
import subprocess, random, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W, H, FPS = 1080, 1920, 30
SRC = '/home/claude/nasa_dl/kepler/'; BGM = '/home/claude/dl_music2/Heartwarming.mp3'
OUT = 'media/kepler'; os.makedirs(OUT, exist_ok=True)
CX = (W - 110) // 2           # keep clear of the right-hand action rail
MAXW = 700                    # safe text width (px) around CX
GOLD = (255, 214, 120); WHITE = (255, 255, 255); INK = (20, 12, 40)
def F(sz, w='Black'): return ImageFont.truetype(f'/usr/share/fonts/opentype/noto/NotoSansCJK-{w}.ttc', sz, index=0)

def text_layer(lines, size, fill=WHITE, glow=None, stroke=10, gap=1.25, hl=None):
    """lines -> RGBA image (centered), thick outline + optional glow. hl: set of line indexes drawn in GOLD."""
    f = F(size); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    ws = [d0.textlength(t, font=f) for t in lines]
    if max(ws) > MAXW:            # phones crop the sides of a 9:16 video; keep every line inside the safe width
        size = int(size * MAXW / max(ws)); f = F(size); ws = [d0.textlength(t, font=f) for t in lines]
    w = int(max(ws) + stroke * 2 + 60); lh = int(size * gap)
    h = lh * len(lines) + stroke * 2 + 60
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, t in enumerate(lines):
        c = GOLD if hl and i in hl else fill
        d.text((w / 2, 30 + stroke + lh * i + lh / 2), t, font=f, fill=c, anchor='mm', stroke_width=stroke, stroke_fill=INK)
    if glow:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for i, t in enumerate(lines):
            gd.text((w / 2, 30 + stroke + lh * i + lh / 2), t, font=f, fill=glow + (255,), anchor='mm', stroke_width=stroke + 8, stroke_fill=glow + (255,))
        g = g.filter(ImageFilter.GaussianBlur(18)); g.alpha_composite(im); im = g
    return im

def cover(path, cx=.5, cy=.5, zoom=1.0, bright=.55, box=None):
    im = Image.open(path).convert('RGB')
    if box: im = im.crop(box)
    iw, ih = im.size
    tw = min(iw, ih * W / H) / zoom; th = tw * H / W
    x0 = max(0, min(iw - tw, cx * iw - tw / 2)); y0 = max(0, min(ih - th, cy * ih - th / 2))
    im = im.resize((int(W * 1.12), int(H * 1.12)), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))
    return ImageEnhance.Brightness(im).enhance(bright)

from PIL import ImageChops
FIELD = (395, 95, 2005, 1705)   # star-field area of the plate (outside is white border)
def night(cx, zoom, seed):
    st = cover(SRC + 'PIA11985.jpg', cx, .5, zoom, 1.0, FIELD).filter(ImageFilter.GaussianBlur(1.6))
    st = ImageEnhance.Brightness(ImageEnhance.Color(st).enhance(.35)).enhance(.9)
    base = Image.new('RGB', st.size); d = ImageDraw.Draw(base)
    for y in range(st.size[1]):
        k = y / st.size[1]; d.line((0, y, st.size[0], y), fill=(int(10 + 22 * k), int(14 + 10 * k), int(44 + 30 * k)))
    return ImageChops.screen(base, st)
BG_STARS = night(.5, 1.0, 1)
BG_STARS2 = night(.35, 1.5, 2)
# Kepler spacecraft art in the middle of the star field
def kepler_bg():
    b = BG_STARS.copy().filter(ImageFilter.GaussianBlur(2)); k = Image.open(SRC + 'PIA11824.jpg').convert('RGB')
    kw = int(W * 1.12 * .95); k = k.resize((kw, int(kw * k.height / k.width)), Image.LANCZOS)
    m = Image.new('L', k.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, k.width, k.height), 40, fill=255)
    b.paste(ImageEnhance.Brightness(k).enhance(.85), (int((W * 1.12 - kw) / 2) - 55, int(H * 1.12 / 2 - k.height / 2) - 160), m); return b
BG_KEP = kepler_bg()

# ---------- script ----------
T = {
 'ja': dict(
  title=(['NASAに'], ['“推されていた”', '星座TOP5']),
  ranks=[('第5位', ['その星座は', '有名人と縁がある'], ['一緒に写ったのは', '「すばる」'], 'おうし座', '推された回数 2回'),
         ('第4位', ['その星座は', 'ご近所づきあいが上手'], ['太陽系から約8光年の', 'ご近所の星を観測'], 'しし座', '推された回数 2回'),
         ('第3位', ['その星座は', '最後まで大切にされる'], ['燃料が尽きる前、', '最後に観測した星座'], 'みずがめ座', '推された回数 3回'),
         ('第2位', ['その星座は', '一途に愛される'], ['同じ星団に', '3回も会いに来た'], 'かに座', '推された回数 3回')],
  one=(['第1位は…'], ['コメント欄で', '発表！']),
  k1=(['この推し活の正体は'], ['NASAの', 'ケプラー宇宙望遠鏡']),
  k2=['星がほんの少し', '暗くなる瞬間を見張って', '惑星をさがしていた'],
  k3=(['見つけた惑星'], ['2,600個以上']),
  k4=(['あなたの星座の星にも', '惑星があるかも'], ['何位だったか', '教えてね']),
  sizes=dict(title=110, big=130, desc=84, fact=60, sign=150, sub=44)),
 'en': dict(
  title=(["NASA's"], ['“favorite”', 'zodiac signs', 'TOP 5']),
  ranks=[('No.5', ['This sign has', 'famous friends'], ['Pictured together:', 'the Pleiades'], 'TAURUS', 'Picked 2 times'),
         ('No.4', ['This sign is', 'great with neighbors'], ['It observed a star', '~8 light-years from the Sun'], 'LEO', 'Picked 2 times'),
         ('No.3', ['This sign is', 'cherished to the end'], ['The last sign observed', 'before the fuel ran out'], 'AQUARIUS', 'Picked 3 times'),
         ('No.2', ['This sign is', 'loved faithfully'], ['It came back 3 times', 'to the same star cluster'], 'CANCER', 'Picked 3 times')],
  one=(['No.1 is...'], ['in the', 'comments!']),
  k1=(['Who was the superfan?'], ["NASA's Kepler", 'Space Telescope']),
  k2=['It hunted planets', 'by watching for stars', 'to dim, just a little'],
  k3=(['Planets found'], ['2,600+']),
  k4=(['The stars of your sign', 'may have planets too'], ['What rank', 'was your sign?']),
  sizes=dict(title=100, big=120, desc=78, fact=56, sign=140, sub=44)),
}

def build_timeline(L):
    s = T[L]['sizes']; tl = []  # (start, end, bg, [(t_in, img, y_center, pop)], sparkle)
    t = 0.0
    a, b = T[L]['title']
    tl.append((t, t + 3.4, BG_STARS, [(0.1, text_layer(a, s['title']), 500, True), (0.5, text_layer(b, s['big'], fill=GOLD, glow=(255, 170, 60), stroke=12, gap=1.2), 870, True)], True)); t += 3.4
    for rank, desc, fact, sign, sub in T[L]['ranks']:
        els = [(0.0, text_layer([rank], 120, fill=GOLD, glow=(255, 150, 40), stroke=12), 430, True),
               (0.4, text_layer(desc, s['desc'], gap=1.25, hl={1}), 640, False),
               (1.9, text_layer(fact, s['fact'], gap=1.3, fill=(230, 230, 245), stroke=8), 860, False),
               (3.3, text_layer([sign], s['sign'], fill=WHITE, glow=(255, 190, 80), stroke=14), 1080, True),
               (3.5, text_layer([sub], s['sub'], fill=(225, 225, 240), stroke=6), 1230, False)]
        tl.append((t, t + 5.4, BG_STARS2 if len(tl) % 2 else BG_STARS, els, True)); t += 5.4
    a, b = T[L]['one']
    tl.append((t, t + 3.2, BG_STARS, [(0.0, text_layer(a, 120, fill=GOLD, glow=(255, 150, 40), stroke=12), 560, True), (0.9, text_layer(b, 110, stroke=12, glow=(255, 120, 160)), 900, True)], True)); t += 3.2
    a, b = T[L]['k1']
    tl.append((t, t + 3.6, BG_KEP, [(0.0, text_layer(a, 70), 410, True), (1.0, text_layer(b, 84, fill=GOLD, glow=(255, 170, 60), stroke=12), 1165, True)], False)); t += 3.6
    tl.append((t, t + 3.6, BG_STARS2, [(0.0, text_layer(T[L]['k2'], s['desc'], gap=1.3, hl={1}), 820, False)], False)); t += 3.6
    a, b = T[L]['k3']
    tl.append((t, t + 3.0, BG_STARS, [(0.0, text_layer(a, 80), 640, True), (0.4, text_layer(b, 150, fill=GOLD, glow=(255, 170, 60), stroke=14), 860, True)], True)); t += 3.0
    a, b = T[L]['k4']
    tl.append((t, t + 4.6, BG_STARS, [(0.0, text_layer(a, s['desc'], gap=1.3), 640, False), (1.4, text_layer(b, 96, fill=GOLD, glow=(255, 170, 60), stroke=12), 1000, True)], True)); t += 4.6
    return tl, t

def sparkle(fr, seed, n=26):
    r = random.Random(seed); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(n):
        x, y = r.randint(40, W - 150), r.randint(330, 1330); ph = r.random() * 6.28; sp = r.uniform(.15, .35)
        a = max(0, math.sin(fr * sp + ph)); L = 6 + 18 * a
        if a < .05: continue
        c = (255, 240, 200, int(230 * a))
        d.line((x - L, y, x + L, y), fill=c, width=3); d.line((x, y - L, x, y + L), fill=c, width=3)
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=c)
    return ov

def render(L):
    tl, total = build_timeline(L); nfr = int(total * FPS)
    out = f'{OUT}/uranai.{L}.mp4'; silent = f'/tmp/uranai_{L}_v.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    poster = None
    for fr in range(nfr):
        tt = fr / FPS
        seg = next(sg for sg in tl if sg[0] <= tt < sg[1]) if tt < tl[-1][1] else tl[-1]
        st, en, bg, els, spk = seg; lt = tt - st
        z = 1 + 0.06 * (lt / (en - st))       # slow push-in
        bw, bh = bg.size; cw, ch = W * 1.12 / z, H * 1.12 / z
        frame = bg.crop((int((bw - cw) / 2), int((bh - ch) / 2), int((bw + cw) / 2), int((bh + ch) / 2))).resize((W, H), Image.BILINEAR).convert('RGBA')
        if spk: frame.alpha_composite(sparkle(fr, int(st * 10)))
        for t_in, img, yc, pop in els:
            if lt < t_in: continue
            k = min(1, (lt - t_in) / 0.28); a = k
            sc = (0.7 + 0.3 * (1 - (1 - k) ** 3) + (0.06 * math.sin(k * math.pi) if pop else 0)) if pop else 1
            im = img if sc == 1 else img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
            if a < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
            yoff = 0 if pop else int(30 * (1 - k))
            frame.alpha_composite(im, (int(CX - im.width / 2), int(yc - im.height / 2 + yoff)))
        # fade to black over the segment edges (soft cuts)
        edge = min(lt, en - lt)
        if edge < 0.12:
            frame = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), frame, max(0, edge / 0.12) * 0.6 + 0.4)
        rgb = frame.convert('RGB'); p.stdin.write(rgb.tobytes())
        if abs(tt - 1.5) < 1 / FPS / 2: poster = rgb
    p.stdin.close(); p.wait()
    (poster or rgb).save(f'{OUT}/uranai.poster.{L}.jpg', quality=88)
    fade_st = total - 2.2
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', silent, '-i', BGM, '-filter_complex',
                    f'[1:a]atrim=0:{total},asetpts=N/SR/TB,afade=t=in:d=0.4,afade=t=out:st={fade_st}:d=2.2,loudnorm=I=-16:TP=-1.5[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(total, 1), 's')

if __name__ == '__main__':
    for L in (sys.argv[1:] or ['ja', 'en']): render(L)
