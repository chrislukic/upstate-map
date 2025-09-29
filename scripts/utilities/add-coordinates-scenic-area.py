import json
import math
import time
import requests
from urllib.parse import urlencode
from shapely.geometry import shape, mapping, MultiPolygon, Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid

ARCGIS_PORTAL_ITEM = "bb2dfa2ccec0462ebe40e4efd8e2252f"  # NY State Parks Property (OPRHP)
PORTAL_ITEM_URL = f"https://www.arcgis.com/sharing/rest/content/items/{ARCGIS_PORTAL_ITEM}?f=pjson"
PORTAL_DATA_URL = f"https://www.arcgis.com/sharing/rest/content/items/{ARCGIS_PORTAL_ITEM}/data?f=pjson"

TARGETS = [
    {
        "id": "hudson_highlands_east_bank",
        "unit_names_like": [
            "HUDSON HIGHLANDS STATE PARK%",
            "HUDSON HIGHLANDS SP%"
        ],
        "properties": {
            "name": "Hudson Highlands State Park Preserve (east bank)",
            "region": "Hudson Valley",
            "category": "mountain_region",
            "score": 8.6,
            "tags": ["river-views","short-steep","scrambles","train-access"],
            "nearby_hubs": ["Cold Spring","Beacon","Peekskill"]
        }
    },
    {
        "id": "hudson_highlands_west_bank",
        "unit_names_like": [
            "STORM KING STATE PARK%"
        ],
        "properties": {
            "name": "Storm King State Park (west bank anchor)",
            "region": "Hudson Valley",
            "category": "mountain_region",
            "score": 8.2,
            "tags": ["ridge-views","river-views","scrambles"],
            "nearby_hubs": ["Cornwall-on-Hudson","Newburgh"]
        }
    }
]

def fetch_json(url, params=None):
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()

def portal_item_to_layer_url():
    # Resolve the FeatureServer URL from the ArcGIS item
    meta = fetch_json(PORTAL_ITEM_URL)
    # Some items expose the service URL in "url". If not, try /data
    if "url" in meta:
        return meta["url"]
    data = fetch_json(PORTAL_DATA_URL)
    # Look for a FeatureServer URL in the data blob
    for k, v in data.items():
        if isinstance(v, str) and "FeatureServer" in v:
            return v
        if isinstance(v, list):
            for itm in v:
                if isinstance(itm, dict):
                    for vv in itm.values():
                        if isinstance(vv, str) and "FeatureServer" in vv:
                            return vv
    raise RuntimeError("Could not resolve FeatureServer URL from portal item.")

def query_features(feature_server_url, where_like_clauses):
    # Try each LIKE clause until we get features
    layer0 = feature_server_url.rstrip("/") + "/0"
    for like in where_like_clauses:
        # Try both Name and Label fields
        for field in ["Name", "Label"]:
            where = f"UPPER({field}) LIKE '{like}'"
            params = {
                "where": where,
                "outFields": "*",
                "f": "geojson",
                "returnGeometry": "true",
                "outSR": 4326
            }
            resp = fetch_json(layer0 + "/query", params)
            feats = resp.get("features", [])
            if feats:
                return feats, where
    return [], None

def explore_service_structure(feature_server_url):
    """Explore the service structure to understand available fields and data"""
    layer0 = feature_server_url.rstrip("/") + "/0"
    
    # First, get service metadata
    try:
        metadata = fetch_json(layer0 + "?f=json")
        print(f"Service metadata:")
        print(f"  Name: {metadata.get('name', 'Unknown')}")
        print(f"  Type: {metadata.get('type', 'Unknown')}")
        print(f"  Geometry Type: {metadata.get('geometryType', 'Unknown')}")
        
        # Get field information
        fields = metadata.get('fields', [])
        print(f"  Available fields ({len(fields)}):")
        for field in fields[:10]:  # Show first 10 fields
            print(f"    - {field.get('name', 'Unknown')} ({field.get('type', 'Unknown')})")
        if len(fields) > 10:
            print(f"    ... and {len(fields) - 10} more fields")
            
    except Exception as e:
        print(f"Error getting service metadata: {e}")
    
    # Try to get a small sample of data
    try:
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
            "returnGeometry": "false",
            "outSR": 4326,
            "resultRecordCount": 5
        }
        
        resp = fetch_json(layer0 + "/query", params)
        features = resp.get("features", [])
        print(f"\nSample data ({len(features)} features):")
        
        if features:
            # Show the first feature's attributes
            attrs = features[0].get("attributes", {})
            print("  First feature attributes:")
            for key, value in list(attrs.items())[:10]:  # Show first 10 attributes
                print(f"    {key}: {value}")
            if len(attrs) > 10:
                print(f"    ... and {len(attrs) - 10} more attributes")
        else:
            print("  No features found in the service")
            
    except Exception as e:
        print(f"Error getting sample data: {e}")
    
    return features

