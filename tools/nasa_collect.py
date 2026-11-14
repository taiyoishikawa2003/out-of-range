"""Collect candidate NASA media for each machine on the official challenge resource list.
Writes data/nasa_catalog.json (metadata only). Does NOT choose what goes into posts."""
import json, urllib.request, urllib.parse, time
MACHINES = {
 # id: (place, label, official resource URL, image-search queries)
 "apollo-lm":   ("moon", "Apollo Lunar Module descent stage", "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C", ["lunar module descent stage moon surface", "apollo lunar module on moon"]),
 "lrv":         ("moon", "Lunar Roving Vehicle", "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1971-063C", ["lunar roving vehicle moon surface", "apollo 17 lunar rover", "apollo 15 lunar rover"]),
 "alsep":       ("moon", "ALSEP", "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C", ["ALSEP", "lunar laser ranging retroreflector apollo", "passive seismic experiment apollo"]),
 "surveyor":    ("moon", "Surveyor landers", "https://science.nasa.gov/mission/surveyor-3/", ["surveyor 3 apollo 12", "surveyor lander moon"]),
 "sojourner":   ("mars", "Sojourner / Mars Pathfinder", "https://science.nasa.gov/mission/mars-pathfinder/", ["sojourner rover", "mars pathfinder sojourner"]),
 "spirit":      ("mars", "Spirit rover", "https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/", ["spirit rover mars", "spirit rover tracks"]),
 "opportunity": ("mars", "Opportunity rover", "https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/", ["opportunity rover mars", "opportunity rover selfie", "opportunity tracks"]),
 "viking":      ("mars", "Viking 1 & 2 landers", "https://science.nasa.gov/mission/viking-1/", ["viking lander mars surface", "viking 1 lander"]),
 "phoenix":     ("mars", "Phoenix lander", "https://science.nasa.gov/mission/insight/", ["phoenix mars lander", "phoenix lander ice"]),
 "insight":     ("mars", "InSight lander", "https://science.nasa.gov/mission/insight/", ["insight lander selfie", "insight lander mars", "insight seismometer"]),
 "ingenuity":   ("mars", "Ingenuity helicopter", "https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/", ["ingenuity mars helicopter", "ingenuity helicopter flight"]),
 "dawn":        ("deep", "Dawn spacecraft", "https://science.nasa.gov/mission/dawn/", ["dawn spacecraft ceres", "dawn vesta"]),
 "near":        ("deep", "NEAR Shoemaker", "https://science.nasa.gov/mission/near-shoemaker/", ["NEAR shoemaker eros", "eros asteroid near"]),
 "pioneer":     ("deep", "Pioneer 10 & 11", "https://science.nasa.gov/mission/pioneer-10/", ["pioneer 10 spacecraft", "pioneer plaque", "pioneer 11"]),
 "kepler":      ("deep", "Kepler Space Telescope", "https://science.nasa.gov/mission/kepler/", ["kepler space telescope", "kepler spacecraft"]),
}
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception as e: err = e; time.sleep(1.5)
    raise err
out = {}
for mid, (place, label, res, qs) in MACHINES.items():
    seen, items = set(), []
    for q in qs:
        for mt in ("image", "video", "audio"):
            u = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": mt, "page_size": 25 if mt == "image" else 8})
            try: d = get(u)
            except Exception as e: print("ERR", mid, q, mt, e); continue
            for it in d["collection"]["items"]:
                m = it["data"][0]; nid = m["nasa_id"]
                if nid in seen: continue
                seen.add(nid)
                links = {l.get("rel"): l["href"] for l in it.get("links", [])}
                thumb = next((l["href"] for l in it.get("links", []) if l.get("rel") == "preview"), None)
                items.append({"nasa_id": nid, "media": mt, "title": m.get("title"), "date": (m.get("date_created") or "")[:10],
                              "center": m.get("center"), "photographer": m.get("photographer") or m.get("secondary_creator"),
                              "description": (m.get("description") or "")[:600], "keywords": m.get("keywords", [])[:12],
                              "thumb": thumb, "collection": it["href"],
                              "page": f"https://images.nasa.gov/details/{urllib.parse.quote(nid)}", "query": q})
    out[mid] = {"place": place, "label": label, "resource": res, "items": items}
    print(mid, len(items), sum(i["media"] == "image" for i in items), "img", sum(i["media"] == "video" for i in items), "vid", sum(i["media"] == "audio" for i in items), "aud")
json.dump(out, open("data/nasa_catalog.json", "w"), ensure_ascii=False, indent=1)
