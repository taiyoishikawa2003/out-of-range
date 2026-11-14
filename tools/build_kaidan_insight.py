#!/usr/bin/env python3
"""Build the "InSight kaidan Part 1" video (ja / en) from NASA media.

Source media (download with the URLs in data/posts.json sources) go in SRC.
Frames are drawn with Pillow and piped to ffmpeg; audio is mixed with ffmpeg.
Usage: python3 tools/build_kaidan_insight.py <src_dir> <out_dir>
"""
import math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 720, 1280, 30
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
BLOOP_AT = 57.70           # start of the impact sound inside the NASA video
BLOOP_LEN = 3.0
PEAKS = [0.15, 1.40, 1.65] # the three "bloops", seconds after BLOOP_AT

# slide: (start, end, background, texts)
S = dict(s1=(0, 3.5), s2=(3.5, 8.5), s3=(8.5, 15.5), s4=(15.5, 21.5),
         s5=(21.5, 26.5), s6=(26.5, 33.5), s7=(33.5, 40.5), s8=(40.5, 44.5), s9=(44.5, 48.5))
TOTAL = 48.5
B1, B4, B5 = 0.3, 17.0, 22.5  # bloop clip placements

TXT = {
  'ja': {
    's1': '2021年9月5日。\n誰もいない火星で、\n音が3回鳴った。',
    's2': 'そこにいたのは、\n機械が1台だけ。',
    's3': 'ずっと、\n風の音がしていた。',
    's4': '……',
    'bloop': '……ボッ。',
    's5': 'もう一度。',
    's6': 'そのあと、上から見ると\n地面に黒い穴が\n増えていた。',
    's7a': 'でも、おかしい。',
    's7b': 'この機械には、\nマイクが\n付いていない。',
    's8': '意味、わかった？',
    's8s': '答えはコメント欄に',
    's9': '素材：NASA/JPL-Caltech ほか\n\n音：NASAが観測データから作った音\n（風の音は60倍速）\n\n穴の写真：MRO HiRISE\n\n出典はアプリの「出典」から',
  },
  'en': {
    's1': 'Sept 5, 2021.\nNo one was on Mars.\nSomething made a sound.\n3 times.',
    's2': 'The only one there\nwas a machine.',
    's3': 'The wind\nnever stopped.',
    's4': '...',
    'bloop': '...bloop.',
    's5': 'One more time.',
    's6': 'Later, seen from above,\nnew dark holes\nhad appeared.',
    's7a': "But here's the creepy part.",
    's7b': 'This machine\nhas no\nmicrophone.',
    's8': 'Did you get it?',
    's8s': 'Answer in the comments',
    's9': 'Media: NASA/JPL-Caltech et al.\n\nSounds made by NASA\nfrom mission data\n(wind sped up 60x)\n\nCraters: MRO HiRISE\n\nSources: tap "Sources"',
  },
}

def font(sz): return ImageFont.truetype(FONT, sz, index=0)

def cover(img, cx=None, cy=None, zoom=1.0):
    """Crop img to 9:16 around (cx,cy) (fractions), then zoom in."""
    iw, ih = img.size
    tw = min(iw, ih * W / H); th = tw * H / W
    tw /= zoom; th /= zoom
    cx = (cx if cx is not None else .5) * iw; cy = (cy if cy is not None else .5) * ih
    x0 = min(max(cx - tw / 2, 0), iw - tw); y0 = min(max(cy - th / 2, 0), ih - th)
    return img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + tw, y0 + th))

