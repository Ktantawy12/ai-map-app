import streamlit as st
import folium
from streamlit.components.v1 import html

from app.agent import run_graph


st.set_page_config(page_title="AI Map App", layout="wide")
st.title("AI Map Query System")



query = st.text_input(
    "Ask a map question",
    ""
)
run = st.button("Search")

m = folium.Map(location=[52.52, 13.405], zoom_start=11)

if run and query.strip():
    result = run_graph(query.strip())

    if not result.get("ok"):
        st.error(result.get("error", "Agent failed"))
        with st.expander("Debug steps"):
            st.json(result.get("steps", []))
    else:
        geo = result["geo"]
        poly = result["polygon"]
        features = result["layer"]["features"]
        parsed = result["parsed"]

        st.success(f"{parsed['layer_type']} within {parsed['radius_km']} km of {geo['place_name']}")
        st.write(f"Showing {len(features)} results")


        m = folium.Map(location=[geo["lat"], geo["lon"]], zoom_start=13)
        folium.Marker([geo["lat"], geo["lon"]], popup=geo["place_name"]).add_to(m)

        latlon_ring = [[p[1], p[0]] for p in poly["coordinates"][0]]
        folium.Polygon(latlon_ring).add_to(m)

        for feat in features:
            lon, lat = feat["geometry"]["coordinates"]
            name = feat["properties"].get("name", parsed["layer_type"])
            folium.Marker([lat, lon], popup=name).add_to(m)

        with st.expander("Agent steps"):
            st.json(result["steps"])

html(m.get_root().render(), height=600)
