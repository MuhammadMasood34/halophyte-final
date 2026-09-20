# Soil Salinity Mapper source

The active integrated page displays observed GPS-geotagged halophyte records from the Karachi Coast source table. The checked-in source does not report EC values, so the map labels them as unavailable rather than estimating salinity.

- `data/` — observed locations and vegetation-coverage context.
- `generate_soil_salinity_map.py` — deterministic Folium asset generator.
- `output/` — generated CSV, GeoJSON, HTML, and metadata.
- `reference/` — retained notebook and project source documents.
- `../../public/modules/soil-salinity-mapping/generated-map.html` — deployed browser asset.

Regenerate with:

```powershell
python modules\soil-salinity-mapper\generate_soil_salinity_map.py --province "Karachi Coast"
```
