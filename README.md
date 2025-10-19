Microburbs Mini Explorer

A clean, data-driven property insights dashboard built to visualise real-time property data from the Microburbs API. It helps users explore suburb-level metrics such as median prices, dwelling sizes, and market distribution in a simple, interactive way.

Phase 1: Foundation Setup

What’s working

Flask server running locally on port 5001

Polished frontend designed in UX Pilot

Static files served correctly with responsive layout

Tailwind CSS for styling and modern UI components

Hover effects, smooth animations, and Highcharts integration

Current features

Header with suburb search, property-type dropdown, and run button

KPI cards showing key suburb stats (using placeholder data initially)

Price distribution chart built with Highcharts

Six sample property cards with price, address, and property details

Consistent use of Poppins font and custom colour palette

Stack

Backend: Flask

Frontend: Vanilla JavaScript + Tailwind CSS

Charts: Highcharts

Icons: Font Awesome

Fonts: Google Fonts (Poppins)

Run locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py


App runs at: http://localhost:5001

Phase 2: Backend API Integration

What’s working

Integrated with the Microburbs Sandbox API using secure token auth

Added data parsing and validation for property listings

Calculated medians for price, bedrooms, and land size

Built histogram generation for price distribution

Added error handling for malformed or missing API fields

Key endpoint
GET /api/suburb/properties
Parameters: suburb (required), property_type (optional)
Returns: Summary metrics and property listings

Example response

{
  "summary": {
    "count": 8,
    "median_price": 1098750,
    "median_bedrooms": 4,
    "median_land_sqm": 607,
    "price_bins": [...]
  },
  "listings": [...]
}

Phase 3: Frontend Data Integration

What’s working

Frontend now connected to live backend data

KPI cards, charts, and listings update automatically

Highcharts visualises live price ranges per suburb

Property cards generated dynamically from API results

Added loading spinners and clear error messages

User flow

Enter a suburb name (e.g. “Belmont North”).

Click “Run Analysis.”

The dashboard updates with live metrics, chart, and property listings.

Phase 4: Final Polish

What’s working

Fully dynamic property cards with address, price, bedrooms, bathrooms, and land size

Improved formatting and spacing for clarity

Responsive grid layout for all screen sizes

Refined transitions, hover states, and loading indicators

Graceful error handling for any failed API calls

Complete feature set

Live data from Microburbs API

Calculated medians for key property stats

Interactive chart visualising local price segments

Responsive design and clean, modern interface

Smooth animations and well-defined loading states

Final Summary

The Microburbs Mini Explorer is a fully functional prototype showing how complex property data can be made simple and intuitive for investors. It combines a clean, responsive frontend with live API data, statistical analysis, and clear visual feedback — a practical foundation for a scalable property insights tool.

**Note**: This is a demonstration project for the Microburbs Analyst Developer position, showcasing the ability to create a professional, data-driven property insights dashboard.
