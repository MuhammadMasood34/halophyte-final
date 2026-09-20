# Biosaline Halophyte Intelligence Platform — Supervisor Summary

The platform integrates six decision-support modules: a halophyte grass library, species-specific grass prediction, a survey-map layer, crop salinity screening, a curated knowledge graph, and field matching.

The React/TypeScript frontend is served by Vite. FastAPI provides prediction and screening endpoints. Scientific datasets, training code, production inference, and saved artifacts are separated under `ml/`. Standalone data preparation and mapping sources are under `modules/`, while deployable static assets are under `public/modules/`.

Grass prediction is constrained by a 30-record dataset. Species-based predictions use the selected record as their anchor, and the verified species GR50 remains constant when ion inputs change. Crop screening uses saved per-species surrogate artifacts when available and an explicit Maas–Hoffman fallback otherwise. All outputs are estimates intended for academic decision support, not direct agronomic prescriptions.

The mapper currently visualizes observed Karachi Coast halophyte locations. Its cited source does not include EC measurements, so the application does not invent or interpolate salinity values.
