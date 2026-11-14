#!/usr/bin/env python3
"""Kepler zodiac fortune video: "NASA's favorite zodiac signs TOP5" (No.1 revealed in the comments).
Ranking = K2 campaign fields whose centre lies in each zodiac constellation (MAST/STScI K2 campaign table),
ties broken by total observed days. Builds media/kepler/uranai.{ja,en}.mp4 + posters.
Images: NASA (PIA15801 Beehive, PIA09262 Pleiades, PIA21473 red dwarf illustration, PIA21751 TRAPPIST-1 concept,
PIA11824 Kepler). BGM: "Heartwarming" Kevin MacLeod (CC BY 4.0). Chime sound effect is synthesized here."""
import subprocess, random, math, os, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
W, H, FPS = 1080, 1920, 30
K = '/home/claude/nasa_dl/kepler/'; U = '/home/claude/nasa_dl/uranai/'; BGM = '/home/claude/dl_music2/Heartwarming.mp3'
OUT = 'media/kepler'; os.makedirs(OUT, exist_ok=True)
CX = (W - 110) // 2            # keep clear of the right-hand action rail
MAXW = 700                     # phones crop the sides of a 9:16 video; keep every line inside this width
GOLD = (255, 214, 120); WHITE = (255, 255, 255); INK = (20, 12, 40)
def F(sz, w='Black'): return ImageFont.truetype(f'/usr/share/fonts/opentype/noto/NotoSansCJK-{w}.ttc', sz, index=0)

def text_layer(lines, size, fill=WHITE, glow=None, stroke=10, gap=1.25, hl=None, weight='Black'):
    f = F(size, weight); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    ws = [d0.textlength(t, font=f) for t in lines]
    if max(ws) > MAXW:
        size = int(size * MAXW / max(ws)); f = F(size, weight); ws = [d0.textlength(t, font=f) for t in lines]
    w = int(max(ws) + stroke * 2 + 60); lh = int(size * gap); h = lh * len(lines) + stroke * 2 + 60
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pos = lambda i: (w / 2, 30 + stroke + lh * i + lh / 2)
    for i, t in enumerate(lines):
        d.text(pos(i), t, font=f, fill=GOLD if hl and i in hl else fill, anchor='mm', stroke_width=stroke, stroke_fill=INK)
    if glow:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for i, t in enumerate(lines): gd.text(pos(i), t, font=f, fill=glow + (255,), anchor='mm', stroke_width=stroke + 8, stroke_fill=glow + (255,))
        g = g.filter(ImageFilter.GaussianBlur(18)); g.alpha_composite(im); im = g
    return im

BW, BH = int(W * 1.1), int(H * 1.1)   # backgrounds are slightly larger for a slow push-in
def cover(path, cx=.5, cy=.5, zoom=1.0):
    im = Image.open(path).convert('RGB'); iw, ih = im.size
    tw = min(iw, ih * W / H) / zoom; th = tw * H / W
    x0 = max(0, min(iw - tw, cx * iw - tw / 2)); y0 = max(0, min(ih - th, cy * ih - th / 2))
    return im.resize((BW, BH), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))
def grade(im, bright=.55, sat=1.0, vignette=True):
    im = ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(bright)).enhance(sat)
    if vignette:   # darken top and bottom so text and the app UI stay readable
        g = Image.new('L', (1, BH))
        for y in range(BH): g.putpixel((0, y), int(170 * min(1, max(0, abs(y / BH - .45) - .18) / .3)))
        im = Image.composite(Image.new('RGB', im.size), im, g.resize(im.size))
    return im
def navy(st):   # tint a star photo into a deep navy-violet night sky
    base = Image.new('RGB', st.size); d = ImageDraw.Draw(base)
    for y in range(st.size[1]):
        k = y / st.size[1]; d.line((0, y, st.size[0], y), fill=(int(10 + 22 * k), int(14 + 10 * k), int(44 + 30 * k)))
    return ImageChops.screen(base, ImageEnhance.Color(st).enhance(.6))

