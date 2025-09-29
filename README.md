# Scenic NY Map

Interactive map of New York State’s scenic destinations, cities, POIs, trailheads, and PYO farms. Built for fast trip planning and high‑signal discovery.

## Quick start

```bash
# install deps
npm install

# dev server (Vite)
npm run dev
# http://localhost:5173

# build for production
npm run build
# output -> dist/
```

## Project overview

- Scenic areas with a simple rating legend; cities sized by population and colored by NYC drive time.
- Multiple data layers: waterfalls, restaurants, breweries, trailheads, children’s activities, Airbnbs, POIs, PYO.
- Tile + data driven via `public/data/*` JSON and GeoJSON.

## Data directory and schema

- Authoritative data lives in `public/data/`.
- Contracts and file descriptions: see `public/data/README.md`.
- Optional files (e.g., `events.json`) are handled gracefully if absent.

## Maintenance & automation

- Data enrichment, verification, and utilities live in `scripts/`.
- Start here: `scripts/README.md` and `scripts/maintenance/README.md`.
- Google Place ID enrichment and backups supported.

## Tech stack

- Vite, Leaflet, vanilla JS/CSS.
- Build output in `dist/` with hashed assets.

## Troubleshooting

- Data not updating: hard refresh with cache disabled; fetches append `?t=timestamp`.
- 404 on data: run Vite from the repo root; data is served from `public/` at `/`.
- `events.json` missing: it’s optional; the map loads without it.

## License & contributions

Internal project. PRs welcome from collaborators.

