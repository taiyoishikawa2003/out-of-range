#!/usr/bin/env python3
"""Build photo posts: python3 tools/slides/build.py [post_module ...]   (run from the repo root)
Renders slides (ja/en) with headless Chrome and upserts each post into data/posts.json."""
import sys, os, json, subprocess, importlib, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
ALL = ['p_surveyor', 'p_viking', 'p_pioneer', 'p_near', 'p_runway', 'p_ranking', 'p_viking2', 'p_pioneer11', 'p_lrv', 'p_aruaru']
mods = sys.argv[1:] or ALL
P = 'data/posts.json'; posts = json.load(open(P))
for name in mods:
    m = importlib.import_module(name); post = dict(m.POST); d = f"media/{m.DIR}"; os.makedirs(d, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for lang in ('ja', 'en'):
        lib.setlang(lang)
        for i, s in enumerate(m.SLIDES, 1):
            open(f'{tmp}/{i}.{lang}.html', 'w').write(lib.page(s['html'](), getattr(m, 'CSS', '')))
    subprocess.run(['node', os.path.join(lib.HERE, 'render.mjs'), tmp], check=True)
    slides = []
    for i, s in enumerate(m.SLIDES, 1):
        for lang in ('ja', 'en'): shutil.copy(f'{tmp}/{i}.{lang}.jpg', f'{d}/{i}.{lang}.jpg')
        e = {'bg': {'ja': f'{d}/{i}.ja.jpg', 'en': f'{d}/{i}.en.jpg'}, 'alt': s['alt'], 'dur': s.get('dur', 4)}
        for k in ('quiz', 'music', 'sfx'):
            if k in s: e[k] = s[k]
        slides.append(e)
    post.update({'type': 'carousel', 'slides': slides, 'noSourceSlide': True, 'fit': 'contain', 'stats': {'likes': 0, 'saves': 0}})
    idx = next((k for k, x in enumerate(posts) if x['id'] == post['id']), None)
    if idx is None: posts.append(post)
    else: posts[idx] = post
    shutil.rmtree(tmp); print('built', post['id'], len(slides), 'slides')
json.dump(posts, open(P, 'w'), ensure_ascii=False, indent=1)
