# OUT OF RANGE: submission text

Text for the NASA Space Apps Challenge 2026 project page (English, ready to paste). Last updated 2026-11-15.

## Project Name

OUT OF RANGE

## High-Level Project Summary

OUT OF RANGE is a short-video style feed for kids who grew up on short videos, including kids who are not interested in space. The machines NASA left on the Moon, on Mars and in deep space post about their own lives, in formats those kids already know: a scary story, a POV, a group chat, a nav app, a ranking, a movie trailer, a quiz, a game. The jokes are only in the format. Every fact is true. Each post says what the machine is, why it was sent and what it found, is built from real NASA images and sound, and links to its NASA sources. A map shows where every machine rests now, and kids can make their own true post, which the app will not publish without a source. It runs in any browser with no login, in English and Japanese.

## Link to Project Demo

https://taiyoishikawa2003.github.io/out-of-range/demo/

## Link to Final Project

https://taiyoishikawa2003.github.io/out-of-range/

## Detailed Project Description

**What it is**

OUT OF RANGE looks and works like the short-video apps kids already use: a vertical feed you swipe through, with sound, likes, comments and profiles. But every account belongs to a machine NASA left behind, and every post is a true story about it.

**Why this form**

The challenge says school-age kids "often hear only about active, ongoing missions", and that the history of past missions sits in "dense technical websites". We asked where those kids already spend their attention. The answer is short-video feeds. So instead of asking kids to come to a space site, we took the machines to the place and the formats kids already know. A kid with no interest in space will still stop for a scary story, a group chat or a ranking. The space fact is the punchline.

**What is in the feed** (14 posts: videos with sound, swipeable photo posts, a playable game and a quiz)

- InSight (Mars): a scary-story video built on the real sound of a meteoroid hitting Mars, recorded by its seismometer
- Surveyor 3 (Moon): a POV video. Alone for 2.5 years, then Apollo 12 landed about 180 m away and took its camera home for science
- Apollo landing sites (Moon): a tappable quiz about what people left on the Moon, and why scientists want some of it back
- Opportunity (Mars): a landscape movie trailer shown in a "PR" slot, like a sponsored post (our own trailer, labelled as not a real ad)
- Pioneer 10 (deep space): its nav app. "Arrive in about 2 million years." Walking would take longer than the age of the universe
- Spirit (Mars): "expectation vs reality". A broken wheel dragged through the soil and dug up nearly pure silica, evidence of ancient hot springs or steam vents
- A just-for-fun quiz, "Which space machine are you?", whose result cards carry real facts about eight machines
- NEAR Shoemaker (asteroid Eros): a group chat. An orbiter with no legs is asked to land, and survives
- Kepler (deep space): a zodiac ranking video made from real Kepler / K2 data
- Opportunity (Mars): a playable game. First try to drive the rover like an RC car with a 20-minute signal delay (you cannot). Then drive it the way rover drivers really did: plan the day, send the commands at once, and let the rover stop itself when its cameras see a rock
- Viking 1 (Mars): a detective case file with a tappable quiz. What cut off the lander after six years? (A faulty command from Earth.)
- Opportunity (Mars): "We texted 1,000 times. No reply." The ending of the trailer: more than a thousand commands after the 2018 dust storm
- Apollo 17 rover, Ingenuity, InSight, Apollo 11 lander: a fashion check. Four looks, four real engineering reasons
- Opportunity, Spirit, Viking 1, Pioneer 10, Ingenuity: a ranking of how many times longer than planned each one worked

**Beyond the feed**

- "Where are they now?": interactive maps of the Moon and Mars with 22 landing sites and machines (Apollo descent stages and rovers, Surveyors, Vikings, Sojourner, Spirit, Opportunity, Phoenix, InSight, Ingenuity, and NEAR, Dawn, Kepler and Pioneer 10 farther out). Tapping a pin answers the questions the challenge asks: what it is, why it was sent, what it found, and where it is now. Landing positions come from NASA's NSSDCA catalogue.
- Lunar Lost & Found (/lost/): a counter for things left on the Moon. Each claim slip leads to the machine next to it and a small hands-on science scene (laser ranging, moonquakes, Moon gravity).
- Create: kids make their own true post from real NASA photos. The app asks for a source before it lets them post, so the habit we want to teach (check where a fact comes from) is built into the tool. Posts stay on the device.
- A 10-minute activity for classes and families (About page).

