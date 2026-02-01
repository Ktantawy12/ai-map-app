import requests

OVERPASS_URLS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.nchc.org.tw/api/interpreter",
]

LAYER_MAP = {
    "cafe": ("amenity", "cafe"),
    "restaurant": ("amenity", "restaurant"),
    "hospital": ("amenity", "hospital"),
    "pharmacy": ("amenity", "pharmacy"),
    "school": ("amenity", "school"),
    "bank": ("amenity", "bank"),
    "fuel": ("amenity", "fuel"),
    "supermarket": ("shop", "supermarket"),
    "park": ("leisure", "park"),
}

def retrieve_geodata_layer(layer_type: str, bbox: dict, data_source: str = "osm") -> dict:
    # Keep interface stable even if we later add mapbox backend
    if data_source != "osm":
        return {"ok": True, "type": "FeatureCollection", "features": []}

    if layer_type not in LAYER_MAP:
        return {"ok": False, "error": f"Unsupported layer_type '{layer_type}'"}

    # bbox validation
    try:
        min_lat = float(bbox["min_lat"]); min_lon = float(bbox["min_lon"])
        max_lat = float(bbox["max_lat"]); max_lon = float(bbox["max_lon"])
    except Exception:
        return {"ok": False, "error": "Invalid bbox format"}

    if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        return {"ok": False, "error": "Invalid bbox latitude"}
    if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
        return {"ok": False, "error": "Invalid bbox longitude"}
    if min_lat > max_lat or min_lon > max_lon:
        return {"ok": False, "error": "Invalid bbox ordering (min > max)"}

    key, val = LAYER_MAP[layer_type]

    query = f"""
    [out:json][timeout:60];
    (
      node["{key}"="{val}"]({min_lat},{min_lon},{max_lat},{max_lon});
      way["{key}"="{val}"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation["{key}"="{val}"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out center;
    """

    last_error = None
    data = None

    for url in OVERPASS_URLS:
        try:
            r = requests.post(url, data=query.encode("utf-8"), timeout=90)
            if r.status_code == 200:
                data = r.json()
                break
            last_error = f"{url} -> HTTP {r.status_code}"
        except Exception as e:
            last_error = f"{url} -> {str(e)}"

    if data is None:
        return {"ok": False, "error": f"All Overpass endpoints failed. Last: {last_error}"}

    features = []
    MAX_RESULTS = 60

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name", layer_type)

        if el.get("type") == "node":
            lat = el.get("lat")
            lon = el.get("lon")
        else:
            center = el.get("center")
            if not center:
                continue
            lat = center.get("lat")
            lon = center.get("lon")

        if lat is None or lon is None:
            continue

        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"name": name, "layer_type": layer_type},
        })

        if len(features) >= MAX_RESULTS:
            break

    return {"ok": True, "type": "FeatureCollection", "features": features}

