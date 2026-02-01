# AI Map Agent

##  Overview

---


##  System Architecture

The system separates reasoning from execution.

User Query ->
  LLM ->
MCP Tool Layer ->
Geospatial Processing ->
Streamlit Map Interface
---

##  Core Components
  
### 1 LLM Reasoning Layer

The LLM is responsible for extracting:

* layer_type

* location

* radius_km

* Constructing structured tool calls

The model does not perform geospatial computation directly.

This prevents hallucination and enforces execution correctness.

### 2 MCP Tool Server

The project exposes geospatial tools via MCP:

* geocode_address_tool

* buffer_point_tool

* retrieve_geodata_layer_tool

Each tool:

* Has a defined schema

* Is independently testable

* Returns structured outputs

* Can be reused across agents

This design mirrors real-world AI agent orchestration systems.

### 3 Geospatial Pipeline

Address → Coordinates

Coordinates → Buffer (GeoJSON Polygon)

Polygon → Bounding Box

Bounding Box → OSM Feature Query

Spatial logic is deterministic and separated from the LLM.

### 4 Frontend (Streamlit)

Features:

* Interactive natural language input

* Map rendering via Folium

* Debug visibility (agent steps)

* Polygon visualization

---


## Technologies

* Python 

* Streamlit

* OpenAI API (LLM orchestration)

* Mapbox API (map tiles)

* OpenStreetMap (geodata source)

* FastMCP (tool server framework)

* Folium (map visualization)

* GeoJSON

---


## Data Sources
  
| Source | Purpose |
|--------|---------|
| OpenStreetMap | Geospatial features |
| OpenAI API | Natural language parsing |
| Mapbox | Interactive tiles |

---

##  Challenges & Solutions

---

##  Example Workflow

Input:

“Find 5 hospitals within 2km of Potsdamer Platz.”

Execution:

LLM parses:

layer_type: hospital

radius_km: 2

location: Potsdamer Platz

Geocode → Coordinates

Buffer → GeoJSON polygon

Bounding box → OSM query

Render interactive map

---

## Installation

```bash
git clone https://github.com/Ktantawy12/ai-map-app.git
cd ai-map-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_key
MAPBOX_API_KEY=your_key
```

---

## ▶ Run

```bash
streamlit run app/main.py
```

---

## Author

Karim Tantawy
AI & Data Engineer
Berlin / Egypt




