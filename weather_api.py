#!/usr/bin/env python
# Weather API Module for Agri Wiz
# Fetches real-time weather data for crop recommendations

import json
import os
import urllib.request
import urllib.parse
import datetime
import time

class WeatherAPI:
    def __init__(self, api_key=None):
        """Initialize the WeatherAPI with an optional API key."""
        self.api_key = api_key or "demo_key"  # Use demo key if none provided
        self.cache_file = "weather_cache.json"
        self.cache_duration = 3600  # Cache weather data for 1 hour (in seconds)
        self.weather_cache = self._load_cache()
    
    def _load_cache(self):
        """Load the weather cache from file if it exists."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading weather cache: {e}")
            return {}
    
    def _save_cache(self):
        """Save the weather cache to file."""
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.weather_cache, f)
        except Exception as e:
            print(f"Error saving weather cache: {e}")
    
    def _is_cache_valid(self, location):
        """Check if cache for a location is still valid."""
        if location in self.weather_cache:
            timestamp = self.weather_cache[location].get("timestamp", 0)
            return (time.time() - timestamp) < self.cache_duration
        return False
    
    def get_weather_data(self, location):
        """
        Get current weather data for a location.
        
        This is a simplified implementation using OpenWeatherMap API.
        In production, replace this with actual API calls using your API key.
        """
        # Check if we have valid cached data
        if self._is_cache_valid(location):
            print(f"Using cached weather data for {location}")
            return self.weather_cache[location]
            
        try:
            # In a real implementation, use the API key and make actual HTTP requests
            if self.api_key == "demo_key":
                # Return mock data for demo purposes
                weather_data = self._get_mock_weather_data(location)
            else:
                # Construct the API URL (OpenWeatherMap example)
                encoded_location = urllib.parse.quote(location)
                url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_location}&appid={self.api_key}&units=metric"
                
                # Make the API request
                with urllib.request.urlopen(url) as response:
                    data = response.read()
                    weather_data = self._parse_api_response(json.loads(data))
                    
            # Cache the result
            weather_data["timestamp"] = time.time()
            self.weather_cache[location] = weather_data
            self._save_cache()
            
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather data for {location}: {e}")
            # Return mock data as fallback
            return self._get_mock_weather_data(location)
    
    def _parse_api_response(self, api_data):
        """Parse the OpenWeatherMap API response into our format."""
        try:
            return {
                "temperature": api_data["main"]["temp"],
                "humidity": api_data["main"]["humidity"],
                "rainfall": api_data.get("rain", {}).get("1h", 0),
                "description": api_data["weather"][0]["description"],
                "timestamp": time.time()
            }
        except KeyError as e:
            print(f"Error parsing API response: {e}")
            return self._get_mock_weather_data("unknown")
    
    def _get_mock_weather_data(self, location):
        """Generate mock weather data for demo purposes."""
        # Extract country/region from location if possible
        location_lower = location.lower()
        
        # Check for known locations and return more accurate mock data
        if "india" in location_lower:
            if "north" in location_lower or "punjab" in location_lower:
                return {
                    "temperature": 32.5,
                    "humidity": 65,
                    "rainfall": 0.5,
                    "description": "Partly cloudy",
                    "timestamp": time.time()
                }
            elif "south" in location_lower or "kerala" in location_lower:
                return {
                    "temperature": 30.0,
                    "humidity": 85,
                    "rainfall": 2.5,
                    "description": "Light rain",
                    "timestamp": time.time()
                }
        elif "usa" in location_lower:
            if "midwest" in location_lower:
                return {
                    "temperature": 22.0,
                    "humidity": 55,
                    "rainfall": 0.0,
                    "description": "Clear sky",
                    "timestamp": time.time()
                }
            elif "california" in location_lower:
                return {
                    "temperature": 25.0,
                    "humidity": 40,
                    "rainfall": 0.0,
                    "description": "Sunny",
                    "timestamp": time.time()
                }
        
        # Generic mock data if location not recognized
        current_month = datetime.datetime.now().month
        
        # Adjust temperature and rainfall based on season in northern hemisphere
        if 3 <= current_month <= 5:  # Spring
            temp = 20.0 + (hash(location) % 10) - 5
            rainfall = 1.0 + (hash(location[::-1]) % 3)
            humidity = 60 + (hash(location) % 20)
            description = "Spring showers"
        elif 6 <= current_month <= 8:  # Summer
            temp = 28.0 + (hash(location) % 15) - 7
            rainfall = 0.5 + (hash(location[::-1]) % 2)
            humidity = 55 + (hash(location) % 25)
            description = "Warm and humid"
        elif 9 <= current_month <= 11:  # Fall
            temp = 15.0 + (hash(location) % 10) - 5
            rainfall = 0.7 + (hash(location[::-1]) % 2.5)
            humidity = 50 + (hash(location) % 20)
            description = "Cool and breezy"
        else:  # Winter
            temp = 5.0 + (hash(location) % 15) - 10
            rainfall = 0.3 + (hash(location[::-1]) % 1.5)
            humidity = 40 + (hash(location) % 30)
            description = "Cold with occasional precipitation"
        
        return {
            "temperature": round(temp, 1),
            "humidity": round(humidity, 0),
            "rainfall": round(rainfall, 1),
            "description": description,
            "timestamp": time.time()
        }
    
    def get_weather_based_recommendations(self, weather_data):
        """
        Get recommendations based on current weather conditions.
        
        Returns a dictionary with recommendations and alerts.
        """
        recommendations = {
            "watering_advice": "",
            "alerts": [],
            "farming_tips": []
        }
        
        # Watering advice
        if weather_data["rainfall"] > 1.5:
            recommendations["watering_advice"] = "Skip watering today due to recent rainfall."
        elif weather_data["humidity"] > 80:
            recommendations["watering_advice"] = "Light watering recommended due to high humidity."
        elif weather_data["temperature"] > 30:
            recommendations["watering_advice"] = "Increase watering frequency due to high temperatures."
        else:
            recommendations["watering_advice"] = "Regular watering schedule recommended."
        
        # Weather alerts
        if weather_data["temperature"] > 35:
            recommendations["alerts"].append("HEAT ALERT: Protect sensitive crops from extreme heat.")
        elif weather_data["temperature"] < 5:
            recommendations["alerts"].append("FROST ALERT: Take measures to protect crops from frost.")
        
        if weather_data["rainfall"] > 3.0:
            recommendations["alerts"].append("HEAVY RAIN ALERT: Check for potential flooding and ensure proper drainage.")
        
        # Farming tips based on weather
        if 20 <= weather_data["temperature"] <= 30:
            recommendations["farming_tips"].append("Optimal temperature for most crop growth and development.")
        
        if weather_data["humidity"] > 70:
            recommendations["farming_tips"].append("High humidity increases disease risk. Monitor crops for fungal infections.")
        elif weather_data["humidity"] < 40:
            recommendations["farming_tips"].append("Low humidity may cause excessive transpiration. Consider shade for sensitive crops.")
        
        if "rain" in weather_data["description"].lower():
            recommendations["farming_tips"].append("Current rainfall presents a good opportunity for transplanting seedlings.")
        
        return recommendations

# Helper function to get humidity level from percentage
def get_humidity_level(humidity_percentage):
    if humidity_percentage <= 40:
        return "low"
    elif humidity_percentage <= 70:
        return "medium"
    else:
        return "high"

# Helper function to get rainfall level from mm
def get_rainfall_level(rainfall_mm):
    if rainfall_mm <= 0.5:
        return "low"
    elif rainfall_mm <= 2:
        return "medium"
    else:
        return "high"

# Simple test if run directly
if __name__ == "__main__":
    api = WeatherAPI()
    data = api.get_weather_data("Punjab, India")
    print(f"Weather for Punjab, India:")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Humidity: {data['humidity']}% ({get_humidity_level(data['humidity'])})")
    print(f"Rainfall: {data['rainfall']}mm ({get_rainfall_level(data['rainfall'])})")
    print(f"Description: {data['description']}")
    
    recommendations = api.get_weather_based_recommendations(data)
    print("\nRecommendations:")
    print(f"- {recommendations['watering_advice']}")
    
    if recommendations["alerts"]:
        print("\nAlerts:")
        for alert in recommendations["alerts"]:
            print(f"- {alert}")
    
    if recommendations["farming_tips"]:
        print("\nFarming Tips:")
        for tip in recommendations["farming_tips"]:
            print(f"- {tip}")