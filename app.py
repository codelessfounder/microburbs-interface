from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import math
from statistics import median
from urllib.parse import urlencode
import requests

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Microburbs API configuration
API_BASE = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = os.getenv("MICROBURBS_TOKEN", "test")  # sandbox uses 'test'

def get_json(path, params):
    """Make API request to Microburbs with error handling"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{API_BASE}{path}?{urlencode(params)}"
    
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return {"error": f"Failed to fetch data: {str(e)}"}

def try_price(item):
    """Extract numeric price from various field formats"""
    # Try numeric fields first
    for k in ("price", "price_amount", "price_value"):
        if isinstance(item.get(k), (int, float)) and item[k] > 0:
            return item[k]
    
    # Fall back to price_text like "$1,050,000"; strip non-digits
    txt = item.get("price_text") or item.get("price_display") or ""
    digits = "".join(ch for ch in txt if ch.isdigit())
    return int(digits) if digits else None

def extract_property_data(item):
    """Extract property data from the nested structure"""
    attributes = item.get("attributes", {})
    address = item.get("address", {})
    
    return {
        "price": item.get("price"),
        "bedrooms": attributes.get("bedrooms"),
        "bathrooms": attributes.get("bathrooms"),
        "land_size": attributes.get("land_size"),
        "garage_spaces": attributes.get("garage_spaces"),
        "property_type": item.get("property_type"),
        "listing_date": item.get("listing_date"),
        "address": f"{address.get('street', '')}, {address.get('sal', '')}, {address.get('state', '')}".strip(", "),
        "description": attributes.get("description", ""),
        "coordinates": item.get("coordinates", {})
    }

def create_histogram(values, k=8):
    """Create price distribution histogram"""
    if not values:
        return []
    
    mn, mx = min(values), max(values)
    if mn == mx:
        return [{"label": f"${mn:,.0f}", "count": len(values)}]
    
    step = (mx - mn) / k
    bins = [{"lo": mn + i*step, "hi": mn + (i+1)*step, "count": 0} for i in range(k)]
    
    for v in values:
        idx = min(int((v - mn) / step), k-1)
        bins[idx]["count"] += 1
    
    for b in bins:
        b["label"] = f"${b['lo']:,.0f}–${b['hi']:,.0f}"
        del b["lo"], b["hi"]
    
    return bins

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "Microburbs Mini Explorer is running"}

@app.route('/api/suburb/properties')
def suburb_properties():
    """API endpoint to fetch and process property data from Microburbs"""
    suburb = request.args.get("suburb", "").strip()
    prop_type = request.args.get("property_type", "").strip() or None
    
    if not suburb:
        return jsonify({"error": "suburb is required"}), 400

    # Prepare API parameters
    params = {"suburb": suburb}
    if prop_type:
        params["property_type"] = prop_type

    # Fetch data from Microburbs API
    raw = get_json("/suburb/properties", params)
    
    if "error" in raw:
        return jsonify(raw), 500

    # Process the response - expecting a dict with 'results' key
    items = raw.get("results", []) if isinstance(raw, dict) else raw if isinstance(raw, list) else []

    # Extract and process data using the new structure
    processed_items = [extract_property_data(item) for item in items]
    
    prices = [item["price"] for item in processed_items if item["price"]]
    beds = [item["bedrooms"] for item in processed_items if item["bedrooms"]]
    # Handle land_size that might be strings like "973 m²" or "nan"
    lands = []
    for item in processed_items:
        if item["land_size"] and item["land_size"] != "nan":
            try:
                # Extract number from strings like "973 m²"
                land_str = str(item["land_size"]).replace("m²", "").replace("m2", "").strip()
                if land_str and land_str != "nan":
                    lands.append(float(land_str))
            except (ValueError, TypeError):
                continue
    garage_spaces = [item["garage_spaces"] for item in processed_items if item["garage_spaces"]]

    # Calculate summary statistics
    summary = {
        "suburb": suburb,
        "property_type": prop_type,
        "count": len(processed_items),
        "median_price": median(prices) if prices else None,
        "median_bedrooms": median(beds) if beds else None,
        "median_land_sqm": median(lands) if lands else None,
        "median_garage_spaces": median(garage_spaces) if garage_spaces else None,
        "price_bins": create_histogram(prices) if prices else [],
    }

    # Create property cards with essential fields
    def create_property_card(item):
        return {
            "address": item["address"],
            "price": item["price"],
            "price_text": f"${item['price']:,.0f}" if item["price"] else "Price on request",
            "bedrooms": item["bedrooms"],
            "bathrooms": item["bathrooms"],
            "car_spaces": item["garage_spaces"],
            "land_size": item["land_size"],
            "property_type": item["property_type"],
            "listing_date": item["listing_date"],
            "description": item["description"][:200] + "..." if len(item["description"]) > 200 else item["description"],
            "coordinates": item["coordinates"]
        }

    return jsonify({
        "summary": summary,
        "listings": [create_property_card(item) for item in processed_items]
    })

if __name__ == '__main__':
    print("🚀 Starting Microburbs Mini Explorer...")
    print("📍 Server will be available at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
