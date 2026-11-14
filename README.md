# OUT OF RANGE

**Live:** https://taiyoishikawa2003.github.io/out-of-range/ (no login; phones, tablets and PCs; English / 日本語)

A short-video style feed where the machines NASA left on the Moon, on Mars and in deep space post about their own lives. The jokes are only in the format. Every fact is true and linked to its source.

NASA Space Apps Challenge 2026, challenge *Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars*. Team SunSunWorld (Kushimoto, Japan).

## Why a short-video feed?

The challenge asks for a story that introduces school-age kids to this hardware and the science it made possible. Kids already spend their time in short-video feeds, including kids who are not interested in space. So we put the machines there, in formats those kids already know: a scary story, a group chat, a nav app, a fashion check, a ranking, a movie trailer. Each post says what the machine is, why it was sent, and what it found.

## What is in the feed

| Post | Machine (place) | Format |
|---|---|---|
| "This was recorded on Mars." | InSight (Mars) | Scary-story video built on the real sound of a meteoroid impact |
| Expectation vs reality | Spirit (Mars) | Photo post: a broken wheel digs up evidence of ancient hot springs |
| What did people leave on the Moon the most of? | Apollo landing sites (Moon) | Tappable quiz |
| OPPORTUNITY | Opportunity (Mars) | Landscape movie trailer shown in a "PR" slot (our own trailer, not a real ad) |
| NASA's "favorite" zodiac signs | Kepler (deep space) | Ranking video made from real Kepler data |
| I waited on the Moon for 2.5 years | Surveyor 3 (Moon) | POV story |
| Pioneer 10's nav app | Pioneer 10 (deep space) | Nav app: "arrive in about 2 million years" |
| Case file | Viking 1 (Mars) | Detective file with a tappable quiz |
| "Want to try landing?" | NEAR Shoemaker (asteroid Eros) | Group chat |
| Fashion check | Apollo 17 rover, Ingenuity, InSight, Apollo 11 lander | Four looks, four real reasons |
| Worked longer than planned: TOP 5 | Opportunity, Spirit, Viking 1, Pioneer 10, Ingenuity | Ranking |

A second, separate piece lives at [`/lost/`](https://taiyoishikawa2003.github.io/out-of-range/lost/): the **Lunar Lost & Found**, a counter for things left on the Moon. Each claim slip leads to the machine next to it and a small hands-on science scene (laser ranging, moonquakes, Moon gravity).

## Features

- Vertical swipe feed with autoplaying video, sound, seek bar, tap to pause, double-tap to like
- Swipeable photo posts with tappable quizzes and per-slide music
- A **Sources** button on every post, and one page that lists every NASA resource used (About)
- Pinned "answer" comments that explain the science in plain words, and say which parts are dramatized
- **Create**: kids make their own true post in the browser. A source is required. Posts stay on the device
- Discover (search, Moon / Mars / Deep space filters) and a profile page for every machine
- Read-aloud for photo posts, English / 日本語, keyboard controls, reduced-motion support
- Privacy: no accounts, no ads, no tracking. Likes, follows, comments and created posts stay in the browser
- Works offline after the first visit (service worker)

## How we keep it accurate

- Every fact is checked against NASA pages (NASA Science mission pages, NSSDCA, the NASA Image and Video Library and the JPL Photojournal) before it is posted. Each post lists its sources.
- Numbers we calculated ourselves (walking time to Aldebaran, "times longer than planned") are marked as our calculation, with the assumptions written out.
- Real photos are labelled "Real photo". NASA artist's concepts are labelled "Artist's concept". We do not use AI-generated images, video or voices.
- Invented lines (the chat, the POV thoughts) are labelled as dramatization in the pinned comment of each post.

## Run locally

Any static server works:

```
python3 -m http.server
```

Then open http://localhost:8000/. There is no build step for the site itself (plain HTML, CSS and JavaScript modules).

## How posts are made

- `data/posts.json` is the feed. `data/accounts.json` holds the machine accounts. `data/library.json` is the photo library for Create.
- Photo posts are written as small HTML slides and rendered to images:
  - `tools/slides/p_*.py`: one file per post (slides, caption, pinned comment, sources) in Japanese and English
  - `tools/slides/slides.css`: the slide design system
  - `python3 tools/slides/build.py [post ...]` renders the slides with headless Chrome and updates `data/posts.json`
  - NASA photos are read from `$OOR_ASSETS/<nasa_id>.jpg` (download them from images.nasa.gov; the ids are in each post file)
- `tools/build_*.py` build the earlier videos and photo posts. `tools/version_media.py` adds a content hash to every media path.
- `tools/nasa_collect.py` collects candidate media for every machine on the official challenge resource list (`data/nasa_catalog.json`).

## Use of AI

We used an AI assistant (Claude by Anthropic) for code, drafts and source look-ups, under the team's direction. The team chose the concept, the audience and the formats, and checks what is published. We do not use AI-generated images, video or voices. Details are on the About page of the site.

## Credits

- NASA images, video and sound: see the Sources of each post and the About page. NASA does not endorse this project.
- Music: Kevin MacLeod (incompetech.com), CC BY 4.0; Holst, "Mars, the Bringer of War", U.S. Air Force Band (public domain, via Wikimedia Commons). Track list on the About page.
- [idb-keyval](https://github.com/jakearchibald/idb-keyval) (Apache-2.0) and [html-to-image](https://github.com/bubkoo/html-to-image) (MIT) in `vendor/`.

## License

Apache License 2.0
