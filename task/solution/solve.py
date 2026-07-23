import csv, json
from pathlib import Path
from shapely.geometry import shape, mapping
from shapely.validation import make_valid
from shapely.ops import transform
from shapely import normalize, to_wkb
from pyproj import Transformer

DATA=Path('/app/data')
APP=Path('/app')

def load(name):
    return json.loads((DATA/name).read_text())['features']

def reproj_geom(g, src='EPSG:4326', dst='EPSG:32643'):
    t=Transformer.from_crs(src,dst,always_xy=True)
    return transform(t.transform,g)

def choose_native_crs(building_geoms, district_features):
    best = None
    for epsg in (32643, 32644):
        transformed = [reproj_geom(shape(f['geometry']), dst=f'EPSG:{epsg}') for f in district_features]
        district_union = transformed[0]
        for geom in transformed[1:]:
            district_union = district_union.union(geom)
        score = sum(g.intersection(district_union).area for g in building_geoms)
        if best is None or score > best[0]:
            best = (score, epsg, transformed)
    return best[1], best[2]

district_features = load('districts.geojson')
building_features = load('buildings.geojson')
raw_building_geoms = [shape(f['geometry']) for f in building_features]
native_epsg, district_geoms = choose_native_crs(raw_building_geoms, district_features)
if native_epsg != 32643:
    raise RuntimeError(f'expected EPSG:32643 to be the best aligned CRS, got EPSG:{native_epsg}')
districts=[(f['properties']['district_id'], g) for f, g in zip(district_features, district_geoms)]

records=[]
for f in building_features:
    g=make_valid(shape(f['geometry']))
    if g.geom_type == 'GeometryCollection':
        parts=[p for p in g.geoms if p.geom_type in ('Polygon','MultiPolygon')]
        g=max(parts, key=lambda p:p.area) if parts else g
    records.append((str(f['properties']['building_id']), g))
records.sort(key=lambda x:x[0])
seen_ids=set(); seen_wkb=set(); clean=[]
for bid,g in records:
    wkb=to_wkb(normalize(g), hex=True)
    if bid in seen_ids or wkb in seen_wkb:
        continue
    seen_ids.add(bid); seen_wkb.add(wkb); clean.append((bid,g))

features=[]; summary={did:[] for did,_ in districts}
for bid,g in clean:
    overlaps=[]
    for did,dg in districts:
        a=g.intersection(dg).area
        if a >= 0.1:
            overlaps.append((a,did))
    overlaps.sort(key=lambda x:(-x[0], x[1]))
    if len(overlaps)>1 and abs(overlaps[0][0]-overlaps[1][0]) < 0.01:
        maxa=overlaps[0][0]
        did=sorted(d for a,d in overlaps if abs(a-maxa)<0.01)[0]
    else:
        did=overlaps[0][1]
    area=round(g.area,2)
    summary[did].append(area)
    features.append({"type":"Feature","properties":{"building_id":bid,"district_id":did,"area_m2":area},"geometry":mapping(g)})

out={"type":"FeatureCollection","name":"clean_buildings","crs":{"type":"name","properties":{"name":"EPSG:32643"}},"features":features}
(APP/'clean_buildings.geojson').write_text(json.dumps(out,indent=2))
with (APP/'district_summary.csv').open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['district_id','building_count','total_building_area_m2','average_building_area_m2'])
    w.writeheader()
    for did in sorted(summary):
        vals=summary[did]
        total=round(sum(vals),2); avg=round(total/len(vals),2) if vals else 0.00
        w.writerow({'district_id':did,'building_count':len(vals),'total_building_area_m2':f'{total:.2f}','average_building_area_m2':f'{avg:.2f}'})
