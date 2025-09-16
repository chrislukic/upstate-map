#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "public" / "data"
PRIMARY = DATA_DIR / "orchards_points.json"
EXTRA = DATA_DIR / "orchards_points_extra.json"
OUTPUT = DATA_DIR / "orchards_points.json"


def load_array(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            # if wrapped, try common shape {"orchards": [...]}
            if isinstance(data, dict) and isinstance(data.get("orchards"), list):
                return data["orchards"]
        except Exception:
            return []
    return []


def key_for(item: dict) -> tuple:
    name = (item.get("name") or "").strip().lower()
    lat = item.get("lat") or item.get("latitude") or item.get("coords", [None, None])[0]
    lng = item.get("lng") or item.get("longitude") or item.get("coords", [None, None])[1]
    return (name, round(float(lat), 6) if lat is not None else None, round(float(lng), 6) if lng is not None else None)


def main():
    primary = load_array(PRIMARY)
    extra = load_array(EXTRA)

    merged = []
    seen = set()
    for src in (primary, extra):
        for item in src:
            k = key_for(item)
            if k in seen:
                continue
            seen.add(k)
            merged.append(item)

    # write back to PRIMARY
    OUTPUT.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(merged)} records (merged {len(primary)} + {len(extra)})")


if __name__ == "__main__":
    main()
