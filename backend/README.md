# Backend API

FastAPI services for grass prediction, crop salinity screening, and survey-map status/generation.

## Run

```powershell
python -m pip install -r backend\requirements.txt
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Main endpoints

- `GET /health`, `/metadata`, `/grasses`, `/model-metrics`
- `POST /predict`
- `GET /biosaline-crop-screening/status`, `/biosaline-crop-screening/crops`
- `POST /biosaline-crop-screening/predict`
- `GET /soil-salinity/status`
- `POST /soil-salinity/generate-map`

All datasets, models, configuration, and generated assets are resolved relative to the repository root.
