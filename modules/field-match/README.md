# Halophyte Field Match source

This module contains the source and cleaned plant datasets used by the integrated field-matching page at `public/modules/field-match/index.html`.

- `data/plants_source.csv` — source records.
- `data/plants_cleaned.json` — application-ready records.
- `scripts/clean_data.py` — deterministic source-to-JSON transformation.

The browser-ready HTML is retained under `public/modules/field-match/` because Vite copies `public/` directly into the production build.