def fitwide(img, zoom=1.0):
    """Whole landscape image on a blurred, darkened copy of itself."""
    bg = cover(img).filter(ImageFilter.GaussianBlur(30)).point(lambda v: v * .35)
    iw, ih = img.size; w = int(W * zoom); h = int(ih * w / iw)
    fg = img.resize((w, h), Image.LANCZOS)
    bg.paste(fg, ((W - w) // 2, (H - h) // 2 - 40))
    return bg

def text(draw, s, y, sz, alpha=255, fill=(255, 255, 255)):
    f = font(sz); lines = s.split('\n'); lh = int(sz * 1.35)
    y0 = y - lh * len(lines) / 2
    for i, ln in enumerate(lines):
        w = draw.textlength(ln, font=f)
        draw.text(((W - w) / 2, y0 + i * lh), ln, font=f, fill=fill + (alpha,),
                  stroke_width=max(3, sz // 12), stroke_fill=(0, 0, 0, alpha))

def ease(t, a, b): return max(0., min(1., (t - a) / max(b - a, 1e-6)))

def main():
    os.makedirs(OUT, exist_ok=True)
    im = {k: Image.open(f'{SRC}/{k}.jpg').convert('RGB') for k in ['PIA23376', 'PIA22871', 'PIA25408', 'PIA22876']}
    for lang in ['ja', 'en']:
        T = TXT[lang]; silent = f'{OUT}/_v_{lang}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '26',
                               '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
        for n in range(int(TOTAL * FPS)):
            t = n / FPS
            def p(k): a, b = S[k]; return (t - a) / (b - a)
            if S['s2'][0] <= t < S['s2'][1]:      # orbit view, slow push in on the lander
                fr = cover(im['PIA23376'], .512, .476, 1 + 1.6 * p('s2'))
            elif S['s3'][0] <= t < S['s3'][1]:
                fr = cover(im['PIA22871'], .5, .5, 1 + .12 * p('s3'))
            elif S['s6'][0] <= t < S['s6'][1]:
                fr = fitwide(im['PIA25408'], 1 + .25 * p('s6'))
            elif S['s7'][0] <= t < S['s7'][1]:
                fr = cover(im['PIA22876'], .5, .55, 1 + .5 * p('s7'))
            else:
                fr = Image.new('RGB', (W, H), (0, 0, 0))
            # fade from/to black at each slide boundary
            for k, (a, b) in S.items():
                if a <= t < b and k in ('s2', 's3', 's6', 's7'):
                    fr = Image.blend(Image.new('RGB', (W, H)), fr, min(ease(t, a, a + .5), 1 - ease(t, b - .4, b)))
            ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
            if t < S['s1'][1]: text(d, T['s1'], 560, 54)
            elif t < S['s2'][1]: text(d, T['s2'], 560, 56, int(255 * ease(t, 4.0, 4.4)))
            elif t < S['s3'][1]: text(d, T['s3'], 560, 58, int(255 * ease(t, 9.5, 9.9)))
            elif t < S['s5'][1]:
                hits = [B4 + x for x in PEAKS] if t < S['s4'][1] else [B5 + x for x in PEAKS]
                k = sum(1 for x in hits if t >= x)
                if t >= S['s5'][0]: text(d, T['s5'], 380, 46, int(255 * ease(t, 21.6, 22.0)), (200, 200, 200))
                if k == 0 and t < S['s4'][1]: text(d, T['s4'], 560, 70)
                if k:
                    flash = max(0., 1 - (t - hits[k - 1]) / .6)
                    text(d, T['bloop'], 560, int(70 + 30 * flash))
                    text(d, f'{k}/3', 760, 64, 255, (255, 176, 0))
            elif t < S['s6'][1]: text(d, T['s6'], 300, 50, int(255 * ease(t, 27.3, 27.8)))
            elif t < S['s7'][1]:
                text(d, T['s7a'], 300, 50, int(255 * ease(t, 34.0, 34.4)))
                text(d, T['s7b'], 620, 66, int(255 * ease(t, 36.3, 36.5)))
            elif t < S['s8'][1]:
                text(d, T['s8'], 560, 72, int(255 * ease(t, 40.8, 41.3)))
                text(d, T['s8s'], 700, 36, int(255 * ease(t, 42.0, 42.5)), (255, 176, 0))
            else:
                text(d, T['s9'], 600, 32, int(255 * ease(t, 44.6, 45.0)), (220, 220, 220))
            fr = Image.alpha_composite(fr.convert('RGBA'), ov).convert('RGB')
            ff.stdin.write(fr.tobytes())
            if lang == 'ja' and n == int(2.5 * FPS): fr.save(f'{OUT}/kaidan1.poster.ja.jpg', quality=82)
            if lang == 'en' and n == int(2.5 * FPS): fr.save(f'{OUT}/kaidan1.poster.en.jpg', quality=82)
        ff.stdin.close(); ff.wait()
        # audio: three placements of the impact sound, wind on slide 3, low drone on slide 6
        a3, b3 = S['s3']; a6, b6 = S['s6']
        fc = (f"[1:a]atrim={BLOOP_AT}:{BLOOP_AT + BLOOP_LEN},asetpts=PTS-STARTPTS,afade=t=out:st={BLOOP_LEN - .5}:d=0.5,asplit=3[b1][b4][b5];"
              f"[b1]adelay={int(B1 * 1000)}:all=1[x1];[b4]adelay={int(B4 * 1000)}:all=1[x4];[b5]adelay={int(B5 * 1000)}:all=1[x5];"
              f"[2:a]atrim=1:{1 + b3 - a3},asetpts=PTS-STARTPTS,volume=24dB,afade=t=in:d=0.8,afade=t=out:st={b3 - a3 - .8}:d=0.8,adelay={int(a3 * 1000)}:all=1[w];"
              f"sine=f=55:d={b6 - a6},volume=0.05,afade=t=in:d=1.5,afade=t=out:st={b6 - a6 - 1}:d=1,adelay={int(a6 * 1000)}:all=1[dr];"
              f"[x1][x4][x5][w][dr]amix=inputs=5:normalize=0:duration=longest,apad=whole_dur={TOTAL},aresample=44100[a]")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', f'{SRC}/meteor.mp4', '-i', f'{SRC}/quake.mp4',
                        '-filter_complex', fc,
                        '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', '-ac', '2',
                        '-t', str(TOTAL), '-movflags', '+faststart', f'{OUT}/kaidan1.{lang}.mp4'], check=True)
        os.remove(silent)
        print('built', lang)

main()
