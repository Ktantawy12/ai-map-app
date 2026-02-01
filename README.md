# AI Map Agent  

## Overview

The AI Map Agent enables users to ask natural language spatial questions such as:

> “Find 5 hospitals within 2km of Potsdamer Platz.”

The system parses intent using an LLM, delegates execution to structured tools via MCP, performs deterministic geospatial processing, and renders results in an interactive Streamlit interface.

---
## Demo Video

https://github.com/Ktantawy12/ai-map-app/releases/tag/v1.0.0
---

## System Architecture

The system strictly separates reasoning from execution.

```
User Query 
    ↓
LLM 
    ↓
MCP Tool Layer
    ↓
Geospatial Processing
    ↓
Streamlit Map Interface
```

### Design Principle

The LLM does **not** perform geospatial computation.  
It only extracts structured parameters.  
All spatial logic is deterministic and tool-driven.

This prevents hallucination and ensures execution correctness.

---

## Core Components

### 1) LLM Reasoning Layer

Responsible for extracting:

- `layer_type`
- `location`
- `radius_km`

And constructing structured tool calls.

The model:
- Does not calculate distances
- Does not query OSM directly
- Does not generate spatial geometry

This enforces strict reasoning-execution separation.

---

### 2) MCP Tool Server

Geospatial tools are exposed via **FastMCP**:

- `geocode_address_tool`
- `buffer_point_tool`
- `retrieve_geodata_layer_tool`

Each tool:

- Has a defined schema
- Is independently testable
- Returns structured outputs
- Can be reused across agents
- Runs over stdio via MCP

This mirrors production-grade AI orchestration systems.

---

### 3) Geospatial Pipeline

Deterministic spatial processing:

```
Address → Coordinates
Coordinates → Buffer (GeoJSON Polygon)
Polygon → Bounding Box
Bounding Box → OSM Feature Query
```

Key characteristics:

- No LLM in execution loop
- GeoJSON-compliant outputs
- Spatial operations isolated from reasoning

---

### 4) Frontend (Streamlit)

Features:

- Natural language input
- Interactive map rendering via Folium
- Adjustable result slider
- Polygon visualization
- Agent step debug panel
- Structured execution trace visibility

This ensures transparency and explainability.

---

## Technologies Used

- Python 3.11
- Streamlit
- OpenAI API (LLM orchestration)
- Mapbox API (map tiles)
- OpenStreetMap (geodata source)
- FastMCP (tool server framework)
- Folium (map visualization)
- GeoJSON

---

## Data Sources

| Source | Purpose |
|--------|---------|
| OpenStreetMap | Geospatial feature retrieval |
| OpenAI API | Natural language parsing |
| Mapbox | Geocoding |

---

## Example Workflow

### Input

> “Find hospitals within 2km of Potsdamer Platz.”

### Execution

1. LLM parses:
   - `layer_type`: hospital  
   - `radius_km`: 2  
   - `location`: Potsdamer Platz  

2. Geocode → Coordinates  
3. Buffer → GeoJSON polygon  
4. Bounding box → OSM query  
5. Render interactive map  

---

## Challenges & Solutions

### 1) LLM Hallucination Risk  
**Solution:**  
Strict separation between reasoning and execution.  
The LLM only extracts structured parameters.

---

### 4) API Key Security  
**Solution:**  
Environment-based configuration via `.env` and exclusion from Git tracking.

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

## Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_key
MAPBOX_API_KEY=your_key
```

---

## Run

```bash
streamlit run app/main.py
```

---


## Author

Karim Tantawy  
AI & Data Engineer  




