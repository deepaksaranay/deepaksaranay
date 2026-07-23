You are working in `/app`. Build a reproducible geospatial cleaning pipeline for the files in `/app/data`:

- `/app/data/roads.geojson`: road segments with projected metric coordinates and missing CRS metadata.
- `/app/data/buildings.geojson`: building footprints in the same missing projected CRS as the roads; some polygons are invalid and some records are duplicates.
- `/app/data/districts.geojson`: district boundaries in EPSG:4326.

Determine whether the roads/buildings are EPSG:32643 or EPSG:32644 by testing which CRS aligns with the districts. Use the aligned CRS, EPSG:32643, for all output geometry and metric calculations.

Create exactly these files:

- `/app/clean_buildings.geojson`
- `/app/district_summary.csv`

`/app/clean_buildings.geojson` must be a GeoJSON FeatureCollection in EPSG:32643. Each feature must contain only these properties: `building_id`, `district_id`, and `area_m2`. Repair invalid building geometries with topology-preserving validity repair. Compute `area_m2` from the full repaired footprint in EPSG:32643, not from a clipped district intersection.

Deduplicate buildings deterministically after repair: sort records by `building_id` ascending, then keep the first record and drop later records if they repeat either the same `building_id` or the same normalized geometry.

Assign each remaining building to exactly one district. Ignore district intersection pieces smaller than `0.1` square meters. Choose the district with the largest intersection area; if the best two district overlaps differ by less than `0.01` square meters, choose the lexicographically smallest `district_id`.

`/app/district_summary.csv` must contain exactly these columns: `district_id`, `building_count`, `total_building_area_m2`, `average_building_area_m2`. Include one row for every district, even districts with zero assigned buildings. Round numeric area values to two decimal places.
