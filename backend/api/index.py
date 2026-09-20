from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI
from fastapi.responses import JSONResponse


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

for path in (BACKEND_DIR, PROJECT_ROOT):
    path_text = str(path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from soil_salinity_service import generate_soil_salinity_map, soil_salinity_status  # noqa: E402


app = FastAPI(title="Halophyte Decision Support API")

STATIC_DEPLOYMENT_MESSAGE = (
    "Live generation is available locally; deployment is serving static/project data."
)


class LazyBackendApp:
    def __init__(self) -> None:
        self._app: Callable[..., Any] | None = None

    def _load(self) -> Callable[..., Any]:
        if self._app is None:
            from main import app as backend_app

            self._app = backend_app
        return self._app

    async def __call__(self, scope: dict[str, Any], receive: Callable[..., Any], send: Callable[..., Any]) -> None:
        await self._load()(scope, receive, send)


def _runtime() -> str:
    return "vercel" if os.getenv("VERCEL") else "local"


@app.get("/api/health")
@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "runtime": _runtime(),
        "message": "API is running.",
    }


@app.get("/api/soil/status")
@app.get("/soil/status")
@app.get("/api/soil-salinity/status")
@app.get("/soil-salinity/status")
def soil_status() -> dict[str, object]:
    return soil_salinity_status()


@app.post("/api/soil/generate")
@app.post("/soil/generate")
@app.post("/api/soil-salinity/generate-map")
@app.post("/soil-salinity/generate-map")
def soil_generate(request: dict[str, object] | None = None) -> Any:
    province = str((request or {}).get("province") or "Karachi Coast")
    try:
        return generate_soil_salinity_map(province=province)
    except Exception as exc:
        if os.getenv("VERCEL"):
            return JSONResponse(
                status_code=200,
                content={
                    "status": "static_unavailable",
                    "mode": "vercel_static",
                    "data_mode": "observed_halophyte_locations",
                    "deployment_mode": "vercel_static",
                    "message": STATIC_DEPLOYMENT_MESSAGE,
                    "region": "Karachi Coast",
                    "study_area": "Karachi Coast",
                    "source": "Niaz et al., 2021, Table 2",
                    "ec_available": False,
                    "ec_display": "Not reported in source",
                    "points_rendered": 0,
                    "total_points": 0,
                    "generation_state": "assets_generated",
                    "map_label": "Observed Halophyte Locations",
                    "output_dir": "",
                    "python_executable": sys.executable,
                    "scientific_notice": "Observed GPS-geotagged halophyte species locations from the Karachi Coast source table.",
                    "outputs": {},
                    "detail": "Static generated map is not available.",
                    "map_url": None,
                },
            )
        return JSONResponse(
            status_code=500,
            content={"detail": f"Soil salinity map generation failed: {exc}"},
        )


app.mount("/api", LazyBackendApp())
app.mount("/", LazyBackendApp())
