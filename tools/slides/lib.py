"""Shared helpers for building OUT OF RANGE photo posts.
Each post module defines POST (metadata for data/posts.json) and SLIDES (list of dicts:
  html: callable -> inner HTML for the current language, alt: {ja,en}, dur: seconds, plus optional quiz/music/sfx).
build.py renders every slide for ja/en to media/<dir>/<n>.<lang>.jpg and upserts the post into data/posts.json.
NASA photos are read from $OOR_ASSETS/<nasa_id>.jpg (download with tools/slides/fetch_nasa.py)."""
import os
ASSETS = os.environ.get('OOR_ASSETS', '/home/claude/assets')
HERE = os.path.dirname(os.path.abspath(__file__))
LANG = 'ja'
def setlang(l):
    global LANG; LANG = l
def t(ja, en): return ja if LANG == 'ja' else en
def bg(nid, pos='50% 50%', zoom=1, filt='', origin='50% 50%'):
    return f'<img class="bg" src="file://{ASSETS}/{nid}.jpg" style="object-position:{pos};transform:scale({zoom});transform-origin:{origin};filter:{filt or "none"}">'
def shade(kind='top'): return f'<div class="shade {kind}"></div>'
def tag(ja, en, cls=''): return f'<div class="tag {cls}">{t(ja, en)}</div>'
def h(ja, en, cls=''): return f'<div class="h {cls}">{t(ja, en)}</div>'
def bx(ja, en, cls=''): return f'<div class="bxw"><span class="bx {cls}">{t(ja, en)}</span></div>'
def col(*kids, cls='', style=''): return f'<div class="col {cls}" style="{style}">' + ''.join(k for k in kids if k) + '</div>'
def cr(ja, en): return f'<div class="cr">{t(ja, en)}</div>'
def page(inner, css=''):
    return (f'<!doctype html><html lang="{LANG}"><meta charset="utf-8"><link rel="stylesheet" href="file://{HERE}/slides.css">'
            f'<style>{css}</style><body class="{LANG}"><div class="s">{inner}</div></body></html>')
def src(kind, title, url):
    K = {'img': {'en': 'Image', 'ja': '画像'}, 'fact': {'en': 'Fact check', 'ja': '事実確認'}, 'music': {'en': 'Music', 'ja': 'BGM'},
         'calc': {'en': 'Our calculation', 'ja': '自分たちの計算'}, 'art': {'en': "Image (artist's concept)", 'ja': '画像（想像図）'}}
    return {'kind': K[kind], 'title': title, 'url': url}
def nasa_img(nid, title, credit='NASA'):
    import urllib.parse
    return src('img', f'{nid} {title} ({credit})', 'https://images.nasa.gov/details/' + urllib.parse.quote(nid))
def music(title):
    return src('music', f'"{title}" Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0 License, http://creativecommons.org/licenses/by/4.0/ (shortened to a loop)', 'https://incompetech.com/music/royalty-free/')
def pj(pia, title, credit):
    return src('img', f'{pia} {title} ({credit})', f'https://photojournal.jpl.nasa.gov/catalog/{pia}')
def fact(title, url): return src('fact', title, url)
def pinned(user, ja, en): return [{'user': user, 'pinned': True, 'text': {'ja': ja, 'en': en}}]
