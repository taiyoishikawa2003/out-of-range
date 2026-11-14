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
W, H, FPS = 1080, 1920, 30
S = W / 720                      # layout below is written for 720 px wide; scale it up
TOTAL = 31.0
F_JA = ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc', 0)
F_EN = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 0)
F_UI = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc', 0)
BLOOP_AT, BLOOP_LEN, PEAKS = 57.70, 3.0, [0.15, 1.40, 1.65]  # impact sound inside the NASA video
B1, B4 = 0.2, 12.6                                          # where the impact sound is placed
HITS = [B1 + x for x in PEAKS] + [B4 + x for x in PEAKS]
STING = 24.0                                                # synth hit on "no microphone"

# scenes: (start, end, image or None)
SC = [(0, 3.2, 'sunset'), (3.2, 7.5, 'orbit'), (7.5, 11.4, 'deck'), (11.4, 17.0, 'scope'),
      (17.0, 21.5, 'crater'), (21.5, 26.0, 'selfie'), (26.0, TOTAL, 'dome')]
HEART = [21.7, 22.5, 23.2, 23.8]                           # heartbeats under the riser (team-made)

# captions: (start, end, [(y, size, [(appear_time, text, red), ...]), ...])  one tuple list = one line
def cap(lang):
    if lang == 'ja':
        return [
          (0.0, 3.2, [(190, 26, [(0.0, '※イヤホン推奨', 0)]),
                      (640, 64, [(0.3, 'これ、', 0), (0.75, '火星', 1), (1.0, 'で', 0)]),
                      (730, 64, [(1.3, '録れた音。', 0)])]),
          (3.2, 7.5, [(640, 56, [(3.6, 'まわりに', 0), (4.0, '誰もいない。', 0)]),
                      (740, 56, [(5.3, 'いるのは', 0)]),
                      (830, 56, [(5.8, 'この機械', 0), (6.3, '1台だけ。', 1)])]),
          (7.5, 11.4, [(640, 56, [(7.9, 'ずっと', 0), (8.3, '風の音だけ。', 0)]),
                       (740, 56, [(9.8, '……の', 0), (10.3, 'はずだった。', 1)])]),
          (11.4, 17.0, [(640, 84, [(HITS[3], 'ボッ', 0), (HITS[4], 'ボッ', 0), (HITS[5], 'ボッ', 1)]),
                        (780, 44, [(15.4, '3回、鳴った。', 0)])]),
          (17.0, 21.5, [(250, 52, [(17.3, 'あとで', 0), (17.7, '上から見たら', 0)]),
                        (350, 52, [(18.8, '地面に', 0), (19.2, '黒い穴', 1), (19.6, 'が増えてた。', 0)])]),
          (21.5, 26.0, [(560, 56, [(21.9, '……待って。', 0)]),
                        (680, 66, [(23.2, 'こいつ、', 0), (STING, 'マイク', 1), (24.4, 'が', 0)]),
                        (780, 66, [(24.7, 'ついてない。', 0)])]),
          (26.0, TOTAL, [(170, 22, [(26.0, '素材：NASA/JPL-Caltech ほか　効果音：チーム制作', 0)]),
                         (610, 70, [(26.5, 'じゃあ、', 0), (27.1, '何で', 1)]),
                         (710, 70, [(27.6, '聞いたの？', 0)]),
                         (830, 34, [(29.0, '答えはコメ欄', 0)])]),
        ]
    return [
          (0.0, 3.2, [(190, 26, [(0.0, '(headphones on)', 0)]),
                      (640, 60, [(0.3, 'This', 0), (0.6, 'was', 0), (0.85, 'recorded', 0)]),
                      (730, 60, [(1.3, 'on', 0), (1.5, 'Mars.', 1)])]),
          (3.2, 7.5, [(640, 56, [(3.6, 'No one', 0), (4.0, 'around.', 0)]),
                      (740, 56, [(5.3, 'Just', 0), (5.8, 'this machine.', 1)])]),
          (7.5, 11.4, [(640, 56, [(7.9, 'Only', 0), (8.3, 'the wind.', 0)]),
                       (740, 56, [(9.8, 'Or so', 0), (10.3, 'we thought.', 1)])]),
          (11.4, 17.0, [(640, 60, [(HITS[3], 'bloop', 0), (HITS[4], 'bloop', 0), (HITS[5], 'bloop', 1)]),
                        (780, 44, [(15.4, '3 times.', 0)])]),
          (17.0, 21.5, [(250, 50, [(17.3, 'Later,', 0), (17.7, 'from above:', 0)]),
                        (350, 50, [(18.8, 'new', 0), (19.2, 'holes', 1), (19.6, 'in the ground.', 0)])]),
          (21.5, 26.0, [(560, 56, [(21.9, '...wait.', 0)]),
                        (680, 64, [(23.2, 'It has', 0), (STING, 'no', 1)]),
                        (780, 64, [(24.4, 'microphone.', 1)])]),
          (26.0, TOTAL, [(170, 22, [(26.0, 'Media: NASA/JPL-Caltech et al.  SFX: our team', 0)]),
                         (610, 66, [(26.5, 'So', 0), (27.1, 'how', 1)]),
                         (710, 66, [(27.6, 'did it hear that?', 0)]),
                         (830, 34, [(29.0, 'Answer in the comments', 0)])]),
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
    out.paste(img.resize((w, h), Image.LANCZOS), ((W - w) // 2, (H - h) // 2 + int(60 * S)))
    return out

def vignette():
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse((-W * .35, -H * .2, W * 1.35, H * 1.2), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(240))
    return Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [ImageChops.invert(m).point(lambda v: v * .95)])

_cache = {}
def caption_layer(lang, ci, lines, t):
    vis = tuple(sum(1 for (tt, _, _) in ch if t >= tt) for (_, _, ch) in lines)
    key = (lang, ci, vis)
    if key in _cache: return _cache[key]
    lay = Image.new('RGBA', (W, H)); sh = Image.new('RGBA', (W, H))
    dl, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    for (y, sz, ch), n in zip(lines, vis):
        if not n: continue
        f = font(F_UI if sz < 30 else (F_JA if lang == 'ja' else F_EN), int(sz * S)); y = y * S
        sep = '' if lang == 'ja' else ' '
        widths = [dl.textlength(tx, font=f) for _, tx, _ in ch]
        x = (W - 48 * S - (sum(widths) + dl.textlength(sep, font=f) * (len(ch) - 1))) / 2
        for k, ((_, tx, red), w) in enumerate(zip(ch, widths)):
            if k < n:
                col = RED if red else ((200, 200, 200) if sz < 30 else (240, 240, 240))
                ds.text((x + 3, y + 4), tx, font=f, fill=(0, 0, 0, 255), anchor='lm')
                dl.text((x, y), tx, font=f, fill=col + (255,), anchor='lm')
            x += w + dl.textlength(sep, font=f)
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.alpha_composite(sh, Image.alpha_composite(sh, lay))
    _cache[key] = out
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    raw = {k: Image.open(f'{SRC}/hi/{f}.jpg').convert('RGB') for k, f in
           [('orbit', 'PIA23376'), ('deck', 'PIA22871'), ('crater', 'PIA25408'), ('selfie', 'PIA22876'),
            ('sunset', 'PIA23202'), ('dome', 'PIA23177')]}
    im = {k: grade(v) for k, v in raw.items()}
    crater_bg = cover(im['crater']).filter(ImageFilter.GaussianBlur(30)).point(lambda v: v * .3)
    vig = vignette()
    rnd = random.Random(7)
    grain = [Image.effect_noise((W, H), 40).convert('RGB') for _ in range(6)]
    hud_f = font(F_UI, int(22 * S))
    # the real impact sound as a waveform (drawn like an oscilloscope while it plays)
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(BLOOP_AT), '-t', str(BLOOP_LEN), '-i', f'{SRC}/meteor.mp4', '-ac', '1', '-ar', '8000',
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    import array; wav = array.array('h', pcm); peak = max(1, max(abs(v) for v in wav))
    wav = [v / peak for v in wav]
    for lang in ['ja', 'en']:
        caps = cap(lang); silent = f'{OUT}/_v_{lang}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
                               '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
        for n in range(int(TOTAL * FPS)):
            t = n / FPS
            a, b, key = next(s for s in SC if s[0] <= t < s[1])
            p = (t - a) / (b - a)
            if key == 'orbit': fr = cover(im['orbit'], .512, .476, 1 + 1.8 * p)
            elif key == 'deck': fr = cover(im['deck'], .5, .45, 1.05 + .15 * p)
            elif key == 'crater': fr = fitwide(im['crater'], crater_bg, 1 + .2 * p)
            elif key == 'selfie': fr = cover(im['selfie'], .52, .42, 1.1 + .9 * p * p)
            elif key == 'sunset': fr = ImageEnhance.Brightness(cover(im['sunset'], .5, .55, 1.2 + .25 * p)).enhance(.75)
            elif key == 'dome': fr = ImageEnhance.Brightness(cover(im['dome'], .5, .5, 1.15 + .3 * p)).enhance(.45 * min(1, (t - a) / 2.0))
            else: fr = Image.new('RGB', (W, H), (4, 4, 6))
            if key == 'scope' and t >= B4:   # oscilloscope of the real signal, revealed as it plays
                d = ImageDraw.Draw(fr); cy, amp = int(H * .31), int(120 * S); pos = min(1, (t - B4) / BLOOP_LEN)
                for gx in range(0, W, int(60 * S)): d.line((gx, cy - amp, gx, cy + amp), fill=(22, 22, 26))
                d.line((0, cy, W, cy), fill=(40, 40, 46), width=2)
                N = int(len(wav) * pos); step = max(1, len(wav) // W)
                pts = [(i * W / (len(wav) / step), cy - wav[i * step] * amp) for i in range(N // step)]
                if len(pts) > 1:
                    d.line(pts, fill=(200, 30, 30), width=max(2, int(2 * S)))
                    gl = Image.new('RGB', (W, H)); ImageDraw.Draw(gl).line(pts, fill=(255, 40, 40), width=int(8 * S))
                    fr = ImageChops.add(fr, gl.filter(ImageFilter.GaussianBlur(10 * S)).point(lambda v: v * .5))
            if key and key != 'scope':  # fade in/out, flicker
                k = min(1, (t - a) / .35) * (1 - max(0, (t - (b - .25)) / .25))
                if rnd.random() < .06: k *= .55
                fr = Image.blend(Image.new('RGB', (W, H)), fr, max(0, min(1, k)))
            # hits: shake, red flash, colour split
            hit = max([max(0, 1 - (t - x) / .35) for x in HITS + [STING] if t >= x] + [0])
            if hit > 0:
                dx, dy = rnd.randint(-14, 14) * hit * S, rnd.randint(-14, 14) * hit * S
                fr = ImageChops.offset(fr, int(dx), int(dy))
                r, g, bb = fr.split(); fr = Image.merge('RGB', (ImageChops.offset(r, int(10 * hit * S), 0), g, bb))
                for _ in range(int(6 * hit)):   # glitch: shift a few horizontal slices
                    y0 = rnd.randint(0, H - 80); hh = rnd.randint(8, 70); sl = fr.crop((0, y0, W, y0 + hh))
                    fr.paste(ImageChops.offset(sl, rnd.randint(-60, 60), 0), (0, y0))
                fr = Image.blend(fr, Image.new('RGB', (W, H), (120, 0, 0)), .45 * hit)
            fr = Image.blend(fr, grain[n % len(grain)], .07)
            fr = Image.alpha_composite(fr.convert('RGBA'), vig)
            if key not in (None, 'scope', 'dome', 'sunset'):  # found-footage HUD
                d = ImageDraw.Draw(fr)
                if (n // 15) % 2 == 0: d.ellipse((34 * S, 150 * S, 50 * S, 166 * S), fill=(220, 20, 20, 255))
                d.text((58 * S, 158 * S), 'REC', font=hud_f, fill=(230, 230, 230, 230), anchor='lm')
                d.text((W - 34 * S - 110, 158 * S), 'INSIGHT / ELYSIUM PLANITIA', font=hud_f, fill=(230, 230, 230, 200), anchor='rm')
            for ci, (ca, cb, lines) in enumerate(caps):
                if ca <= t < cb: fr = Image.alpha_composite(fr, caption_layer(lang, ci, lines, t))
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
          # heartbeat: two soft low thumps per beat
          *[f"sine=f=55:d=0.18,volume=0.9,afade=t=out:d=0.18:curve=exp,adelay={int((h + dt) * 1000)}:all=1[hb{i}{j}]"
            for i, h in enumerate(HEART) for j, dt in enumerate((0, 0.22))],
          f"[x1][x4][w][dr][rs][bm][bz]" + ''.join(f'[hb{i}{j}]' for i in range(len(HEART)) for j in range(2)) +
          f"amix=inputs={7 + 2 * len(HEART)}:normalize=0:duration=longest,alimiter=limit=0.95,apad=whole_dur={T},aresample=44100[a]",
        ])
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', f'{SRC}/meteor.mp4', '-i', f'{SRC}/quake.mp4',
                        '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                        '-ac', '2', '-t', str(T), '-movflags', '+faststart', f'{OUT}/kaidan1.{lang}.mp4'], check=True)
        os.remove(silent)
        print('built', lang, flush=True)

main()
