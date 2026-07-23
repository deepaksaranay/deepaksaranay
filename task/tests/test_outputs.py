"""Verifier for the geospatial CRS repair, deduplication, spatial join, and aggregation task."""
import csv, json, math
from pathlib import Path
from shapely.geometry import shape

APP=Path('/app')

def load_clean():
    return json.loads((APP/'clean_buildings.geojson').read_text())

def test_required_files_exist():
    """Both files named in the instruction must be produced at the required absolute paths."""
    assert (APP/'clean_buildings.geojson').is_file()
    assert (APP/'district_summary.csv').is_file()

def test_geojson_schema_crs_validity_and_deduplication():
    """The clean GeoJSON must use the required CRS/schema, valid geometries, and deterministic deduplicated building ids."""
    data=load_clean()
    assert data['type']=='FeatureCollection'
    assert data.get('crs',{}).get('properties',{}).get('name')=='EPSG:32643'
    ids=[f['properties']['building_id'] for f in data['features']]
    assert ids==['B001','B002','B003','B004','B006','B007']
    assert len(ids)==len(set(ids))==6
    for f in data['features']:
        assert set(f['properties'])=={'building_id','district_id','area_m2'}
        assert f['properties']['district_id'] in {'D-WEST','D-EAST'}
        assert shape(f['geometry']).is_valid
        assert f['properties']['area_m2'] > 0

def test_expected_building_areas_and_assignments():
    """Building areas must be full repaired footprint areas and every building must receive the expected district assignment."""
    expected_area={'B001':14400.0,'B002':22500.0,'B003':14400.0,'B004':32400.0,'B006':25600.0,'B007':24200.0}
    expected_district={'B001':'D-WEST','B002':'D-WEST','B003':'D-WEST','B004':'D-EAST','B006':'D-EAST','B007':'D-WEST'}
    for f in load_clean()['features']:
        bid=f['properties']['building_id']
        assert f['properties']['district_id']==expected_district[bid]
        assert math.isclose(float(f['properties']['area_m2']), expected_area[bid], rel_tol=0.005, abs_tol=1.0)

def test_district_summary_matches_feature_aggregates():
    """The CSV must have the exact schema, all districts, and aggregates matching the clean building features."""
    rows=list(csv.DictReader((APP/'district_summary.csv').open()))
    assert rows and set(rows[0])=={'district_id','building_count','total_building_area_m2','average_building_area_m2'}
    assert [r['district_id'] for r in rows]==['D-EAST','D-WEST']
    by={d:[] for d in ['D-EAST','D-WEST']}
    for f in load_clean()['features']:
        by[f['properties']['district_id']].append(float(f['properties']['area_m2']))
    for r in rows:
        vals=by[r['district_id']]
        assert int(r['building_count'])==len(vals)
        total=round(sum(vals),2)
        avg=round(total/len(vals),2) if vals else 0.0
        assert math.isclose(float(r['total_building_area_m2']), total, rel_tol=0.005, abs_tol=0.01)
        assert math.isclose(float(r['average_building_area_m2']), avg, rel_tol=0.005, abs_tol=0.01)
