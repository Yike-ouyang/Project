from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import random
load_dotenv()
ORS_API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_loop', methods=['POST'])
def generate_loop():
    data = request.json
    start_lat = data.get('lat')
    start_lng = data.get('lng')
    distance_km = float(data.get('distance', 0))
    print(distance_km)
 
    coordinates = [[start_lng, start_lat]]
    

    url = "https://api.openrouteservice.org/v2/directions/cycling-regular/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
  

    # Paramètre round_trip pour créer une boucle
    payload = {
        "coordinates": coordinates,
        "continue_straight":True,
        "options": {
            "round_trip": {
                "length": distance_km * 1000*1.2,  # longueur en mètres
                "seed": random.randint(1, 100000),  # génère une boucle différente à chaque fois
             
               

            }
        },
        "instructions": True,
        "language":"fr",
        "instructions_format": "text",
        "units": "km",
        "geometry_simplify": True
    }
    

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        route_data = response.json()
        # Extraire distance et durée totales
        summary = route_data['features'][0]['properties']['summary']
        distance = summary.get('distance', 0)
        duration = summary.get('duration', 0)

        # Extraire instructions
        steps = route_data['features'][0]['properties']['segments'][0]['steps']
        instructions = []
        for step in steps:
            if step['distance'] < 1:
                dist = step['distance'] *1000
                if dist > 10:
                    instructions.append(f"{step['instruction']} ({dist} m )")
            else:
                instructions.append(f"{step['instruction']} ({step['distance']:.2f} km )")

        return jsonify({
            "geojson": route_data,
            "distance": distance,
            "duration": duration,
            "instructions": instructions
        })
    else:
        return jsonify({"error": response.text}), 400

if __name__ == '__main__':
    app.run(debug=True)
