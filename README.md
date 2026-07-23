# Geospatial Data Processing and ETL Harbor Task

This repository contains a single Project Dynamo Harbor task in `task/`. The task asks an agent to clean synthetic municipal GIS data with missing CRS metadata, invalid building footprints, duplicate records, and district-boundary edge cases.

## Overview

The agent works in `/app` with three input layers copied into `/app/data`: roads, buildings, and districts. The roads and buildings use projected metric coordinates with CRS metadata removed, while districts are supplied in EPSG:4326. The agent must infer the correct projected CRS, repair and deduplicate building footprints, assign each building to one district, and produce:

- `/app/clean_buildings.geojson`
- `/app/district_summary.csv`

## Approach

The reference solution compares candidate UTM projections against the district layer, selects EPSG:32643, reprojects districts into that CRS, repairs invalid geometries with `shapely.validation.make_valid`, deduplicates after normalized WKB generation, assigns buildings by largest district intersection with sliver and tie-breaking rules, and aggregates district metrics.

## Environment

`task/environment/Dockerfile` uses a digest-pinned Python base image from the approved public ECR namespace and bakes in pinned Python dependencies for geospatial processing and verification. The verifier installs nothing at test time.

## Verification

`task/tests/test.sh` runs the pytest verifier in `task/tests/test_outputs.py`. The tests check output existence, exact schemas, CRS metadata, geometry validity, deterministic deduplication, expected building areas and district assignments, and CSV aggregates derived from the GeoJSON output.
