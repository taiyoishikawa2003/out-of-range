#!/usr/bin/env python3
"""Synthesize the short interface sounds used in motion videos (no third-party audio). Output: tools/motion/sfx/*.wav"""
import numpy as np, wave, os
SR = 44100; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx')
def save(name, x, gain=0.8):
    x = np.asarray(x, np.float64); x = x / (np.abs(x).max() + 1e-9) * gain
    st = np.stack([x, x], 1); w = wave.open(f'{OUT}/{name}.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
def t(d): return np.arange(int(SR * d)) / SR
def env(x, a=0.004, r=None):
    n = len(x); e = np.ones(n); na = max(1, int(SR * a)); e[:na] = np.linspace(0, 1, na)
    if r: nr = min(n, int(SR * r)); e[-nr:] *= np.linspace(1, 0, nr)
    return x * e
def sweep(f0, f1, d, shape=1.0):
    x = t(d); f = f0 + (f1 - f0) * (x / d) ** shape; return np.sin(2 * np.pi * np.cumsum(f) / SR)
rng = np.random.default_rng(7)
def noise(d): return rng.standard_normal(int(SR * d))
def lp(x, k):  # one-pole low-pass
    y = np.zeros_like(x); a = 0.0
    for i, v in enumerate(x): a += k * (v - a); y[i] = a
    return y
# pop: text box appears
x = t(0.09); save('pop', env(sweep(520, 900, 0.09) * np.exp(-x * 38), r=0.03), 0.55)
# msg: chat message received (two soft tones)
a = env(np.sin(2 * np.pi * 880 * t(0.07)) * np.exp(-t(0.07) * 30)); b = env(np.sin(2 * np.pi * 1175 * t(0.16)) * np.exp(-t(0.16) * 16))
save('msg', np.concatenate([a, np.zeros(int(SR * 0.02)), b]), 0.5)
# send: chat message sent (soft rising blip)
x = t(0.12); save('send', env(sweep(420, 980, 0.12, 0.6) * np.exp(-x * 20), r=0.04), 0.45)
# tick: typing / counter
x = t(0.018); save('tick', env(np.sin(2 * np.pi * 1900 * x) * np.exp(-x * 240)), 0.3)
# ding: reveal
x = t(0.9); save('ding', env((np.sin(2 * np.pi * 1318.5 * x) + 0.5 * np.sin(2 * np.pi * 1975.5 * x) + 0.25 * np.sin(2 * np.pi * 2637 * x)) * np.exp(-x * 5.5), r=0.2), 0.5)
# whoosh: scene change
x = noise(0.32); e = np.sin(np.pi * np.linspace(0, 1, len(x))) ** 2; save('whoosh', lp(x, 0.18) * e, 0.4)
# thud: heavy punchline
x = t(0.5); save('thud', env((sweep(120, 42, 0.5, 0.5) + 0.25 * lp(noise(0.5), 0.05)) * np.exp(-x * 9)), 0.9)
# riser: before a reveal
x = t(1.1); save('riser', env((sweep(220, 1250, 1.1, 2.0) * 0.6 + lp(noise(1.1), 0.3) * 0.5) * (x / 1.1) ** 2, r=0.02), 0.45)
# buzz: wrong / denied
x = t(0.28); save('buzz', env(np.sign(np.sin(2 * np.pi * 110 * x)) * 0.5 + np.sign(np.sin(2 * np.pi * 138 * x)) * 0.5, r=0.05), 0.3)
# chime: navigation instruction (three notes up)
parts = [env(np.sin(2 * np.pi * f * t(0.16)) * np.exp(-t(0.16) * 9), r=0.03) for f in (784, 988, 1175)]
save('chime', np.concatenate(parts), 0.5)
print(sorted(os.listdir(OUT)))
