#!/usr/bin/env python3
"""Write the wording in tools/texts.py into data/posts.json and data/accounts.json, and put the feed in order.

Safe to run again and again. Run it after tools/slides/build.py or tools/motion/publish.py,
because those rebuild a post from its own module and would bring old wording back.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from texts import ACCOUNTS, POSTS, ORDER, LIKES

ROOT = pathlib.Path(__file__).resolve().parent.parent
PJ, AJ = ROOT / 'data/posts.json', ROOT / 'data/accounts.json'
posts = json.loads(PJ.read_text())
accounts = json.loads(AJ.read_text())
FACT = {'en': 'Fact check', 'ja': '事実確認'}
problems = []

# ---- accounts ----
for handle, a in ACCOUNTS.items():
    acc = accounts.setdefault(handle, {})
    acc['kind'] = a['kind']
    acc['name'] = {'en': a['name'][1], 'ja': a['name'][0]}
    acc['bio'] = {'en': a['bio'][1], 'ja': a['bio'][0]}
    if a.get('since'):
        acc['since'] = {'en': a['since'][1], 'ja': a['since'][0]}
    else:
        acc.pop('since', None)
for handle, acc in accounts.items():
    if handle not in ACCOUNTS and not acc.get('hidden'):
        problems.append(f'account without text: {handle}')

# ---- posts ----
by_id = {p['id']: p for p in posts}
for pid, tx in POSTS.items():
    p = by_id.get(pid)
    if not p:
        problems.append(f'no such post: {pid}')
        continue
    if 'caption' in tx:
        p['caption'] = {'ja': tx['caption'][0], 'en': tx['caption'][1]}
    pinned = [c for c in p.get('comments', []) if c.get('pinned')]
    if 'pinned' in tx:
        pinned[0]['text'] = {'ja': tx['pinned'][0], 'en': tx['pinned'][1]}
    if 'head' in tx:
        for lang, new in zip(('ja', 'en'), tx['head']):
            lines = pinned[0]['text'][lang].split('\n')
            lines[0] = new
            pinned[0]['text'][lang] = '\n'.join(lines)
    for old, new in tx.get('sub', []):
        hit = False
        for lang in ('ja', 'en'):
            s = pinned[0]['text'][lang]
            if new in s:
                hit = True
            elif old in s:
                pinned[0]['text'][lang] = s.replace(old, new)
                hit = True
        if not hit:
            problems.append(f'{pid}: text to replace not found: {old[:40]}')
    if 'comments' in tx:
        rest, keep_src, add_src = [], set(), []
        for c in tx['comments']:
            user, ja, en = c[:3]
            opt = c[3] if len(c) > 3 else {}
            if user not in accounts:
                problems.append(f'{pid}: comment from unknown account {user}')
            rest.append({'user': user, 'text': {'ja': ja, 'en': en}})
            if opt.get('fact', True):
                keep_src.add(user)
            for title, url in opt.get('src', []):
                add_src.append({'kind': dict(FACT), 'title': f"For @{user}'s comment: {title}", 'url': url})
        p['comments'] = pinned + rest
        # sources added for a comment stay only while that comment still states a fact
        def keep(s):
            t = s.get('title')
            if not isinstance(t, str) or not t.startswith('For @'):
                return True
            return t[5:].split("'s comment")[0] in keep_src
        p['sources'] = [s for s in p.get('sources', []) if keep(s)]
        have = {s.get('title') for s in p['sources'] if isinstance(s.get('title'), str)}
        p['sources'] += [s for s in add_src if s['title'] not in have]

# ---- starting counts (staged) ----
fol = {}
for p in posts:
    n = LIKES.get(p['id'])
    if n is None:
        problems.append(f"no like count for {p['id']}"); continue
    p['stats'] = {**(p.get('stats') or {}), 'likes': n, 'saves': n // 9}
    fol[p['account']] = fol.get(p['account'], 0) + n
for handle, n in fol.items():
    if handle in accounts:
        accounts[handle]['followers'] = round(n * 0.4 / 10) * 10

# ---- order ----
missing = [i for i in ORDER if i not in by_id]
extra = [p['id'] for p in posts if p['id'] not in ORDER]
if missing:
    problems.append(f'ORDER names posts that do not exist: {missing}')
posts = [by_id[i] for i in ORDER if i in by_id] + [by_id[i] for i in extra]
if extra:
    print('not in ORDER (kept at the end):', extra)

if problems:
    print('\n'.join('PROBLEM: ' + x for x in problems))
    sys.exit(1)
PJ.write_text(json.dumps(posts, ensure_ascii=False, indent=1))
AJ.write_text(json.dumps(accounts, ensure_ascii=False, indent=1))
print(f'texts applied: {len(POSTS)} posts, {len(ACCOUNTS)} accounts; feed order: {len(posts)} posts')