def explore_park_names(feature_server_url, search_terms=None):
    """Explore what park names are available in the service"""
    layer0 = feature_server_url.rstrip("/") + "/0"
    
    # Get a sample of all park names using both Name and Label fields
    params = {
        "where": "1=1",
        "outFields": "Name,Label",
        "f": "json",
        "returnGeometry": "false",
        "outSR": 4326,
        "resultRecordCount": 1000
    }
    
    resp = fetch_json(layer0 + "/query", params)
    all_parks = []
    for f in resp.get("features", []):
        attrs = f["attributes"]
        name = attrs.get("Name", "")
        label = attrs.get("Label", "")
        if name:
            all_parks.append(name)
        if label and label != name:
            all_parks.append(label)
    
    print(f"Found {len(all_parks)} total park names in the service")
    
    if search_terms:
        print(f"\nSearching for parks containing: {search_terms}")
        matching_parks = []
        for term in search_terms:
            matches = [p for p in all_parks if term.upper() in p.upper()]
            matching_parks.extend(matches)
            if matches:
                print(f"  '{term}' matches: {matches}")
        
        if not matching_parks:
            print("  No matches found. Here are some similar park names:")
            for term in search_terms:
                similar = [p for p in all_parks if any(word in p.upper() for word in term.upper().split())]
                if similar:
                    print(f"  Similar to '{term}': {similar[:5]}")  # Show first 5 matches
    
    return all_parks

def dissolve_features(features):
    geoms = []
    for f in features:
        g = shape(f["geometry"])
        # Fix invalid rings if any
        g = make_valid(g)
        # Force to MultiPolygon
        if isinstance(g, Polygon):
            g = MultiPolygon([g])
        geoms.append(g)
    dissolved = unary_union(geoms)
    # Ensure MultiPolygon output
    if isinstance(dissolved, Polygon):
        dissolved = MultiPolygon([dissolved])
    return dissolved

def simplify_geom(geom, tolerance):
    # Preserve topology (Shapely >=2.0 uses GEOS preserve topology by default)
    return geom.simplify(tolerance, preserve_topology=True)

def centroid_label_point(geom):
    c = geom.representative_point()  # better for label placement than pure centroid
    return [c.x, c.y]

def bbox(geom):
    minx, miny, maxx, maxy = geom.bounds
    return [minx, miny, maxx, maxy]

def feature_template(fid, props, geom, source_note, where_used, lod=None):
    p = {
        **props,
        "style": {"fill": "#d6a62e", "stroke": "#d6a62e"},
        "source": {
            "authority": "NYS OPRHP — NY State Parks Property (boundaries)",
            "portal_item": ARCGIS_PORTAL_ITEM,
            "where_clause": where_used,
            "fetched_at": time.strftime("%Y-%m-%d"),
            "notes": source_note
        },
        "stats": {
            "area_km2": round(geom.area * (111.32**2), 2)  # rough WGS84 planar approx; good enough for relative display
        },
        "lod": lod or "full",
        "label_point": centroid_label_point(geom)
    }
    return {
        "type": "Feature",
        "id": f"{fid}__{p['lod']}",
        "properties": p,
        "bbox": bbox(geom),
        "geometry": mapping(geom)
    }

def main():
    try:
        print("Fetching ArcGIS portal item metadata...")
        fs_url = portal_item_to_layer_url()
        print(f"FeatureServer URL: {fs_url}")
        
        # First, explore the service structure
        print("\nExploring service structure...")
        sample_features = explore_service_structure(fs_url)
        
        # Then explore what park names are available
        search_terms = ["HUDSON HIGHLANDS", "STORM KING"]
        all_parks = explore_park_names(fs_url, search_terms)
        
        out_features = []
        for target in TARGETS:
            print(f"\nProcessing {target['id']}...")
            feats, where = query_features(fs_url, target["unit_names_like"])
            if not feats:
                print(f"WARNING: No features returned for {target['id']} using clauses {target['unit_names_like']}")
                continue
            print(f"Found {len(feats)} features for {target['id']}")
            dissolved = dissolve_features(feats)

            # LODs tuned for web maps (adjust to suit your max zoom)
            lods = [
                ("full", 0.0),
                ("z8_10", 0.005),
                ("z<=7", 0.01)
            ]
            for lod_name, tol in lods:
                geom = dissolved if tol == 0 else simplify_geom(dissolved, tol)
                out_features.append(
                    feature_template(
                        target["id"],
                        target["properties"],
                        geom,
                        "Geometry dissolved from authoritative park parcels; non-contiguous areas preserved.",
                        where_used=where,
                        lod=lod_name
                    )
                )

        if not out_features:
            raise RuntimeError("No features were generated. Check your TARGETS configuration.")

        fc = {
            "type": "FeatureCollection",
            "name": "hudson_highlands_granular",
            "crs": {"type":"name","properties":{"name":"EPSG:4326"}},
            "features": out_features
        }

        # Write to the correct location in the project structure
        output_path = "../../public/data/scenic-areas/hudson-highlands.geojson"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(fc, f, ensure_ascii=False, indent=2)

        print(f"Wrote {output_path} with {len(out_features)} features (3 LODs x 2 parks).")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
