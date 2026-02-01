
from typing import Dict, Any, Callable

from llm import llm_parse_query
from app.mcp_local.mcp_client import LocalMCPClient
mcp = LocalMCPClient()



def polygon_bbox(poly_geojson: Dict[str, Any]) -> Dict[str, float]:
    ring = poly_geojson.get("coordinates", [[]])[0]
    lons = [pt[0] for pt in ring]
    lats = [pt[1] for pt in ring]
    return {
        "min_lat": float(min(lats)),
        "min_lon": float(min(lons)),
        "max_lat": float(max(lats)),
        "max_lon": float(max(lons)),
    }

# ---- Nodes ----
def node_llm(state: Dict[str, Any]) -> Dict[str, Any]:
    out = llm_parse_query(state["query"])
    if not out.get("ok"):
        return {**state, "ok": False, "error": out.get("error"), "steps": state["steps"] + [{"node":"llm", "error": out.get("error")}]}
    return {**state, "ok": True, "parsed": out, "steps": state["steps"] + [{"node":"llm", "output": out}]}

def node_geocode(state):
    place = state["parsed"]["place"]
    res = mcp.call("geocode_address_tool", {"address": place})

    if not res.get("ok"):
        return {**state, "ok": False, "error": res.get("error"),
                "steps": state["steps"] + [{"node":"geocode", "error": res.get("error")}]}

    lat = res.get("lat", res.get("latitude"))
    lon = res.get("lon", res.get("longitude"))
    if lat is None or lon is None:
        return {**state, "ok": False, "error": "Geocoder returned no coordinates",
                "steps": state["steps"] + [{"node":"geocode","error":"no coords"}]}

    out = {"lat": float(lat), "lon": float(lon), "place_name": res.get("display_name", place)}
    return {**state, "ok": True, "geo": out, "steps": state["steps"] + [{"node":"geocode","output": out}]}


    # normalize keys (some versions return lat/lon, some latitude/longitude)
    lat = geo.get("lat", geo.get("latitude"))
    lon = geo.get("lon", geo.get("longitude"))
    place_name = geo.get("place_name", geo.get("display_name", parsed["place"]))

    if lat is None or lon is None:
        return {**state, "ok": False, "error": "Geocoder returned no coordinates", "steps": state["steps"] + [{"node":"geocode", "error":"no coords"}]}

    out = {"lat": float(lat), "lon": float(lon), "place_name": place_name}
    return {**state, "ok": True, "geo": out, "steps": state["steps"] + [{"node":"geocode", "output": out}]}

def node_buffer(state):
    lat, lon = state["geo"]["lat"], state["geo"]["lon"]
    r = state["parsed"]["radius_km"]
    poly = mcp.call("buffer_point_tool", {"latitude": lat, "longitude": lon, "radius_km": r})

    if not (isinstance(poly, dict) and poly.get("type") == "Polygon"):
        return {**state, "ok": False, "error": "Buffer tool returned invalid polygon",
                "steps": state["steps"] + [{"node":"buffer","error":"invalid polygon"}]}

    bbox = polygon_bbox(poly)
    return {**state, "ok": True, "polygon": poly, "bbox": bbox,
            "steps": state["steps"] + [{"node":"buffer","output":{"radius_km": r}}, {"node":"bbox","output": bbox}]}


def node_retrieve(state):
    layer_type = state["parsed"]["layer_type"]
    bbox = state["bbox"]
    res = mcp.call("retrieve_geodata_layer_tool", {"layer_type": layer_type, "bbox": bbox, "data_source": "osm"})

    if not res.get("ok"):
        return {**state, "ok": False, "error": res.get("error"),
                "steps": state["steps"] + [{"node":"retrieve","error": res.get("error")}]}

    features = (res.get("features") or [])[:60]
    out = {"type": "FeatureCollection", "features": features}
    return {**state, "ok": True, "layer": out,
            "steps": state["steps"] + [{"node":"retrieve","output":{"returned": len(res.get("features", [])), "showing": len(features)}}]}



NODES: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "llm": node_llm,
    "geocode": node_geocode,
    "buffer": node_buffer,
    "retrieve": node_retrieve,
}

EDGES = {
    "llm": "geocode",
    "geocode": "buffer",
    "buffer": "retrieve",
    "retrieve": None,
}

def run_graph(query: str) -> Dict[str, Any]:
    state: Dict[str, Any] = {"query": query, "ok": True, "steps": []}

    current = "llm"
    while current:
        state = NODES[current](state)
        if not state.get("ok"):
            return state
        current = EDGES[current]

    return state
