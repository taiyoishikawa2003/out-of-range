#!/usr/bin/env python3
"""Build "InSight kaidan Part 1" (ja / en, ~31 s) from NASA media.

Horror look: graded stills, grain, vignette, flicker, shake + red flash on hits,
found-footage HUD, word-by-word captions (ja: Mincho, en: bold sans, key word in red).
Sounds: NASA InSight data (impact, wind) + team-made synth drone / riser / hit.
Usage: python3 tools/build_kaidan_insight.py <src_dir> <out_dir>
"""
import random, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 720, 1280, 30
TOTAL = 31.0
F_JA = ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc', 0)
F_EN = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 0)
F_UI = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc', 0)
BLOOP_AT, BLOOP_LEN, PEAKS = 57.70, 3.0, [0.15, 1.40, 1.65]  # impact sound inside the NASA video
B1, B4 = 0.2, 12.6                                          # where the impact sound is placed
HITS = [B1 + x for x in PEAKS] + [B4 + x for x in PEAKS]
STING = 24.0                                                # synth hit on "no microphone"

# scenes: (start, end, image or None)
SC = [(0, 3.2, None), (3.2, 7.5, 'orbit'), (7.5, 11.4, 'deck'), (11.4, 17.0, None),
      (17.0, 21.5, 'crater'), (21.5, 26.0, 'selfie'), (26.0, TOTAL, None)]

# captions: dict(a=appear, b=end, s=text ("^red^", "\n"), y, z=size, st=type|slam|whisper, fx="shake glitch ghost", x=offset, r=rotation)
def C(a, b, s, y, z, st='type', fx='', x=0, r=0): return dict(a=a, b=b, s=s, y=y, z=z, st=st, fx=fx, x=x, r=r)
def cap(lang):
    h1, h2, h3 = HITS[3:]
    if lang == 'ja':
        return [
          C(0, 3.2, '※イヤホン推奨', 190, 26, 'whisper'),
          C(2.0, 3.2, '……今の、聞こえた？', 640, 58, 'type', 'shake'),
          C(3.5, 7.5, 'これ、^火星^で録れた音。', 620, 54),
          C(5.4, 7.5, 'まわりには、誰もいない。', 720, 38, 'whisper'),
          C(7.8, 11.4, '聞こえるのは、風だけ。', 620, 54),
          C(10.0, 11.4, '……の、^はずだった。^', 730, 62, 'slam', 'glitch shake'),
          C(h1, 17.0, 'ボッ', 440, 110, 'slam', 'glitch', -140, -8),
          C(h2, 17.0, 'ボッ', 610, 124, 'slam', 'glitch', 110, 7),
          C(h3, 17.0, '^ボッ^', 800, 150, 'slam', 'glitch shake', -10, -3),
          C(15.6, 17.0, '3回。', 300, 40, 'whisper'),
          C(17.3, 21.5, '上から、撮ってみたら', 250, 46),
          C(19.0, 21.5, '地面に、^穴^。', 360, 66, 'slam', 'shake'),
          C(21.8, 26.0, '……ねえ。', 560, 44, 'whisper'),
          C(22.8, 26.0, 'こいつ、', 660, 60),
          C(STING, 26.0, '^マイク、ない。^', 790, 86, 'slam', 'glitch shake ghost'),
          C(26.0, TOTAL, '素材：NASA/JPL-Caltech ほか　効果音：チーム制作', 170, 20, 'whisper'),
          C(26.6, TOTAL, 'じゃあ……', 600, 62),
          C(27.9, TOTAL, '^何^が、聞いてたの？', 710, 66, 'slam', 'shake ghost'),
          C(29.2, TOTAL, '答えはコメ欄', 830, 32, 'whisper'),
        ]
    return [
          C(0, 3.2, '(headphones on)', 190, 26, 'whisper'),
          C(2.0, 3.2, '...did you hear that?', 640, 54, 'type', 'shake'),
          C(3.5, 7.5, 'This was recorded\non ^Mars^.', 620, 52),
          C(5.4, 7.5, 'No one around.', 760, 38, 'whisper'),
          C(7.8, 11.4, 'All you hear\nis wind.', 620, 54),
          C(10.0, 11.4, '...or ^so we thought.^', 760, 54, 'slam', 'glitch shake'),
          C(h1, 17.0, 'bloop', 440, 92, 'slam', 'glitch', -120, -8),
          C(h2, 17.0, 'bloop', 610, 104, 'slam', 'glitch', 100, 7),
          C(h3, 17.0, '^bloop^', 800, 124, 'slam', 'glitch shake', -10, -3),
          C(15.6, 17.0, '3 times.', 300, 40, 'whisper'),
          C(17.3, 21.5, 'Seen from above,', 250, 46),
          C(19.0, 21.5, 'new ^holes^.', 360, 66, 'slam', 'shake'),
          C(21.8, 26.0, '...wait.', 560, 44, 'whisper'),
          C(22.8, 26.0, 'This thing', 660, 58),
          C(STING, 26.0, '^has no mic.^', 790, 84, 'slam', 'glitch shake ghost'),
          C(26.0, TOTAL, 'Media: NASA/JPL-Caltech et al.  SFX: our team', 170, 20, 'whisper'),
          C(26.6, TOTAL, 'So...', 600, 62),
          C(27.9, TOTAL, '^what^ was listening?', 710, 62, 'slam', 'shake ghost'),
          C(29.2, TOTAL, 'Answer in the comments', 830, 32, 'whisper'),
    ]

