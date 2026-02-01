AI Map Agent – Geospatial Intelligence Assistant

An AI-powered geospatial assistant that combines Large Language Models with real-world mapping data to answer spatial questions, retrieve geodata layers, and perform geographic analysis such as buffering and feature extraction.

 Project Overview

AI Map Agent enables users to:

Convert natural language into spatial queries

Geocode addresses into coordinates

Create geographic buffers

Retrieve geospatial features (e.g., schools, hospitals, restaurants)

Visualize results interactively on a map

Control number of returned results via UIArchitecture

The system follows a modular tool-driven architecture:

User Query
     ↓
LLM (Query Parsing & Planning)
     ↓
MCP Tool Layer
     ↓
Geospatial Processing
     ↓
Streamlit UI Visualization

Core Components

LLM Layer – Parses user intent into structured tool calls

MCP Server – Exposes geospatial tools as callable functions

Geospatial Tools

Geocoding

Buffer creation

Layer retrieval (OpenStreetMap)

Streamlit Frontend – Interactive UI & map rendering

🛠️ Technologies Used

Python 3.11+

Streamlit

OpenAI API

Mapbox API

OpenStreetMap (OSM)

FastMCP

GeoJSON

Requests / Geospatial utilities

🔍 Features
1️⃣ Natural Language Spatial Queries

Users can ask:

“Find 10 restaurants within 2km of Alexanderplatz”

The LLM:

Extracts location

Determines radius

Identifies layer type

Controls result count

2️⃣ Geocoding Tool

Converts address → latitude & longitude.

3️⃣ Buffer Tool

Creates a GeoJSON polygon around a coordinate with configurable radius (km).

4️⃣ Geodata Retrieval

Retrieves features from OSM within bounding box constraints.

5️⃣ Result Control (UI Feature)

Users can select:

Number of returned results

Radius size

Layer type

📁 Repository Structure
ai-map-app/
│
├── app/
│   ├── main.py                # Streamlit entry point
│   ├── agent.py               # LLM orchestration
│   ├── tools/
│   │   ├── tool1_geocode.py
│   │   ├── tool2_retrieve_layer.py
│   │   └── tool3_buffer.py
│
├── mcp_server.py              # MCP tool server
├── requirements.txt
├── .env (not tracked)
└── README.md

🔑 API Configuration

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_key
MAPBOX_API_KEY=your_mapbox_key


⚠️ .env is excluded from Git tracking.

▶️ How to Run Locally
1️⃣ Clone repository
git clone https://github.com/Ktantawy12/ai-map-app.git
cd ai-map-app

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run application
streamlit run app/main.py

📊 Data Sources

OpenStreetMap (OSM) for geospatial features

OpenAI API for LLM-based parsing and planning

Mapbox for map visualization

🧩 Design Decisions
Tool-Based Architecture

Separated reasoning (LLM) from execution (geospatial tools).

This ensures:

Modularity

Extensibility

Easy debugging

Clear separation of concerns

MCP Integration

Tools are exposed via MCP, enabling structured function calling from the LLM.

Stateless Design

Each request is processed independently for clarity and reproducibility.

⚠️ Challenges & Solutions
1. Natural Language Ambiguity

Handled via structured tool schema and controlled parsing.

2. Bounding Box Accuracy

Implemented buffer-to-bbox conversion to ensure correct OSM queries.

3. API Key Security

Excluded .env from version control and enforced local loading.

4. Large Repo Size

Removed venv/ and unnecessary files to ensure clean submission.

📹 Demo Video

A short demo video is attached in this repository README (see below).




👤 Author

Karim Tantawy
AI & Data Engineer
Berlin / Egypt



