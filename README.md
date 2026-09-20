# Biosaline Halophyte Intelligence Platform

The Biosaline Halophyte Intelligence Platform is a final-year computer science project that combines a searchable halophyte library, scientific prediction workflows, mapping, crop screening, a curated knowledge graph, and field-to-species matching in one React application.

## Modules

1. **Halophyte Grass Library** — search, filter, sort, inspect, and convert units for 30 curated grass records.
2. **Species-Specific Prediction Model** — estimate missing ion-concentration values from a selected species profile or mechanism group.
3. **Soil Salinity Mapper** — displays the checked-in Karachi Coast survey layer and supports local regeneration of its map assets.
4. **Crop Salinity Screening** — evaluates crop yield response, risk, irrigation frequency, and alternatives using species-specific surrogate models when available and Maas–Hoffman fallback logic otherwise.
5. **Halophyte Knowledge Graph** — explores curated paper, species, mechanism, gene, and use relationships, with local corpus search and citations.
6. **Halophyte Field Match** — filters candidate plants against field salinity and use constraints.

## Technology stack

- React 18, TypeScript, Vite, and Lucide icons
- FastAPI and Pydantic
- pandas, NumPy, scikit-learn, joblib, PyYAML, openpyxl, and Folium
- Static HTML modules embedded by the React navigation
- Vercel static and Python deployment configuration

## Repository structure

```text
backend/                         FastAPI routes and production services
docs/                            Submission and scientific reference documents
ml/
  data/                          Grass prediction dataset
  models/                        Grass prediction bundle and evaluation metadata
  notebooks/                     Grass prediction evaluation notebook
  crop_salinity/
    config/                      Crop parameters and simulation configuration
    data/source/                 Verified 241-row crop salinity dataset
    inference/                   Production crop-screening logic
    training/                    Dataset reconstruction and model training
    models/                      Crop surrogate metadata/artifacts
modules/
  field-match/                   Source data and preparation script
  knowledge-graph/               Curated graph data and construction scripts
  soil-salinity-mapper/          Survey data, generator, outputs, and references
public/modules/                  Browser-ready embedded module assets
scripts/                         Local development helpers
src/                             React application
tests/                           Backend and scientific-invariant tests
```

The HTML and map files in `public/modules/` are intentional deployment assets. Their source data and generators live under `modules/`.

## Installation

### Frontend

```powershell
npm.cmd install
```

### Backend

```powershell
python -m venv backend\.venv
backend\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Python 3.11 or 3.12 is recommended when binary scientific packages are unavailable for a newer Python release.

## Environment setup

Copy `.env.example` to `.env` only when configuration overrides are needed. Real `.env` files are ignored by Git.

- `VITE_API_BASE_URL` — optional frontend API origin; local development defaults to `http://127.0.0.1:8000`, while production defaults to same-origin `/api`.
- `ENABLE_SOIL_MAP_GENERATION` — enables local/deployed map regeneration when explicitly set to `true`; Vercel serves the checked-in map by default.
- `SOIL_SALINITY_PYTHON` — optional Python executable override for local map generation.
- `EARTHENGINE_PROJECT` — optional project identifier used by the mapper's local Earth Engine status check.

## Local development

Start both services on Windows:

```powershell
npm.cmd run dev:all
```

Or start them separately:

```powershell
cd backend
.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

```powershell
npm.cmd run dev
```

The frontend normally opens at `http://127.0.0.1:5173`; FastAPI documentation is at `http://127.0.0.1:8000/docs`.

## Production build

```powershell
npm.cmd run build
npm.cmd run preview
```

The build output is written to `dist/` and is ignored by Git.

## Data and models

- `src/data/grassLibraryData.ts` — frontend grass-library records.
- `ml/data/halophyte_grass_library.csv` — backend grass-prediction dataset.
- `ml/models/best_model_bundle.joblib` — saved grass prediction model bundle.
- `ml/models/model_comparison_results.csv` and `model_metrics_summary.json` — evaluation outputs.
- `ml/crop_salinity/data/source/AuthenticHalophyteData.xlsx` — verified crop salinity source dataset (241 observations, 6 species).
- `ml/crop_salinity/models/` — crop surrogate metadata and optional serialized models.
- `modules/soil-salinity-mapper/data/` — observed Karachi Coast locations and vegetation context.

Training notebooks and scripts are not required at application startup. Do not regenerate datasets or retrain models as part of normal development.

## Scientific assumptions

- Grass-library prediction operates on a small 30-record dataset and produces estimates, not field measurements.
- Grass-based mode anchors estimates to the selected species. Mechanism-based mode uses weighted nearest records within the selected salt-handling mechanism.
- **GR50 is a fixed characteristic of the selected grass record. Changing Na, K, or Cl inputs does not alter that species' GR50.**
- Crop screening uses a species-specific saved surrogate when both model and encoder artifacts are present. Otherwise it reports and uses the Maas–Hoffman response formula.
- Dataset column names and units are preserved. Grass GR50 is in dS/m; ion fields are in mmol kg⁻¹ tissue dry weight.
- Crop-screening output is decision support only and requires local soil, irrigation-water, cultivar, and agronomic validation.
- The currently deployed mapper contains observed GPS-geotagged halophyte locations. EC values were not reported in that source and are not inferred by the application.

## Testing

Run the complete local check:

```powershell
npm.cmd run check
```

Or run checks independently:

```powershell
npm.cmd run build
python -m unittest discover -s tests -v
python -m py_compile backend\*.py backend\api\index.py
```

Regenerate the checked-in survey map only when its source tables or generator change:

```powershell
python modules\soil-salinity-mapper\generate_soil_salinity_map.py --province "Karachi Coast"
```

## Deployment

`vercel.json` builds the Vite frontend and routes `/api/*` to `backend/api/index.py`. Client-side routes fall back to `index.html`. The checked-in map and embedded HTML modules are served from `public/modules/`; server-side map generation remains disabled on Vercel unless explicitly configured.

## Troubleshooting

- **Frontend cannot reach the API:** verify the backend is on port 8000 or set `VITE_API_BASE_URL`.
- **PowerShell blocks `npm`:** use `npm.cmd` as shown above.
- **Scientific Python package installation fails:** use Python 3.11 or 3.12 and recreate `backend/.venv`.
- **Crop screening reports fallback mode:** `surrogate_model.pkl` and `species_encoder.pkl` are optional and currently absent unless trained locally; the Maas–Hoffman fallback remains functional.
- **Embedded module is blank:** build/serve through Vite rather than opening `index.html` directly, and confirm the corresponding file exists in `public/modules/`.
- **Map regeneration fails:** install backend requirements and confirm the source CSV files under `modules/soil-salinity-mapper/data/` are present.