RED = (230, 30, 30)

def font(spec, sz): return ImageFont.truetype(spec[0], sz, index=spec[1])

def grade(img):
    """Cold, desaturated, dark, contrasty."""
    img = ImageEnhance.Color(img).enhance(.35)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Brightness(img).enhance(.62)
    r, g, b = img.split()
    return Image.merge('RGB', (r.point(lambda v: v * .9), g, b.point(lambda v: min(255, v * 1.08 + 6))))

def cover(img, cx=.5, cy=.5, zoom=1.0):
    iw, ih = img.size
    tw = min(iw, ih * W / H) / zoom; th = tw * H / W
    x0 = min(max(cx * iw - tw / 2, 0), iw - tw); y0 = min(max(cy * ih - th / 2, 0), ih - th)
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + tw, y0 + th))

def fitwide(img, bg, zoom=1.0):
    out = bg.copy(); iw, ih = img.size; w = int(W * zoom); h = int(ih * w / iw)
    out.paste(img.resize((w, h), Image.BILINEAR), ((W - w) // 2, (H - h) // 2 + 60))
    return out

def vignette():
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse((-W * .35, -H * .2, W * 1.35, H * 1.2), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(160))
    return Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [ImageChops.invert(m).point(lambda v: v * .95)])

F_CAP = ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc', 0)
F_WH = ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', 0)

def segs(s):
    """'a^b^c' -> [(char, red)] with newlines kept."""
    out, red = [], False
    for ch in s:
        if ch == '^': red = not red
        else: out.append((ch, red))
    return out

def char_times(it):
    """Irregular typewriter timing (pauses after punctuation)."""
    rnd = random.Random(hash(it['s']) & 0xffff); t = it['a']; ts = []
    for ch, _ in segs(it['s']):
        ts.append(t)
        t += (0.30 if ch in '、。…,.?？' else rnd.uniform(.045, .13)) if ch != '\n' else 0
    return ts

_cache = {}
def text_img(it, n):
    """RGBA image (cropped) of the first n characters, with shadow."""
    key = (id(it), n)
    if key in _cache: return _cache[key]
    f = font(F_WH if it['st'] == 'whisper' else F_CAP, it['z'])
    cs = segs(it['s']); lines = [[]]
    for c in cs:
        if c[0] == '\n': lines.append([])
        else: lines[-1].append(c)
    lh = int(it['z'] * 1.3); pad = 30
    tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    lw = [sum(tmp.textlength(c, font=f) for c, _ in ln) for ln in lines]
    Wd, Hd = int(max(lw) + pad * 2), int(lh * len(lines) + pad * 2)
    lay = Image.new('RGBA', (Wd, Hd)); sh = Image.new('RGBA', (Wd, Hd))
    dl, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    k = 0
    for li, ln in enumerate(lines):
        x = pad + (max(lw) - lw[li]) / 2; y = pad + li * lh + lh / 2
        for c, red in ln:
            if k >= n: break
            col = RED if red else ((222, 222, 222) if it['st'] == 'whisper' else (236, 232, 228))
            ds.text((x, y + 2), c, font=f, fill=(0, 0, 0, 255), anchor='lm')
            dl.text((x, y), c, font=f, fill=col + (255,), anchor='lm')
            x += tmp.textlength(c, font=f); k += 1
        k += 0
    sh = sh.filter(ImageFilter.GaussianBlur(max(4, it['z'] // 10)))
    out = Image.alpha_composite(Image.alpha_composite(sh, sh), lay)
    if it['r']: out = out.rotate(it['r'], resample=Image.BICUBIC, expand=True)
    _cache[key] = out
    return out

def draw_caption(fr, it, t, rnd):
    if not (it['a'] <= t < it['b']): return fr
    dt = t - it['a']; total = len([c for c, _ in segs(it['s']) if c != '\n'])
    if it['st'] == 'type':
        n = sum(1 for x, (c, _) in zip(char_times(it), segs(it['s'])) if c != '\n' and t >= x)
    else: n = total
    if n == 0: return fr
    img = text_img(it, n)
    alpha = 1.0; scale = 1.0
    if it['st'] == 'whisper': alpha = min(1, dt / .5)
    if it['st'] == 'slam': scale = 1 + .45 * max(0, 1 - dt / .12)
    if t > it['b'] - .15: alpha *= max(0, (it['b'] - t) / .15)
    if scale != 1: img = img.resize((int(img.width * scale), int(img.height * scale)), Image.BILINEAR)
    fx = it['fx']
    ox, oy = 0, 0
    if 'shake' in fx: ox, oy = rnd.randint(-3, 3), rnd.randint(-2, 2)
    glitch = 'glitch' in fx and (dt < .35 or rnd.random() < .04)
    if glitch:
        r, g, b, a = img.split()
        img = Image.merge('RGBA', (ImageChops.offset(r, rnd.randint(4, 12), 0), g, ImageChops.offset(b, -rnd.randint(3, 9), 0), a))
        sl = img.copy(); y0 = rnd.randint(0, max(1, img.height - 20)); hh = rnd.randint(6, 22)
        band = sl.crop((0, y0, img.width, y0 + hh)); img.paste(band, (rnd.randint(-24, 24), y0), band)
    if alpha < 1: img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * alpha)))
    cx = W / 2 - 24 + it['x'] + ox; cy = it['y'] + oy
    pos = (int(cx - img.width / 2), int(cy - img.height / 2))
    if 'ghost' in fx:
        gh = img.copy(); r, g, b, a = gh.split()
        gh = Image.merge('RGBA', (r.point(lambda v: 200), g.point(lambda v: 0), b.point(lambda v: 0), a.point(lambda v: int(v * .28))))
        drift = int(6 + 4 * abs(((t * 3) % 2) - 1))
        fr.alpha_composite(gh, (pos[0] + drift, pos[1] - drift // 2))
    fr.alpha_composite(img, pos)
    return fr

def main():
    os.makedirs(OUT, exist_ok=True)
    raw = {k: Image.open(f'{SRC}/{f}.jpg').convert('RGB') for k, f in
           [('orbit', 'PIA23376'), ('deck', 'PIA22871'), ('crater', 'PIA25408'), ('selfie', 'PIA22876')]}
    im = {k: grade(v) for k, v in raw.items()}
    crater_bg = cover(im['crater']).filter(ImageFilter.GaussianBlur(30)).point(lambda v: v * .3)
    vig = vignette()
    rnd = random.Random(7)
    grain = [Image.effect_noise((W, H), 40).convert('RGB') for _ in range(6)]
    hud_f = font(F_UI, 22)
    for lang in ['ja', 'en']:
        caps = cap(lang); silent = f'{OUT}/_v_{lang}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '25',
                               '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
        for n in range(int(TOTAL * FPS)):
            t = n / FPS
            a, b, key = next(s for s in SC if s[0] <= t < s[1])
            p = (t - a) / (b - a)
            if key == 'orbit': fr = cover(im['orbit'], .512, .476, 1 + 1.8 * p)
            elif key == 'deck': fr = cover(im['deck'], .5, .45, 1.05 + .15 * p)
            elif key == 'crater': fr = fitwide(im['crater'], crater_bg, 1 + .2 * p)
            elif key == 'selfie': fr = cover(im['selfie'], .52, .42, 1.1 + .9 * p * p)
            else: fr = Image.new('RGB', (W, H), (4, 4, 6))
            if key:  # fade in/out, flicker
                k = min(1, (t - a) / .35) * (1 - max(0, (t - (b - .25)) / .25))
                if rnd.random() < .06: k *= .55
                fr = Image.blend(Image.new('RGB', (W, H)), fr, max(0, min(1, k)))
            # hits: shake, red flash, colour split
            hit = max([max(0, 1 - (t - x) / .35) for x in HITS + [STING] if t >= x] + [0])
            if hit > 0:
                dx, dy = rnd.randint(-14, 14) * hit, rnd.randint(-14, 14) * hit
                fr = ImageChops.offset(fr, int(dx), int(dy))
                r, g, bb = fr.split(); fr = Image.merge('RGB', (ImageChops.offset(r, int(10 * hit), 0), g, bb))
                fr = Image.blend(fr, Image.new('RGB', (W, H), (120, 0, 0)), .45 * hit)
            fr = Image.blend(fr, grain[n % len(grain)], .07)
            fr = Image.alpha_composite(fr.convert('RGBA'), vig)
            if key:  # found-footage HUD
                d = ImageDraw.Draw(fr)
                if (n // 15) % 2 == 0: d.ellipse((34, 150, 50, 166), fill=(220, 20, 20, 255))
                d.text((58, 158), 'REC', font=hud_f, fill=(230, 230, 230, 230), anchor='lm')
                d.text((W - 34, 158), 'INSIGHT / ELYSIUM PLANITIA', font=hud_f, fill=(230, 230, 230, 200), anchor='rm')
            for it in caps: fr = draw_caption(fr, it, t, rnd)
            fr = fr.convert('RGB')
            ff.stdin.write(fr.tobytes())
            if n == int(1.6 * FPS): fr.save(f'{OUT}/kaidan1.poster.{lang}.jpg', quality=82)
        ff.stdin.close(); ff.wait()
        # ---- audio ----
        T = TOTAL
        fc = ';'.join([
          f"[1:a]atrim={BLOOP_AT}:{BLOOP_AT + BLOOP_LEN},asetpts=PTS-STARTPTS,afade=t=out:st={BLOOP_LEN - 0.5}:d=0.5,asplit=2[b1][b4]",
          f"[b1]adelay={int(B1 * 1000)}:all=1[x1]", f"[b4]adelay={int(B4 * 1000)}:all=1[x4]",
          f"[2:a]atrim=1:{1 + 11.4 - 7.5},asetpts=PTS-STARTPTS,volume=24dB,afade=t=in:d=0.6,adelay=7500:all=1[w]",
          # drone: two low sines + brown noise, silent during the drops
          f"sine=f=98:d={T},volume=0.09,tremolo=f=0.4:d=0.6[s1]", f"sine=f=138.6:d={T},volume=0.05,tremolo=f=0.27:d=0.7[s2]",
          f"anoisesrc=d={T}:c=brown:a=0.35,lowpass=f=600[nz]",
          f"[s1][s2][nz]amix=inputs=3:normalize=0,afade=t=in:d=2,"
          f"volume=enable='between(t,11.4,12.6)+between(t,26.0,26.6)':volume=0,afade=t=out:st={T - 2}:d=2[dr]",
          # riser before the reveal, cut at the hit
          f"anoisesrc=d={STING - 21.5}:c=pink:a=0.6,highpass=f=800,afade=t=in:d={STING - 21.5}:curve=tri,adelay=21500:all=1[rs]",
          # hit: low boom + noise burst
          f"sine=f=72:d=2.2,volume=1.0,afade=t=out:d=2.2:curve=exp,adelay={int(STING * 1000)}:all=1[bm]",
          f"anoisesrc=d=0.5:c=white:a=0.9,lowpass=f=1800,afade=t=out:d=0.5,adelay={int(STING * 1000)}:all=1[bz]",
          f"[x1][x4][w][dr][rs][bm][bz]amix=inputs=7:normalize=0:duration=longest,alimiter=limit=0.95,apad=whole_dur={T},aresample=44100[a]",
        ])
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', f'{SRC}/meteor.mp4', '-i', f'{SRC}/quake.mp4',
                        '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '112k',
                        '-ac', '2', '-t', str(T), '-movflags', '+faststart', f'{OUT}/kaidan1.{lang}.mp4'], check=True)
        os.remove(silent)
        print('built', lang, flush=True)

main()
