
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from app.tools.tool1_geocode import geocode_address
from app.tools.tool2_retrieve_layer import retrieve_geodata_layer
from app.tools.tool3_buffer import buffer_point

mcp = FastMCP("map-agent-tools")

@mcp.tool()
def geocode_address_tool(address: str) -> Dict[str, Any]:
    """
    MCP tool wrapper for geocoding.
    Input: address string
    Output: dict with lat/lon + display name (your current schema)
    """
    return geocode_address(address)

@mcp.tool()
def buffer_point_tool(latitude: float, longitude: float, radius_km: float) -> Dict[str, Any]:
    """
    MCP tool wrapper for buffer creation.
    Output: GeoJSON Polygon
    """
    return buffer_point(latitude, longitude, radius_km)

@mcp.tool()
def retrieve_geodata_layer_tool(layer_type: str, bbox: Dict[str, float], data_source: str = "osm") -> Dict[str, Any]:
    """
    MCP tool wrapper for layer retrieval.
    Output: dict containing ok + features (your current schema)
    """
    return retrieve_geodata_layer(layer_type=layer_type, bbox=bbox, data_source=data_source)

if __name__ == "__main__":
    # Runs as an MCP server over stdio by default
    mcp.run()
