Data Directory — Contracts and Sources

Purpose
- Authoritative JSON used by the map. Each file’s shape is stable and validated by scripts.

Key files (examples)
- map-data.json: { scenicAreas: [], cities: [], tileLayer: {...}, trainRoutes: [] }
- regions.json: GeoJSON FeatureCollection of NY regions.
- breweries.json, restaurants.json, waterfalls.json: Arrays of POIs with name, lat, lng, optional place_id, google_maps_url, website, region.
- points_of_interest.json: Categorized POIs (museums, art, etc.).
- children.json: Family-friendly activities.
- trail-heads.json: Trailhead markers with lat/lng and metadata.
- our-airbnbs.json: Trip stays; used for reference and trip planning.
- events.json: Seasonal events by region (optional).

Conventions
- Coordinates: lat/lng (not lon). WGS84.
- Strings: UTF-8; avoid unescaped quotes.
- Optional fields: place_id, google_maps_url, website, notes.

Update flow
- Edit JSON → run maintenance/enrichment as needed → commit.
- Scripts automatically back up originals to /backups before writes.

Quality checks
- Duplicates: scripts/utilities/*duplicate* scripts.
- Regions: validated during enrichment; verify visually in app.
- Trailheads: ensure 'lng' is used (not 'lon').

Cache busting
- Frontend appends ?t=timestamp to fetches; hard refresh if changes don’t appear.

