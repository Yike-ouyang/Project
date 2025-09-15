from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
# Remplace par ta clé ORS
ORS_API_KEY = os.getenv("API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_loop', methods=['POST'])
def generate_loop():
    data = request.json
    start_lat = data.get('lat')
    start_lng = data.get('lng')
    distance_km = data.get('distance')

    # OpenRouteService "cycling-regular" profile
    url = "https://api.openrouteservice.org/v2/directions/cycling-regular/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    # ORS a une option "round trip" (circuit)
    payload = {
        "coordinates": [[start_lng, start_lat]],
        "options": {
            "round_trip": {
                "length": distance_km * 1000  # ORS attend en mètres
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), 400

if __name__ == '__main__':
    app.run(debug=True)
