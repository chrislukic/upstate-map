#!/usr/bin/env python3
import json
import time
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT = "scenic-ny-map/1.0 (+https://example.com)"
BASE_URL = "https://nominatim.openstreetmap.org/search?"

INPUT_FILE = "scripts/orchards.json"
OUTPUT_FILE = "public/data/orchards_geocoded.json"


def geocode(query: str):
    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1
        # Optionally: 'countrycodes': 'us'
    }
    url = BASE_URL + urlencode(params)
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req) as resp:
        data = resp.read()
    try:
        results = json.loads(data)
        if results:
            best = results[0]
            return {
                "lat": float(best.get("lat")),
                "lon": float(best.get("lon")),
                "display_name": best.get("display_name"),
                "class": best.get("class"),
                "type": best.get("type"),
                "importance": best.get("importance")
            }
        return None
    except Exception as e:
        print(f"Error parsing response for {query}: {e}", file=sys.stderr)
        return None


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    orchards = data.get("orchards", [])
    output = {"source": data.get("source"), "orchards": []}

    for idx, o in enumerate(orchards, 1):
        query = f"{o['name']}, {o['town']}, {o['state']}"
        print(f"[{idx}/{len(orchards)}] Geocoding: {query}")
        info = geocode(query)
        time.sleep(1.2)  # politeness per Nominatim usage policy
        out = {
            **o,
            "geocoded": info
        }
        output["orchards"].append(out)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {OUTPUT_FILE} with {len(output['orchards'])} entries")


if __name__ == "__main__":
    main()