BG = {
 'night': navy(grade(cover(U + 'PIA15801.jpg', .25, .5, 1.25), .75, vignette=False)),
 'night2': navy(grade(cover(U + 'PIA15801.jpg', .75, .5, 1.6), .7, vignette=False)),
 'taurus': grade(cover(U + 'PIA09262.jpg', .45, .45, 1.0), .5, 1.1),
 'leo': grade(cover(U + 'PIA21473.jpg', .45, .5, 1.0), .45),
 'aquarius': grade(cover(U + 'PIA21751.jpg', .2, .5, 1.0), .5),
 'cancer': grade(cover(U + 'PIA15801.jpg', .5, .5, 1.05), .7),
}
def kepler_bg():
    b = BG['night'].copy(); k = Image.open(K + 'PIA11824.jpg').convert('RGB')
    kw = int(BW * .95); k = k.resize((kw, int(kw * k.height / k.width)), Image.LANCZOS)
    m = Image.new('L', k.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, k.width, k.height), 40, fill=255)
    b.paste(ImageEnhance.Brightness(k).enhance(.85), (int((BW - kw) / 2) - 55, int(BH / 2 - k.height / 2) - 160), m); return b
BG['kepler'] = kepler_bg()

T = {
 'ja': dict(
  title=('NASAに', '“推されていた”', '星座TOP5'),
  ranks=[('第5位', ['その星座は', '有名人と縁がある'], ['一緒に写ったのは', '「すばる」'], 'おうし座', '推された回数 2回', 'taurus', '画像：すばる（NASA スピッツァー宇宙望遠鏡）'),
         ('第4位', ['その星座は', 'ご近所づきあいが上手'], ['太陽系から約8光年の', 'ご近所の星を観測'], 'しし座', '推された回数 2回', 'leo', '画像：赤色矮星の想像図（NASA）'),
         ('第3位', ['その星座は', '最後まで大切にされる'], ['燃料が尽きる前、', '最後に観測した星座'], 'みずがめ座', '推された回数 3回', 'aquarius', '画像：7つの惑星をもつ星トラピスト1の想像図（NASA）'),
         ('第2位', ['その星座は', '一途に愛される'], ['同じ星団に', '3回も会いに来た'], 'かに座', '推された回数 3回', 'cancer', '画像：プレセペ星団（NASA）')],
  one=(['第1位は…'], ['コメント欄で', '発表！']),
  k1=(['この推し活の正体は'], ['NASAの', 'ケプラー宇宙望遠鏡']),
  k2=(['惑星が星の前を通ると', '星の光がほんの少し暗くなる'], ['この瞬間を見張って', '惑星をさがしていた'], '明るさ', '※わかりやすく大きく描いています'),
  k3=(['見つけた惑星'], ['2,600個以上']),
  k4=(['あなたの星座の星にも', '惑星があるかも'], ['何位だったか', '教えてね']),
  sizes=dict(desc=84, fact=60, sign=150, sub=44, cap=26)),
 'en': dict(
  title=("NASA's", '“favorite”', 'zodiac signs TOP 5'),
  ranks=[('No.5', ['This sign has', 'famous friends'], ['Pictured together:', 'the Pleiades'], 'TAURUS', 'Picked 2 times', 'taurus', 'Image: the Pleiades (NASA Spitzer)'),
         ('No.4', ['This sign is', 'great with neighbors'], ['It observed a star', '~8 light-years from the Sun'], 'LEO', 'Picked 2 times', 'leo', "Image: red dwarf star, artist's concept (NASA)"),
         ('No.3', ['This sign is', 'cherished to the end'], ['The last sign observed', 'before the fuel ran out'], 'AQUARIUS', 'Picked 3 times', 'aquarius', "Image: TRAPPIST-1 (7 planets), artist's concept (NASA)"),
         ('No.2', ['This sign is', 'loved faithfully'], ['It came back 3 times', 'to the same star cluster'], 'CANCER', 'Picked 3 times', 'cancer', 'Image: the Beehive Cluster (NASA)')],
  one=(['No.1 is...'], ['in the', 'comments!']),
  k1=(['Who was the superfan?'], ["NASA's Kepler", 'Space Telescope']),
  k2=(['When a planet passes its star,', 'the star dims a little'], ['Kepler watched for this', 'to find planets'], 'Brightness', '*Dip exaggerated so you can see it'),
  k3=(['Planets found'], ['2,600+']),
  k4=(['The stars of your sign', 'may have planets too'], ['What rank', 'was your sign?']),
  sizes=dict(desc=78, fact=56, sign=140, sub=44, cap=26)),
}

