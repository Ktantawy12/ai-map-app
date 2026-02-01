AI Map Agent

* Overview

  

* System Architecture

The system separates reasoning from execution.

User Query ->
  LLM ->
MCP Tool Layer ->
Geospatial Processing ->
Streamlit Map Interface

* Architectural Principles

Tool-based modular design

Deterministic geospatial operations

Explicit schema-driven LLM parsing

Clean separation of concerns

Extendable to multi-tool workflows

* Core Components
  
1 LLM Reasoning Layer

The LLM is responsible only for:

Extracting:

layer_type

location

radius_km

result_limit

Constructing structured tool calls

The model does not perform geospatial computation directly.

This prevents hallucination and enforces execution correctness.

2 MCP Tool Server

The project exposes geospatial tools via MCP:

geocode_address_tool

buffer_point_tool

retrieve_geodata_layer_tool

Each tool:

Has a defined schema

Is independently testable

Returns structured outputs

Can be reused across agents

This design mirrors real-world AI agent orchestration systems.

3 Geospatial Pipeline

Address → Coordinates

Coordinates → Buffer (GeoJSON Polygon)

Polygon → Bounding Box

Bounding Box → OSM Feature Query

Feature Truncation (User-Controlled Limit)

Spatial logic is deterministic and separated from the LLM.

4 Frontend (Streamlit)

Features:

Interactive natural language input

Adjustable result slider

Map rendering via Folium

Debug visibility (agent steps)

Polygon visualization

Feature markers with popups




* Technologies

Python 

Streamlit

OpenAI API (LLM orchestration)

Mapbox API (map tiles)

OpenStreetMap (geodata source)

FastMCP (tool server framework)

Folium (map visualization)

GeoJSON



* Data Sources
Source	           Purpose
OpenStreetMap	  Geospatial features
OpenAI API	     Natural language parsing & planning
Mapbox	           Interactive map tiles

* Challenges & Solutions

* Example Workflow

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

Limit → 5 results

Render interactive map

* Running the Project
Clone
git clone https://github.com/Ktantawy12/ai-map-app.git
cd ai-map-app

Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Environment Variables

Create .env:

OPENAI_API_KEY=your_key
MAPBOX_API_KEY=your_key

Run
streamlit run app/main.py


Author

Karim Tantawy
AI & Data Engineer
Berlin / Egypt

