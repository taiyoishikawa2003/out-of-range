#!/usr/bin/env python3
"""Append ?v=<content hash> to every media/ path in data/posts.json so browsers never show a stale file.
Run after rebuilding any media: python3 tools/version_media.py"""
import json, hashlib, os
P = 'data/posts.json'; posts = json.load(open(P))
def ver(path):
    clean = path.split('?')[0]
    if not os.path.exists(clean): return path
    return f"{clean}?v={hashlib.md5(open(clean, 'rb').read()).hexdigest()[:8]}"
def walk(o):
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v) for v in o]
    return ver(o) if isinstance(o, str) and o.startswith('media/') else o
json.dump(walk(posts), open(P, 'w'), ensure_ascii=False, indent=1); print('versioned')
