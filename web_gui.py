#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, url_for
from agri_wiz import AgriWiz
from weather_api import WeatherAPI, get_humidity_level, get_rainfall_level
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')
agri_wiz = AgriWiz()
weather_api = WeatherAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/locations')
def get_locations():
    locations = agri_wiz.location_manager.get_all_locations()
    return jsonify(locations)

@app.route('/api/weather/<location>')
def get_weather(location):
    try:
        weather_data = weather_api.get_weather_data(location)
        season = agri_wiz.location_manager.get_current_season_for_location(location)
        if not season:
            season = agri_wiz.get_current_season()
        
        return jsonify({
            'temperature': weather_data['temperature'],
            'humidity': weather_data['humidity'],
            'rainfall': weather_data['rainfall'],
            'season': season,
            'humidity_level': get_humidity_level(weather_data['humidity']),
            'rainfall_level': get_rainfall_level(weather_data['rainfall'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    try:
        if 'location' in data and data['location']:
            recommendations, details = agri_wiz.get_recommendations_by_location(
                data['location'],
                data.get('humidity'),
                data.get('soil_fertility')
            )
            return jsonify({
                'recommendations': recommendations,
                'details': details
            })
        else:
            recommendations = agri_wiz.get_recommendations(
                data['soil_type'],
                data['climate'],
                data['season'],
                data.get('rainfall'),
                data.get('humidity'),
                data.get('soil_fertility')
            )
            return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/crops')
def get_crops():
    return jsonify(agri_wiz.crop_data)

@app.route('/api/crops', methods=['POST'])
def add_crop():
    crop_data = request.json
    try:
        agri_wiz.add_crop(crop_data)
        return jsonify({'message': 'Crop added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)