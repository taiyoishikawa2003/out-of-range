#!/usr/bin/env python3
"""Publish motion videos into data/posts.json: python3 tools/motion/publish.py  (run from the repo root, after build.mjs).
Post metadata (caption, pinned comment, sources) comes from tools/slides/p_*.py so it lives in one place."""
import sys, os, json, importlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'slides'))
import lib
SFX = {'kind': {'en': 'Sound effect', 'ja': '効果音'}, 'title': 'Interface sounds: synthesized by the team (tools/motion/make_sfx.py, no third-party audio)', 'url': 'https://github.com/taiyoishikawa2003/out-of-range'}
# module -> (video base path, sound label, extra music credits, insert after post id)
V = {
 'p_surveyor': ('media/surveyor/pov', ('Kevin MacLeod「Gymnopedie No. 1」「Carefree」「Wholesome」(CC BY 4.0)', 'Kevin MacLeod – Gymnopedie No. 1 / Carefree / Wholesome (CC BY 4.0)'), ['Wholesome'], None),
 'p_pioneer': ('media/pioneer/navi', None, [], None),
 'p_near': ('media/near/chat', ('Kevin MacLeod「Sneaky Snitch」「Carefree」(CC BY 4.0)', 'Kevin MacLeod – Sneaky Snitch / Carefree (CC BY 4.0)'), ['Carefree'], None),
 'p_ranking': ('media/ranking/top5', ('Kevin MacLeod「Hyperfun」「Wholesome」(CC BY 4.0)', 'Kevin MacLeod – Hyperfun / Wholesome (CC BY 4.0)'), ['Wholesome'], None),
 'p_oppy': ('media/opportunity/unread', None, [], 'runway-looks-1'),
 'p_phoenix': ('media/phoenix/spot', None, [], None),
 'p_dawn': ('media/dawn/grind', None, [], None),
 'p_sojourner': ('media/sojourner/vlog', None, [], None),
}
P = 'data/posts.json'; posts = json.load(open(P))
for name in (sys.argv[1:] or V):
    base, sound, extra, after = V[name]
    if not os.path.exists(f'{base}.ja.mp4'): print('skip (not built yet):', name); continue
    post = dict(importlib.import_module(name).POST); post.pop('audio', None)
    post.update({'type': 'video', 'video': {'src': {l: f'{base}.{l}.mp4' for l in ('ja', 'en')}, 'poster': {l: f'{base}.poster.{l}.jpg' for l in ('ja', 'en')}, 'fit': 'contain'}, 'stats': {'likes': 0, 'saves': 0}})
    if sound: post['sound'] = {'ja': sound[0], 'en': sound[1]}
    have = ' '.join(s['title'] for s in post['sources'])
    post['sources'] = post['sources'] + [lib.music(t) for t in extra if f'"{t}"' not in have] + [SFX]
    idx = next((k for k, x in enumerate(posts) if x['id'] == post['id']), None)
    if idx is not None: posts[idx] = post
    else:
        k = next((k for k, x in enumerate(posts) if x['id'] == after), len(posts) - 1); posts.insert(k + 1, post)
    print('published', post['id'])
json.dump(posts, open(P, 'w'), ensure_ascii=False, indent=1)
