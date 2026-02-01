import math

def buffer_point(latitude: float, longitude: float, radius_km: float, n_points: int = 64) -> dict:
    """
    Tool 3: Returns a GeoJSON Polygon representing a buffer around a point.

    - Output is always a valid GeoJSON Polygon:
      { "type": "Polygon", "coordinates": [ [ [lon, lat], ... ] ] }
    - Ring is closed (first point == last point)
    - Coordinates are [lon, lat]
    """
    # Basic validation
    if not (-90 <= latitude <= 90):
        return {"ok": False, "error": "Invalid latitude"}
    if not (-180 <= longitude <= 180):
        return {"ok": False, "error": "Invalid longitude"}
    if radius_km <= 0:
        return {"ok": False, "error": "radius_km must be > 0"}

    # Convert km to degrees (approx)
    lat_rad = math.radians(latitude)
    deg_lat = radius_km / 110.574
    cos_lat = math.cos(lat_rad)
    deg_lon = radius_km / (111.320 * cos_lat) if abs(cos_lat) > 1e-12 else 0.0

    ring = []
    for i in range(n_points):
        ang = 2 * math.pi * i / n_points
        lat = latitude + deg_lat * math.sin(ang)
        lon = longitude + deg_lon * math.cos(ang)
        ring.append([lon, lat])

    # Close ring
    if ring[0] != ring[-1]:
        ring.append(ring[0])

    poly = {"type": "Polygon", "coordinates": [ring]}

    # Optional sanity check
    if len(poly["coordinates"][0]) < 4:
        return {"ok": False, "error": "Polygon ring too small"}

    return {"ok": True, **poly}