def transit(frame, lt, L):
    """Animated transit: a planet crosses a star while the light curve below dips."""
    sx, sy, R, pr = CX, 800, 150, 34; p0, p1 = 0.5, 3.6
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((sx - R - 60, sy - R - 60, sx + R + 60, sy + R + 60), fill=(255, 200, 120, 120))
    frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(frame)
    d.ellipse((sx - R, sy - R, sx + R, sy + R), fill=(255, 236, 190))
    k = min(1, max(0, (lt - p0) / (p1 - p0))); span = 2 * R + 180
    px = sx - R - 90 + k * span
    d.ellipse((px - pr, sy - pr + 20, px + pr, sy + pr + 20), fill=(28, 24, 46))
    gx0, gx1, gy = 150, 820, 1080
    d.text((gx0, gy - 40), T[L]['k2'][2], font=F(30, 'Bold'), fill=(210, 210, 230), anchor='lm')
    pts = []
    for i in range(0, int(k * 200) + 1):
        u = i / 200; x = sx - R - 90 + u * span; over = max(0, min(1, (R + pr - abs(x - sx)) / (2 * pr)))
        pts.append((gx0 + u * (gx1 - gx0), gy + 70 * over))
    d.line((gx0, gy + 100, gx1, gy + 100), fill=(120, 120, 150), width=2)
    if len(pts) > 1: d.line(pts, fill=GOLD, width=7, joint='curve')
    d.text((gx1, gy + 135), T[L]['k2'][3], font=F(24, 'Medium'), fill=(180, 180, 205), anchor='rm')

def build_timeline(L):
    s = T[L]['sizes']; tl = []; t = 0.0; chimes = []
    a, b, c = T[L]['title']
    tl.append((t, t + 3.4, 'night', [(0.05, text_layer([a], 100), 470, True), (0.35, text_layer([b], 140, fill=GOLD, glow=(255, 160, 60), stroke=13), 700, True),
                                    (0.75, text_layer([c], 120, glow=(255, 190, 120), stroke=12), 930, True)], True, None)); t += 3.4
    for rank, desc, fact, sign, sub, bg, cap in T[L]['ranks']:
        els = [(0.0, text_layer([rank], 120, fill=GOLD, glow=(255, 150, 40), stroke=12), 430, True),
               (0.4, text_layer(desc, s['desc'], gap=1.25, hl={1}), 640, False),
               (1.9, text_layer(fact, s['fact'], gap=1.3, fill=(235, 235, 248), stroke=8), 860, False),
               (3.3, text_layer([sign], s['sign'], glow=(255, 190, 80), stroke=14), 1080, True),
               (3.5, text_layer([sub], s['sub'], fill=(225, 225, 240), stroke=6), 1220, False),
               (0.4, text_layer([cap], s['cap'], fill=(205, 205, 220), stroke=4, weight='Medium'), 1295, False)]
        chimes.append(t + 3.3); tl.append((t, t + 5.4, bg, els, True, 'flash')); t += 5.4
    a, b = T[L]['one']
    tl.append((t, t + 3.2, 'night2', [(0.0, text_layer(a, 120, fill=GOLD, glow=(255, 150, 40), stroke=12), 560, True), (0.9, text_layer(b, 110, stroke=12, glow=(255, 120, 160)), 900, True)], True, None))
    chimes.append(t + 0.9); t += 3.2
    a, b = T[L]['k1']
    tl.append((t, t + 3.6, 'kepler', [(0.0, text_layer(a, 70), 410, True), (1.0, text_layer(b, 84, fill=GOLD, glow=(255, 170, 60), stroke=12), 1165, True)], False, None)); t += 3.6
    a, b, _, _ = T[L]['k2']
    tl.append((t, t + 5.6, 'night2', [(0.0, text_layer(a, 60, gap=1.3), 470, False), (3.9, text_layer(b, 64, gap=1.3, fill=GOLD, stroke=10), 470, False)], False, 'transit')); t += 5.6
    a, b = T[L]['k3']
    tl.append((t, t + 3.0, 'night', [(0.0, text_layer(a, 80), 640, True), (0.4, text_layer(b, 150, fill=GOLD, glow=(255, 170, 60), stroke=14), 860, True)], True, None))
    chimes.append(t + 0.4); t += 3.0
    a, b = T[L]['k4']
    tl.append((t, t + 4.6, 'night', [(0.0, text_layer(a, 76, gap=1.3), 640, False), (1.4, text_layer(b, 96, fill=GOLD, glow=(255, 170, 60), stroke=12), 1000, True)], True, None)); t += 4.6
    return tl, t, chimes