**How it answers the challenge**

- *What they are, why they were sent, what they found*: every post carries this in its pinned "answer" comment, in plain words for kids, and the map gives the same three answers for every machine.
- *Showing how missions operated rather than listing facts*: each post is built around one moment. A lander photographing its own foot. A camera detached and carried home. A last photo cut short by touchdown. And one post is a game: kids feel the signal delay themselves, then drive the rover the way its drivers really did.
- *Discoveries they still make*: some of these machines are still doing science. The laser reflector Apollo 11 left is still used today to measure the distance to the Moon (light takes about 2.5 seconds to go and come back), which is how we know the Moon moves about 3.8 cm farther away each year. The map says so on its pin, and the Lunar Lost & Found has a hands-on scene for it.
- *A personal connection*: the machines speak in the first person, and the last post ends on one line: "They weren't thrown away. They worked to the very end."
- *Age group*: upper elementary to junior high (about 9 to 15). *Perspective*: the machines' own. *Scope*: broad, from the Moon to interstellar space.
- *Accessibility*: no login, any phone or PC, English and Japanese, read-aloud for photo posts, keyboard controls, reduced-motion support, works offline after the first visit.

**How we keep it accurate**

- Every fact is checked against NASA pages before it is posted (NASA Science mission pages, NSSDCA, the NASA Image and Video Library, the JPL Photojournal). Every post has a Sources button, and the About page lists every resource used.
- Numbers we calculated ourselves are marked as our calculation, with the assumptions written out.
- Real photos are labelled "Real photo". NASA artist's concepts are labelled. We use no AI-generated images, video or voices.
- Invented lines (the chats, the POV thoughts) are labelled as dramatization in each post.

**How it was built**

A static web app in plain HTML, CSS and JavaScript (no framework, no server, no accounts), hosted on GitHub Pages. Posts are data (JSON). Photo posts are small HTML slides rendered to images. Motion videos are web pages with a timeline, recorded frame by frame with headless Chrome and mixed with ffmpeg, in both languages. Everything personal (likes, follows, comments, created posts) stays in the browser. Open source under Apache 2.0: https://github.com/taiyoishikawa2003/out-of-range

**What is next**

Classroom tests with kids, a furigana (reading aid) mode for younger Japanese readers, and more machines and formats.

## NASA Data

NASA Science mission pages and news (facts, dates, design goals):
- https://appel.nasa.gov/2015/08/14/this-month-in-nasa-history-a-quest-commenced-for-life-on-mars
- https://ares.jsc.nasa.gov/missions/mer/
- https://science.nasa.gov/mission/dawn/
- https://science.nasa.gov/mission/insight/
- https://science.nasa.gov/mission/kepler
- https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/
- https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/
- https://science.nasa.gov/mission/mars-pathfinder/
- https://science.nasa.gov/mission/mars-phoenix/
- https://science.nasa.gov/mission/near-shoemaker/
- https://science.nasa.gov/mission/pioneer-10/
- https://science.nasa.gov/mission/surveyor-3/
- https://science.nasa.gov/mission/viking-1/
- https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end/
- https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/
- https://science.nasa.gov/resource/opportunity-rovers-full-marathon-length-traverse
- https://science.nasa.gov/resource/mars-in-a-minute-how-do-rovers-drive-on-mars/
- https://science.nasa.gov/universe/overview/
- https://www.jpl.nasa.gov/images/pia07999-looking-back-at-purgatory-dune
- https://www.jpl.nasa.gov/news/nasa-insight-lander-hears-martian-winds/
- https://www.jpl.nasa.gov/news/nasa-retires-kepler-space-telescope
- https://www.jpl.nasa.gov/news/nasas-opportunity-rover-mission-on-mars-comes-to-end/
- https://www.jpl.nasa.gov/news/opportunity-rolling-again-after-fifth-mars-winter/
- https://www.jpl.nasa.gov/news/rover-amnesia-event-follows-latest-memory-reformatting/
- https://www.jpl.nasa.gov/edu/resources/lesson-plan/mars-rover-driver-board-game/
- https://robotics.jpl.nasa.gov/news/learning-to-drive-the-mars-rovers/
- https://www-robotics.jpl.nasa.gov/media/documents/tradeoffs_ijrr_07.pdf
- https://www.jpl.nasa.gov/videos/spirit-six-years-of-roving-mars/
- https://www.nasa.gov/missions/lro/laser-beams-reflected-between-earth-and-moon-boost-science/

