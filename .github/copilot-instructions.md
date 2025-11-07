# DevOps_DevNet Project Guide for AI Agents

## Project Overview
This project is a collection of Python applications focused on network automation, DevOps practices, and API integrations. The codebase includes multiple independent applications demonstrating different aspects of modern network and API programming.

## Project Structure
The project is organized into several key parts:
- `2.1 Lab/`: Network automation scripts using netmiko for Cisco devices
- `Part3/`, `Part4/`: Basic Python programming concepts and file operations
- `Part5/`: Collection of web applications demonstrating API integrations:
  - `ISS/`: Real-time ISS tracking using Flask and Leaflet.js
  - `MapQuest/`: Navigation app using MapQuest API
  - `StockData_ExpertAPI/`: Stock market data analyzer using FastAPI

## Key Patterns and Conventions

### Web Applications (Part5/)
- Flask-based applications follow a common structure:
  ```
  AppName/
  ├── app.py          # Main Flask application
  ├── *_logic.py      # Business logic (if applicable)
  └── templates/
      └── index.html  # Frontend template
  ```
- FastAPI applications (StockData_ExpertAPI) use async/await pattern for API calls
- Environment variables are used for API keys and sensitive data

### Network Automation (2.1 Lab/)
- Netmiko is used for Cisco device automation
- Device credentials and connection details are typically stored in separate configuration files

## Development Setup

### Python Environment Setup
1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies based on the specific application:
   - For web apps: `pip install Flask requests Flask-CORS`
   - For network automation: `pip install netmiko`
   - For FastAPI apps: `pip install fastapi uvicorn httpx python-dotenv`

### Running Applications
- Flask applications: `python app.py` from the application directory
- FastAPI applications: `uvicorn main:app --reload`
- Network automation scripts: Run directly with Python after configuring device details

## Integration Points
- External APIs used:
  - Open Notify API (ISS Tracker)
  - MapQuest Directions API (MapQuest Navigator)
  - Polygon.io API (StockData_ExpertAPI)
  - Cisco devices via SSH (Network Automation)

## Common Patterns
- API calls are typically wrapped in try-except blocks with specific error handling
- Web applications use templates for frontend rendering
- Configuration values are separated from application code
- Modular design with separate files for business logic and API handling