#!/usr/bin/env python3
"""Team-made sound effects (synthesised, no samples): sad trombone, record scratch, reveal fanfare.
Usage: python3 tools/make_sfx.py <out_dir>
"""
import sys, os, subprocess, wave
import numpy as np

OUT = sys.argv[1]; SR = 44100
os.makedirs(OUT, exist_ok=True)

def brass(freq, dur, vib=0.0, bend=0.0, wah=False):
    t = np.arange(int(SR * dur)) / SR
    f = freq * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / dur * 2 - .4, 0, 1)) * (1 + bend * t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k ** (1.1 if not wah else 1.4) for k in range(1, 12))
    env = np.minimum(1, t / .04) * np.minimum(1, (dur - t) / .08)
    if wah:  # plunger "wah": brighten then darken
        bright = .5 + .5 * np.sin(np.pi * np.clip(t / (dur * .6), 0, 1))
        x = x * (.5 + .5 * bright)
    return x * env

def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * .85
    path = f'{OUT}/{name}.wav'
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-c:a', 'libmp3lame', '-b:a', '128k', f'{OUT}/{name}.mp3'], check=True)
    os.remove(path)

# sad trombone: G3 F#3 F3 E3(long, wobbling down)
notes = [(196.0, .42), (185.0, .42), (174.6, .42), (164.8, 1.4)]
seq = [brass(f, d, vib=.025 if i == 3 else 0, bend=-.06 if i == 3 else 0, wah=True) for i, (f, d) in enumerate(notes)]
gap = np.zeros(int(SR * .04))
save('sad_trombone', np.concatenate([np.concatenate([s, gap]) for s in seq]))

# record scratch: fast pitch-swept noise burst
t = np.arange(int(SR * .45)) / SR
noise = np.random.default_rng(1).standard_normal(len(t))
sweep = np.sin(2 * np.pi * np.cumsum(900 + 2600 * np.sin(2 * np.pi * 7 * t)) / SR)
scr = (noise * .35 + sweep) * np.exp(-t * 5) * np.minimum(1, t / .01)
save('record_scratch', scr)

# reveal: bright major brass chord + cymbal-ish noise swell
chord = sum(brass(f, 1.8) for f in (261.6, 329.6, 392.0, 523.3))
t = np.arange(len(chord)) / SR
cym = np.random.default_rng(2).standard_normal(len(t)); cym = np.diff(np.concatenate([[0], cym])) * np.exp(-t * 2.2) * .5
save('reveal', chord * np.exp(-t * .9) + cym)
print('ok')