def sparkle(fr, seed, n=26):
    r = random.Random(seed); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(n):
        x, y = r.randint(40, W - 150), r.randint(330, 1330); ph = r.random() * 6.28; sp = r.uniform(.15, .35)
        a = max(0, math.sin(fr * sp + ph)); Lr = 6 + 18 * a
        if a < .05: continue
        c = (255, 240, 200, int(230 * a))
        d.line((x - Lr, y, x + Lr, y), fill=c, width=3); d.line((x, y - Lr, x, y + Lr), fill=c, width=3); d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=c)
    return ov

def chime_wav(times, total, path, sr=44100):
    """Soft bell chime (synthesized by the team) at each reveal."""
    out = np.zeros(int(total * sr) + 2 * sr); tt = np.arange(int(1.6 * sr)) / sr
    bell = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * dcy) for f, a, dcy in [(1567.98, .5, 3.2), (2349.3, .3, 4.5), (3135.9, .18, 6), (783.99, .25, 2.5)])
    bell = bell * np.minimum(1, tt / .004)
    for t0 in times:
        k = int(t0 * sr); out[k:k + len(bell)] += bell
    out = (out / max(1e-9, np.abs(out).max()) * 0.6 * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes())

def render(L):
    tl, total, chimes = build_timeline(L); nfr = int(total * FPS)
    out = f'{OUT}/uranai.{L}.mp4'; silent = f'/tmp/uranai_{L}_v.mp4'; cw = f'/tmp/uranai_{L}_chime.wav'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    poster = None
    for fr in range(nfr):
        tt = fr / FPS
        st, en, bgk, els, spk, special = next((sg for sg in tl if sg[0] <= tt < sg[1]), tl[-1]); lt = tt - st
        z = 1 + 0.06 * (lt / (en - st)); cw_, ch_ = BW / z, BH / z
        frame = BG[bgk].crop((int((BW - cw_) / 2), int((BH - ch_) / 2), int((BW + cw_) / 2), int((BH + ch_) / 2))).resize((W, H), Image.BILINEAR).convert('RGBA')
        if spk: frame.alpha_composite(sparkle(fr, int(st * 10)))
        if special == 'transit': transit(frame, lt, L)
        for j, (t_in, img, yc, pop) in enumerate(els):
            if lt < t_in: continue
            if special == 'transit' and j == 0 and lt >= els[1][0]: continue   # second caption replaces the first
            k = min(1, (lt - t_in) / 0.28)
            sc = (0.7 + 0.3 * (1 - (1 - k) ** 3) + 0.06 * math.sin(k * math.pi)) if pop else 1
            im = img if sc == 1 else img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
            if k < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * k)))
            frame.alpha_composite(im, (int(CX - im.width / 2), int(yc - im.height / 2 + (0 if pop else int(30 * (1 - k))))))
        if special == 'flash' and 0 <= lt - els[3][0] < 0.25:   # soft flash as the sign name appears
            a = int(80 * (1 - (lt - els[3][0]) / 0.25)); frame.alpha_composite(Image.new('RGBA', (W, H), (255, 240, 210, a)))
        edge = min(lt, en - lt)
        if edge < 0.12: frame = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), frame, max(0, edge / 0.12) * 0.6 + 0.4)
        rgb = frame.convert('RGB'); p.stdin.write(rgb.tobytes())
        if abs(tt - 1.6) < 1 / FPS / 2: poster = rgb
    p.stdin.close(); p.wait()
    (poster or rgb).save(f'{OUT}/uranai.poster.{L}.jpg', quality=88)
    chime_wav(chimes, total, cw)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', silent, '-i', BGM, '-i', cw, '-filter_complex',
                    f'[1:a]atrim=0:{total},asetpts=N/SR/TB,afade=t=in:d=0.4,afade=t=out:st={total - 2.2}:d=2.2[m];'
                    f'[2:a]volume=0.25[c];[m][c]amix=inputs=2:normalize=0,atrim=0:{total},loudnorm=I=-16:TP=-1.5[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(total, 1), 's')

if __name__ == '__main__':
    for L in (sys.argv[1:] or ['ja', 'en']): render(L)
