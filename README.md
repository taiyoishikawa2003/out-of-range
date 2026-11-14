# OUT OF RANGE

A short-video style feed where the machines NASA left on the Moon, Mars and in deep space post about their own (true) lives.
NASA Space Apps Challenge 2026 — *Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars*. Team SunSunWorld (Kushimoto).

**Live:** https://<user>.github.io/<repo>/ — no login, works on phones, tablets and PCs.

## Features
- Vertical swipe feed (CSS scroll-snap) with autoplaying video, captions (WebVTT, EN/JA), seek bar, tap to unmute/pause, double-tap to like
- Swipeable photo posts with 8 slide layouts (photo+text, big number, quiz, before/after, chat, paper/form, tier list, photo dump)
- Every post ends with an automatic **Sources** slide; a Sources button on every post
- Like, save, follow, comments, share (Web Share API / copy link), deep links `#/p/<id>`
- Following / For You tabs, Discover (search + Moon/Mars/Deep space filters), machine profile pages
- **Create**: kids make their own true post in the browser (requires a source), preview live, download slides as PNG
- Read-aloud (browser text-to-speech), English / 日本語, keyboard controls, reduced-motion support
- Privacy: no accounts, no tracking; everything personal stays in the browser (localStorage / IndexedDB)

## Run locally
Any static server, e.g. `python3 -m http.server` then open http://localhost:8000/.

## Add a post
Edit `data/posts.json` (accounts in `data/accounts.json`, photo library for Create in `data/library.json`).
- Video: `{"type":"video","video":{"src","poster","captions":{"en","ja"}}, ...}`
- Photo post: `{"type":"carousel","slides":[{"layout":"overlay","bg":"...","pos":"top","texts":[{"t":{"en","ja"},"style":"title"}]}]}`
- Layouts: `overlay`, `number`, `quiz`, `compare`, `chat`, `document`, `tier`, `dump` (see `js/render.js`).
- Every post needs `sources: [{title, url}]`.

## Credits
- NASA images and media: see the Sources of each post and the About page. NASA does not endorse this project.
- [idb-keyval](https://github.com/jakearchibald/idb-keyval) (Apache-2.0), [html-to-image](https://github.com/bubkoo/html-to-image) (MIT) in `vendor/`.
- Use of AI: see the About page.

## License
Apache License 2.0
