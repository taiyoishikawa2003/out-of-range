#!/usr/bin/env python3
"""preview.py <module> : render slides to /tmp/sl and make contact sheets /tmp/v/<module>_<lang>.jpg"""
import sys, os, subprocess, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from PIL import Image
for name in sys.argv[1:]:
    m = importlib.import_module(name); d = f'/tmp/sl_{name}'; os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(f'{d}/{f}')
    for lang in ('ja', 'en'):
        lib.setlang(lang)
        for i, s in enumerate(m.SLIDES, 1): open(f'{d}/{i}.{lang}.html', 'w').write(lib.page(s['html'](), getattr(m, 'CSS', '')))
    subprocess.run(['node', os.path.join(lib.HERE, 'render.mjs'), d], check=True)
    for lang in ('ja', 'en'):
        n = len(m.SLIDES); W = 330; H = 587; sh = Image.new('RGB', (n * W, H))
        for i in range(n): sh.paste(Image.open(f'{d}/{i+1}.{lang}.jpg').resize((W, H)), (i * W, 0))
        sh.save(f'/tmp/v/{name}_{lang}.jpg', quality=85)
