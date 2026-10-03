from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import folium
import pandas as pd


MODULE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODULE_DIR.parents[1]
DATA_DIR = MODULE_DIR / "data"
OUTPUT_DIR = MODULE_DIR / "output"
PUBLIC_OUTPUT_DIR = PROJECT_ROOT / "public" / "modules" / "soil-salinity-mapping"

POINTS_PATH = DATA_DIR / "karachi_halophyte_points.csv"
VEGETATION_PATH = DATA_DIR / "karachi_vegetation_coverage.csv"

SOURCE_LABEL = "Niaz et al., 2021, Table 2"
STUDY_AREA = "Karachi Coast"
DATA_MODE = "observed_halophyte_locations"
SCIENTIFIC_NOTICE = "Observed GPS-geotagged halophyte species locations from the Karachi Coast source table."

OUTPUT_COLUMNS = [
    "id",
    "species",
    "family",
    "latitude",
    "longitude",
    "source",
    "observed_value_type",
    "ec_ds_m",
    "study_area",
]


def polygon_feature(name: str, coordinates: list[list[float]]) -> dict[str, object]:
    return {
        "type": "Feature",
        "properties": {"shapeName": name},
        "geometry": {"type": "Polygon", "coordinates": [coordinates]},
    }


def study_area_geojson(points_df: pd.DataFrame) -> tuple[dict[str, object], dict[str, object]]:
    padding = 0.08
    min_lon = float(points_df["longitude"].min()) - padding
    max_lon = float(points_df["longitude"].max()) + padding
    min_lat = float(points_df["latitude"].min()) - padding
    max_lat = float(points_df["latitude"].max()) + padding
    polygon = [
        [min_lon, min_lat],
        [max_lon, min_lat],
        [max_lon, max_lat],
        [min_lon, max_lat],
        [min_lon, min_lat],
    ]
    context = polygon_feature("Karachi Coast Context", polygon)
    target = {
        "type": "FeatureCollection",
        "features": [polygon_feature("Karachi Coast Study Area", polygon)],
    }
    return context, target


def load_observed_points() -> pd.DataFrame:
    if not POINTS_PATH.exists():
        raise FileNotFoundError(f"Observed halophyte point data was not found: {POINTS_PATH}")

    points_df = pd.read_csv(POINTS_PATH)
    missing_columns = [column for column in OUTPUT_COLUMNS if column not in points_df.columns]
    if missing_columns:
        raise ValueError(f"Observed point data is missing columns: {', '.join(missing_columns)}")

    points_df = points_df[OUTPUT_COLUMNS].copy()
    points_df["latitude"] = points_df["latitude"].astype(float)
    points_df["longitude"] = points_df["longitude"].astype(float)
    points_df["ec_ds_m"] = points_df["ec_ds_m"].fillna("Not reported").replace("", "Not reported")
    return points_df


def load_vegetation_summary() -> list[dict[str, object]]:
    if not VEGETATION_PATH.exists():
        return []
    return pd.read_csv(VEGETATION_PATH).to_dict(orient="records")


def popup_html(row: pd.Series) -> str:
    values = [
        ("Species", row["species"]),
        ("Family", row["family"]),
        ("Latitude", f"{float(row['latitude']):.4f}"),
        ("Longitude", f"{float(row['longitude']):.4f}"),
        ("Source", row["source"]),
        ("Study Area", STUDY_AREA),
    ]
    table_rows = "\n".join(
        "<tr>"
        f"<th>{html.escape(str(label))}</th>"
        f"<td>{html.escape(str(value))}</td>"
        "</tr>"
        for label, value in values
    )
    return f"""
    <div style="font-family: IBM Plex Sans, system-ui, -apple-system, Segoe UI, sans-serif; min-width: 260px; max-width: 340px;">
      <h4 style="margin: 0 0 8px; color: #173f39; font-family: Georgia, serif; font-weight: 600;">Halophyte Survey Record</h4>
      <table style="border-collapse: collapse; width: 100%; font-size: 12px;">
        {table_rows}
      </table>
    </div>
    """