NASA Space Science Data Coordinated Archive (NSSDCA), https://nssdc.gsfc.nasa.gov/ : spacecraft entries 1966-045A, 1967-084A, 1967-112A, 1968-001A, 1969-059C, 1969-099C, 1971-008C, 1971-063C, 1972-031C, 1972-096C, 1975-075C, 1975-083C, 1996-068A, 2003-027A, 2003-032A, 2007-034A, 2007-043A, 2020-052A (what each machine was, its landing coordinates and its final state). These coordinates place the pins on our maps.

NASA Image and Video Library (https://images.nasa.gov/), images, video and sound used in posts, in the photo library of the Create tool and in profile pictures: 7040032, ARC-1972-AC72-1338, ARC-1973-AC73-4247, ARC-1973-AC73-9019, AS12-48-7133, AS12-48-7134, JPL-20190423-INSIGHf-0001-First Likely Marsquake Heard by NASAs InSight, JPL-20220919-INSIGHf-0001-InSight Captures Sound of a Meteoroid Striking Mars_1080, KSC-as11-40-5927, PIA04413, PIA09262, PIA09491, PIA11823, PIA15801, PIA21473, PIA21751, PIA22871, PIA22876, PIA23177, PIA23202, PIA23376, PIA25408, S69-39334, as08-14-2383, as11-40-5899, as12-48-7099, as12-48-7110, as12-48-7121, as12-48-7136, as14-66-09277, as17-137-20979, as17-148-22727, iss073e0027806.

JPL Photojournal (https://photojournal.jpl.nasa.gov/): PIA00381, PIA00407, PIA00563, PIA00567, PIA01881, PIA02467, PIA03148, PIA04413, PIA04422, PIA05144, PIA06739, PIA07999, PIA09262, PIA09491, PIA09703, PIA11823, PIA11824, PIA12131, PIA12922, PIA13088, PIA14129, PIA15281, PIA15689, PIA15801, PIA16120, PIA16442, PIA16923, PIA17956, PIA18614, PIA19154, PIA19155, PIA21473, PIA21751, PIA22871, PIA22876, PIA22928, PIA22929, PIA23177, PIA23202, PIA23376, PIA23882, PIA24438, PIA24648, PIA25287, PIA25408.

Maps: Moon map from NASA's Scientific Visualization Studio CGI Moon Kit (https://svs.gsfc.nasa.gov/4720); Mars map from NASA 3D Resources (https://github.com/nasa/NASA-3D-Resources).

How we used it: text facts come from the mission pages and NSSDCA. Every image, video clip and sound in a post is a NASA original, credited in that post's Sources. The full list, post by post, is on the About page of the site.

## Space Agency Partner & Other Data

Other sources used for facts in posts (each is linked from the post that uses it):

- Smithsonian National Air and Space Museum: Apollo 14 (golf shots): https://airandspace.si.edu/apollo-missions/apollo-14
- MAST/STScI: K2 Campaign Fields (dates, positions, objects in each field): https://archive.stsci.edu/missions-and-data/k2/campaign-fields
- Howell et al. 2014, The K2 Mission (fields along the ecliptic): https://arxiv.org/abs/1402.5163
- Business Insider: 96 bags and the 'Poo Bags Paradox': https://businessinsider.in/science/space/article/lunar-loo-did-apollo-astronauts-96-bags-of-poop-and-urine-seed-the-moon-with-life/articleshow/113413267.cms
- Holst, "Mars, the Bringer of War" — U.S. Air Force Band, 1998 (public domain), Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Holst-_mars.ogg
- Kepler/K2 Science Center: K2 approved programs (Campaign 19 includes TRAPPIST-1, toward Aquarius): https://keplergo.github.io/KeplerScienceWebsite/k2-approved-programs.html
- Kepler/K2 Science Center: Campaigns 11–13 (Ophiuchus, Aquarius, Taurus): https://keplergo.github.io/KeplerScienceWebsite/k2-cycle-4-highlights-in-future-fields.html
- Kepler/K2 Science Center: Campaigns 17–19 (Virgo, Cancer, Aquarius; Spica): https://keplergo.github.io/KeplerScienceWebsite/k2-cycle-6-notable-objects-in-campaigns-17-18-19.html
- Kepler/K2 Science Center: Campaigns 14–16 (Leo; Wolf 359): https://keplergo.github.io/KeplerScienceWebsite/k2-go-cycle-5-notable-targets-in-campaigns-14-15-16.html
- The Planetary Society: Silica Soils Near Home Plate: https://planetary.org/space-images/silica-soils-near-home-plate
- NASA/JPL news release: Spirit faces circuitous route (2009) — dragged wheel, silica & hot springs: https://spaceflightnow.com/news/n0903/10spirit
- NASA rover status reports (odometry: 5,347.89 m in 2005; 34,361.37 m in Jan 2012; 41.30 km in Dec 2014), via SpaceRef / Mars Daily: https://www.marsdaily.com/reports/Flash_Memory_Reformat_Planned_999.html
- The Planetary Society: Farewell, Kepler (last data from Aquarius): https://www.planetary.org/articles/farewell-kepler
- BBC Science Focus: Why is there poo on the Moon? (96 bags, left to offset Moon-rock weight): https://www.sciencefocus.com/space/why-is-there-poo-on-the-moon/
- Space.com: Spirit rover (90-sol plan, last contact March 22, 2010): https://www.space.com/18766-spirit-rover.html
- Vox: Apollo astronauts left their poop on the moon (microbe survival, Schuerger): https://www.vox.com/science-and-health/2019/3/22/18236125/apollo-moon-poop-mars-science

Music, libraries and fonts:

- Music: Kevin MacLeod (incompetech.com), Creative Commons Attribution 4.0: "Monkeys Spinning Monkeys", "Fluffing a Duck", "Heartwarming", "Gymnopedie No. 1", "Carefree", "Investigations", "Local Forecast - Elevator", "Sneaky Snitch", "Funkorama", "Hyperfun", "Wholesome", "Heartbreaking" (some shortened)
- Open-source libraries: idb-keyval (Apache-2.0), html-to-image (MIT). Font in rendered slides and videos: Noto Sans CJK (SIL Open Font License).

## Use of Artificial Intelligence

We used an AI assistant (Claude by Anthropic, a large language model). Here is exactly how.

- Concept and rules: chosen by the team. A short-video feed where the machines NASA left behind post for kids; use formats kids already know; keep the jokes in the format only; make every fact real.
- Post ideas and text: some ideas came from the team, and some were proposed and drafted by the AI assistant from NASA sources. The team reviews the posts, checks the wording for kids and decides what stays. Every fact is linked to its source in the post.
- Code and page design: written with the AI assistant, following the team's direction.
- Videos and photo posts: assembled with AI assistance (by scripts written with the AI assistant) from real NASA images, video and sound. No image, video or voice in the project is AI-generated, so there is nothing to watermark. NASA logos are not used.
- Sound: music is by human composers and performers (credited above). Short interface sounds were synthesized by scripts written with the AI assistant.
- Read-aloud: the browser's built-in text-to-speech on the user's own device (a synthetic voice, not generated by us).
- Research: AI was used to search for and summarize NASA sources. Facts were then checked against the NASA pages themselves.

The same disclosure is on the About page of the site and in the README of the repository.