def create_map(points_df: pd.DataFrame, context_geojson: dict[str, object], study_area: dict[str, object]) -> folium.Map:
    center_lat = float(points_df["latitude"].mean())
    center_lon = float(points_df["longitude"].mean())
    halophyte_map = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles="OpenStreetMap")

    folium.GeoJson(
        context_geojson,
        name="Karachi Coast Context",
        style_function=lambda feature: {"fillOpacity": 0, "color": "#6f7d78", "weight": 1.2},
    ).add_to(halophyte_map)

    folium.GeoJson(
        study_area,
        name="Karachi Coast Study Area",
        style_function=lambda feature: {
            "fillColor": "#dfe8e3",
            "color": "#205f55",
            "weight": 1.8,
            "fillOpacity": 0.16,
        },
        tooltip=folium.GeoJsonTooltip(fields=["shapeName"], aliases=["Study Area:"]),
    ).add_to(halophyte_map)

    observed_layer = folium.FeatureGroup(name="Observed Halophyte Locations", show=True)
    for _, row in points_df.iterrows():
        folium.CircleMarker(
            location=[float(row["latitude"]), float(row["longitude"])],
            radius=5,
            color="#173f39",
            fill=True,
            fill_color="#2f7568",
            fill_opacity=0.82,
            weight=1,
            tooltip=str(row["species"]),
            popup=folium.Popup(popup_html(row), max_width=380),
        ).add_to(observed_layer)

    observed_layer.add_to(halophyte_map)
    folium.LayerControl(collapsed=False).add_to(halophyte_map)
    return halophyte_map


def write_outputs(region: str) -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    points_df = load_observed_points()
    context_geojson, study_area = study_area_geojson(points_df)
    vegetation_summary = load_vegetation_summary()

    salinity_grid_path = OUTPUT_DIR / "salinity_grid.csv"
    context_path = OUTPUT_DIR / "pakistan_boundary.geojson"
    study_area_path = OUTPUT_DIR / "target_provinces.geojson"
    output_map_path = OUTPUT_DIR / "soil_salinity_map.html"
    public_map_path = PUBLIC_OUTPUT_DIR / "generated-map.html"

    points_df.to_csv(salinity_grid_path, index=False)
    context_path.write_text(json.dumps(context_geojson, indent=2), encoding="utf-8")
    study_area_path.write_text(json.dumps(study_area, indent=2), encoding="utf-8")

    halophyte_map = create_map(points_df, context_geojson, study_area)
    halophyte_map.save(output_map_path)
    halophyte_map.save(public_map_path)

    metadata = {
        "status": "generated",
        "mode": DATA_MODE,
        "region": region,
        "study_area": STUDY_AREA,
        "source": SOURCE_LABEL,
        "observed_value_type": "GPS-Geotagged Halophyte Species Locations",
        "ec_available": False,
        "ec_display": "Not reported in source",
        "points_rendered": int(len(points_df)),
        "total_points": int(len(points_df)),
        "scientific_notice": SCIENTIFIC_NOTICE,
        "vegetation_summary": vegetation_summary,
        "outputs": {
            "observed_points_csv": POINTS_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "vegetation_coverage_csv": VEGETATION_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "salinity_grid_csv": salinity_grid_path.relative_to(PROJECT_ROOT).as_posix(),
            "pakistan_boundary_geojson": context_path.relative_to(PROJECT_ROOT).as_posix(),
            "target_provinces_geojson": study_area_path.relative_to(PROJECT_ROOT).as_posix(),
            "soil_salinity_map_html": output_map_path.relative_to(PROJECT_ROOT).as_posix(),
            "public_map_html": public_map_path.relative_to(PROJECT_ROOT).as_posix(),
        },
    }
    (OUTPUT_DIR / "generation_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Karachi coast observed halophyte location map assets.")
    parser.add_argument("--province", default="Karachi coast")
    args = parser.parse_args()

    metadata = write_outputs(region=args.province or "Karachi coast")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
