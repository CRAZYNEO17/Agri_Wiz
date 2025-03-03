#!/usr/bin/env python
# Agri Wiz - Crop Recommendation System
# A program to recommend crops to farmers based on location and environmental parameters

import os
import json
import csv
from datetime import datetime
from location_data import LocationManager

class AgriWiz:
    def __init__(self):
        self.crop_data = []
        self.location_manager = LocationManager()
        self.load_crop_data()
        
    def load_crop_data(self):
        """Load crop data from the CSV file."""
        try:
            if os.path.exists("crop_data.csv"):
                with open("crop_data.csv", "r") as file:
                    reader = csv.DictReader(file)
                    self.crop_data = list(reader)
                print(f"Loaded {len(self.crop_data)} crops from database.")
            else:
                print("Crop database not found. Creating sample data.")
                self.create_sample_data()
        except Exception as e:
            print(f"Error loading crop data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample crop data if no data file exists."""
        self.crop_data = [
            {"crop_name": "Rice", "soil_types": "clay,loamy,alluvial", "climates": "tropical,subtropical", "seasons": "summer,rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "medium,high"},
            {"crop_name": "Wheat", "soil_types": "loamy,sandy loam,alluvial", "climates": "temperate,subtropical", "seasons": "winter,spring", "water_needs": "medium", "humidity_preference": "low,medium", "soil_fertility": "medium,high"},
            {"crop_name": "Corn", "soil_types": "loamy,sandy,alluvial", "climates": "temperate,subtropical", "seasons": "summer", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium,high"},
            {"crop_name": "Cotton", "soil_types": "loamy,black soil", "climates": "subtropical,tropical", "seasons": "summer,rainy", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "high"},
            {"crop_name": "Sugarcane", "soil_types": "loamy,clay,black soil", "climates": "tropical,subtropical", "seasons": "spring", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "high"},
            {"crop_name": "Potato", "soil_types": "loamy,sandy loam", "climates": "temperate", "seasons": "winter,spring", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium,high"},
            {"crop_name": "Tomato", "soil_types": "loamy,sandy loam", "climates": "temperate,subtropical", "seasons": "summer,spring", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium,high"},
            {"crop_name": "Soybean", "soil_types": "loamy,clay loam", "climates": "temperate,subtropical", "seasons": "summer", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium"},
            {"crop_name": "Barley", "soil_types": "loamy,clay loam", "climates": "temperate", "seasons": "winter,spring", "water_needs": "low", "humidity_preference": "low", "soil_fertility": "low,medium"},
            {"crop_name": "Oats", "soil_types": "loamy,sandy loam", "climates": "temperate", "seasons": "spring,fall", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium"},
            {"crop_name": "Chickpea", "soil_types": "sandy loam,loamy", "climates": "subtropical", "seasons": "winter", "water_needs": "low", "humidity_preference": "low", "soil_fertility": "low,medium"},
            {"crop_name": "Mustard", "soil_types": "loamy,clay", "climates": "subtropical", "seasons": "winter", "water_needs": "low", "humidity_preference": "low", "soil_fertility": "medium"},
            {"crop_name": "Groundnut", "soil_types": "sandy,loamy,red", "climates": "tropical,subtropical", "seasons": "rainy", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium"},
            {"crop_name": "Sunflower", "soil_types": "loamy,sandy loam", "climates": "temperate,subtropical", "seasons": "spring,summer", "water_needs": "medium", "humidity_preference": "low,medium", "soil_fertility": "medium"},
            {"crop_name": "Mango", "soil_types": "loamy,alluvial,laterite", "climates": "tropical", "seasons": "summer", "water_needs": "medium", "humidity_preference": "medium,high", "soil_fertility": "medium"},
            {"crop_name": "Banana", "soil_types": "loamy,alluvial", "climates": "tropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "high"},
            # Adding new crops with humidity and soil fertility parameters
            {"crop_name": "Coffee", "soil_types": "loamy,volcanic", "climates": "tropical,subtropical", "seasons": "rainy", "water_needs": "medium", "humidity_preference": "high", "soil_fertility": "medium,high"},
            {"crop_name": "Tea", "soil_types": "loamy,acidic", "climates": "tropical,subtropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "medium"},
            {"crop_name": "Cashew", "soil_types": "sandy,red,laterite", "climates": "tropical", "seasons": "summer", "water_needs": "low", "humidity_preference": "medium", "soil_fertility": "low,medium"},
            {"crop_name": "Coconut", "soil_types": "sandy,loamy,laterite", "climates": "tropical", "seasons": "rainy", "water_needs": "medium", "humidity_preference": "high", "soil_fertility": "medium"},
            {"crop_name": "Orange", "soil_types": "loamy,sandy loam", "climates": "subtropical", "seasons": "winter", "water_needs": "medium", "humidity_preference": "medium", "soil_fertility": "medium,high"},
            {"crop_name": "Apple", "soil_types": "loamy,sandy loam", "climates": "temperate", "seasons": "spring", "water_needs": "medium", "humidity_preference": "low,medium", "soil_fertility": "medium,high"},
            {"crop_name": "Grape", "soil_types": "sandy,loamy", "climates": "mediterranean,temperate", "seasons": "spring,summer", "water_needs": "low,medium", "humidity_preference": "low", "soil_fertility": "medium"},
            {"crop_name": "Onion", "soil_types": "loamy,sandy loam", "climates": "temperate,subtropical", "seasons": "winter", "water_needs": "medium", "humidity_preference": "low,medium", "soil_fertility": "medium"},
            {"crop_name": "Garlic", "soil_types": "loamy,sandy loam", "climates": "temperate", "seasons": "winter", "water_needs": "medium", "humidity_preference": "low", "soil_fertility": "medium"},
            {"crop_name": "Turmeric", "soil_types": "loamy,sandy loam", "climates": "tropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "high"},
            {"crop_name": "Ginger", "soil_types": "loamy,sandy loam", "climates": "tropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "high"},
            {"crop_name": "Chili Pepper", "soil_types": "loamy,sandy loam", "climates": "tropical,subtropical", "seasons": "summer", "water_needs": "medium", "humidity_preference": "medium,high", "soil_fertility": "medium,high"},
            {"crop_name": "Cardamom", "soil_types": "loamy,forest", "climates": "tropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "high"},
            {"crop_name": "Black Pepper", "soil_types": "loamy,forest", "climates": "tropical", "seasons": "rainy", "water_needs": "high", "humidity_preference": "high", "soil_fertility": "medium,high"}
        ]
        self.save_crop_data()
    
    def save_crop_data(self):
        """Save crop data to CSV file."""
        try:
            with open("crop_data.csv", "w", newline="") as file:
                fieldnames = ["crop_name", "soil_types", "climates", "seasons", "water_needs", "humidity_preference", "soil_fertility"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.crop_data)
            print("Crop data saved successfully.")
        except Exception as e:
            print(f"Error saving crop data: {e}")
    
    def add_crop(self, crop_data):
        """Add a new crop to the database."""
        self.crop_data.append(crop_data)
        self.save_crop_data()
        print(f"Added {crop_data['crop_name']} to the database.")
    
    def get_recommendations(self, soil_type, climate, season, rainfall=None, humidity=None, soil_fertility=None):
        """Get crop recommendations based on input parameters."""
        recommendations = []
        
        for crop in self.crop_data:
            # Core parameters (required matches)
            soil_match = any(s.strip().lower() == soil_type.lower() 
                            for s in crop["soil_types"].split(","))
            climate_match = any(c.strip().lower() == climate.lower() 
                              for c in crop["climates"].split(","))
            season_match = any(s.strip().lower() == season.lower() 
                             for s in crop["seasons"].split(","))
            
            # Optional parameters (if provided)
            humidity_match = True
            if humidity and "humidity_preference" in crop:
                humidity_match = any(h.strip().lower() == humidity.lower() 
                                  for h in crop["humidity_preference"].split(","))
            
            soil_fertility_match = True
            if soil_fertility and "soil_fertility" in crop:
                soil_fertility_match = any(f.strip().lower() == soil_fertility.lower() 
                                        for f in crop["soil_fertility"].split(","))
            
            if soil_match and climate_match and season_match and humidity_match and soil_fertility_match:
                recommendations.append(crop)
        
        # Sort by water needs based on rainfall if provided
        if rainfall and recommendations:
            if rainfall.lower() == "high":
                recommendations.sort(key=lambda x: 0 if x["water_needs"] == "high" else (1 if x["water_needs"] == "medium" else 2))
            elif rainfall.lower() == "low":
                recommendations.sort(key=lambda x: 0 if x["water_needs"] == "low" else (1 if x["water_needs"] == "medium" else 2))
        
        return recommendations

    def get_current_season(self):
        """Determine current season based on month."""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:  # months 9, 10, 11
            return "fall"
            
    def get_recommendations_by_location(self, location_name, humidity=None, soil_fertility=None):
        """Get crop recommendations based on location and additional parameters."""
        location_info = self.location_manager.get_location_info(location_name)
        
        if not location_info:
            return None, "Location not found in database"
        
        # Get current season for location
        current_month = datetime.now().strftime("%B").lower()
        current_season = None
        
        for season, months in location_info["seasons"].items():
            if current_month in months:
                current_season = season
                break
        
        if not current_season:
            current_season = self.get_current_season()
        
        # Get recommendations based on location data
        soil_type = location_info["common_soil_types"][0] if location_info["common_soil_types"] else "loamy"
        climate = location_info["climate"]
        rainfall = location_info["rainfall"]
        
        # Get humidity from location if available and not provided
        location_humidity = location_info.get("humidity", None)
        if humidity is None and location_humidity:
            humidity = location_humidity
        
        recommendations = self.get_recommendations(soil_type, climate, current_season, rainfall, humidity, soil_fertility)
        
        return recommendations, {
            "soil_type": soil_type,
            "climate": climate,
            "season": current_season,
            "rainfall": rainfall,
            "humidity": humidity,
            "soil_fertility": soil_fertility
        }

def main():
    """Main entry point for Agri Wiz"""
    import sys
    
    # Check if GUI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        # Import and start GUI
        from gui import AgriWizGUI
        app = AgriWizGUI()
        app.run()
        return

    # CLI mode
    agri_wiz = AgriWiz()
    
    print("\n" + "="*50)
    print("🌱 Welcome to Agri Wiz - Crop Recommendation System 🌱")
    print("="*50)
    print("\nTip: Run with --gui argument to use the graphical interface")
    
    while True:
        print("\nPlease select an option:")
        print("1. Get crop recommendations")
        print("2. Get recommendations by location")
        print("3. Add new crop to database")
        print("4. View all crops in database")
        print("5. Manage locations")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            print("\n--- Crop Recommendation ---")
            location = input("Enter your location (optional): ")
            
            # If location provided, try to get soil and climate defaults
            soil_defaults = []
            climate_default = ""
            if location:
                soil_defaults = agri_wiz.location_manager.get_soil_recommendations(location)
                climate_default = agri_wiz.location_manager.get_climate(location)
                
                if soil_defaults or climate_default:
                    print(f"\nFound data for location: {location}")
                    if soil_defaults:
                        print(f"Common soil types: {', '.join(soil_defaults)}")
                    if climate_default:
                        print(f"Climate: {climate_default}")
            
            soil_type = input("Enter soil type (clay/loamy/sandy/black soil): ")
            climate = input("Enter climate (tropical/subtropical/temperate): ") if not climate_default else input(f"Enter climate (tropical/subtropical/temperate) [default: {climate_default}]: ") or climate_default
            
            # Get season or use current season
            use_current = input("Use current season? (y/n): ").lower()
            if use_current == "y":
                if location:
                    season = agri_wiz.location_manager.get_current_season_for_location(location) or agri_wiz.get_current_season()
                else:
                    season = agri_wiz.get_current_season()
                print(f"Current season detected as: {season}")
            else:
                season = input("Enter season (summer/winter/rainy/spring/fall): ")
            
            rainfall = input("Enter rainfall level (low/medium/high) [optional]: ")
            humidity = input("Enter humidity level (low/medium/high) [optional]: ")
            soil_fertility = input("Enter soil fertility (low/medium/high) [optional]: ")
            
            recommendations = agri_wiz.get_recommendations(soil_type, climate, season, rainfall, humidity, soil_fertility)
            
            print("\n--- Recommended Crops ---")
            if recommendations:
                print(f"Found {len(recommendations)} suitable crops for your conditions:")
                for i, crop in enumerate(recommendations, 1):
                    print(f"{i}. {crop['crop_name']} (Water needs: {crop['water_needs']}, "
                          f"Humidity: {crop.get('humidity_preference', 'N/A')}, "
                          f"Soil fertility: {crop.get('soil_fertility', 'N/A')})")
            else:
                print("No crops match your exact criteria. Consider these alternatives:")
                # Provide some close matches with fewer criteria matching
                alternatives = []
                for crop in agri_wiz.crop_data:
                    matches = 0
                    total_parameters = 3  # Core parameters
                    
                    # Check core parameters
                    if any(s.strip().lower() == soil_type.lower() for s in crop["soil_types"].split(",")):
                        matches += 1
                    if any(c.strip().lower() == climate.lower() for c in crop["climates"].split(",")):
                        matches += 1
                    if any(s.strip().lower() == season.lower() for s in crop["seasons"].split(",")):
                        matches += 1
                    
                    # Check optional parameters if provided
                    if humidity and "humidity_preference" in crop:
                        total_parameters += 1
                        if any(h.strip().lower() == humidity.lower() for h in crop["humidity_preference"].split(",")):
                            matches += 1
                    
                    if soil_fertility and "soil_fertility" in crop:
                        total_parameters += 1
                        if any(f.strip().lower() == soil_fertility.lower() for f in crop["soil_fertility"].split(",")):
                            matches += 1
                    
                    # Calculate match percentage
                    match_percentage = (matches / total_parameters) * 100
                    
                    if match_percentage >= 60:  # At least 60% match
                        alternatives.append((crop, matches, match_percentage))
                
                # Sort alternatives by match percentage
                alternatives.sort(key=lambda x: x[2], reverse=True)
                
                for i, (crop, matches, percentage) in enumerate(alternatives[:5], 1):
                    print(f"{i}. {crop['crop_name']} - {percentage:.0f}% match")
                    print(f"   Water needs: {crop['water_needs']}, "
                          f"Humidity: {crop.get('humidity_preference', 'N/A')}, "
                          f"Soil fertility: {crop.get('soil_fertility', 'N/A')}")
        
        elif choice == "2":
            print("\n--- Location-Based Recommendations ---")
            
            # Show available locations
            print("\nAvailable locations in database:")
            locations = agri_wiz.location_manager.get_all_locations()
            for i, loc in enumerate(locations, 1):
                print(f"{i}. {loc.replace('_', ' ').title()}")
                
            location = input("\nEnter your location: ")
            humidity = input("Enter humidity level (low/medium/high) [optional]: ")
            soil_fertility = input("Enter soil fertility (low/medium/high) [optional]: ")
            
            recommendations, details = agri_wiz.get_recommendations_by_location(location, humidity, soil_fertility)
            
            if recommendations is None:
                print(f"\n{details}")
                continue
                
            print(f"\nUsing location data:")
            print(f"  - Soil Type: {details['soil_type']}")
            print(f"  - Climate: {details['climate']}")
            print(f"  - Season: {details['season']}")
            print(f"  - Rainfall: {details['rainfall']}")
            if details['humidity']:
                print(f"  - Humidity: {details['humidity']}")
            if details['soil_fertility']:
                print(f"  - Soil Fertility: {details['soil_fertility']}")
            
            print("\n--- Recommended Crops ---")
            if recommendations:
                print(f"Found {len(recommendations)} suitable crops for your location:")
                for i, crop in enumerate(recommendations, 1):
                    print(f"{i}. {crop['crop_name']} (Water needs: {crop['water_needs']}, "
                          f"Humidity: {crop.get('humidity_preference', 'N/A')}, "
                          f"Soil fertility: {crop.get('soil_fertility', 'N/A')})")
            else:
                print("No crops match your location criteria exactly.")
                print("Try adjusting optional parameters or use option 1 for manual input.")
        
        elif choice == "3":
            print("\n--- Add New Crop ---")
            crop_name = input("Enter crop name: ")
            soil_types = input("Enter suitable soil types (comma-separated): ")
            climates = input("Enter suitable climates (comma-separated): ")
            seasons = input("Enter suitable seasons (comma-separated): ")
            water_needs = input("Enter water needs (low/medium/high): ")
            humidity = input("Enter humidity preference (low/medium/high, comma-separated): ")
            soil_fertility = input("Enter soil fertility needs (low/medium/high, comma-separated): ")
            
            new_crop = {
                "crop_name": crop_name,
                "soil_types": soil_types,
                "climates": climates,
                "seasons": seasons,
                "water_needs": water_needs,
                "humidity_preference": humidity,
                "soil_fertility": soil_fertility
            }
            
            agri_wiz.add_crop(new_crop)
        
        elif choice == "4":
            print("\n--- All Crops in Database ---")
            for i, crop in enumerate(agri_wiz.crop_data, 1):
                print(f"{i}. {crop['crop_name']}")
                print(f"   Soil Types: {crop['soil_types']}")
                print(f"   Climates: {crop['climates']}")
                print(f"   Seasons: {crop['seasons']}")
                print(f"   Water Needs: {crop['water_needs']}")
                if "humidity_preference" in crop:
                    print(f"   Humidity Preference: {crop['humidity_preference']}")
                if "soil_fertility" in crop:
                    print(f"   Soil Fertility: {crop['soil_fertility']}")
                print()
        
        elif choice == "5":
            print("\n--- Manage Locations ---")
            print("1. View all locations")
            print("2. Add new location")
            
            loc_choice = input("Enter your choice (1-2): ")
            
            if loc_choice == "1":
                print("\n--- All Locations in Database ---")
                locations = agri_wiz.location_manager.get_all_locations()
                
                for i, loc_name in enumerate(locations, 1):
                    loc_info = agri_wiz.location_manager.get_location_info(loc_name)
                    print(f"{i}. {loc_name.replace('_', ' ').title()}")
                    print(f"   Climate: {loc_info['climate']}")
                    print(f"   Soil Types: {', '.join(loc_info['common_soil_types'])}")
                    print(f"   Rainfall: {loc_info['rainfall']}")
                    if "humidity" in loc_info:
                        print(f"   Humidity: {loc_info['humidity']}")
                    print(f"   Seasons: {', '.join(loc_info['seasons'].keys())}")
                    print()
            
            elif loc_choice == "2":
                print("\n--- Add New Location ---")
                location_name = input("Enter location name: ")
                soil_types = input("Enter common soil types (comma-separated): ").split(",")
                soil_types = [s.strip() for s in soil_types]
                climate = input("Enter climate: ")
                rainfall = input("Enter rainfall level (low/medium/high): ")
                humidity = input("Enter humidity level (low/medium/high): ")
                
                # Season data
                print("\nNow enter the months for each season (comma-separated):")
                winter_months = input("Winter months: ").lower().split(",")
                winter_months = [m.strip() for m in winter_months]
                summer_months = input("Summer months: ").lower().split(",")
                summer_months = [m.strip() for m in summer_months]
                rainy_months = input("Rainy/Monsoon months: ").lower().split(",")
                rainy_months = [m.strip() for m in rainy_months]
                spring_months = input("Spring months: ").lower().split(",")
                spring_months = [m.strip() for m in spring_months]
                fall_months = input("Fall/Autumn months: ").lower().split(",")
                fall_months = [m.strip() for m in fall_months]
                
                seasons = {}
                if winter_months[0]: seasons["winter"] = winter_months
                if summer_months[0]: seasons["summer"] = summer_months
                if rainy_months[0]: seasons["rainy"] = rainy_months
                if spring_months[0]: seasons["spring"] = spring_months
                if fall_months[0]: seasons["fall"] = fall_months
                
                location_info = {
                    "common_soil_types": soil_types,
                    "climate": climate,
                    "rainfall": rainfall,
                    "humidity": humidity if humidity else None,
                    "seasons": seasons
                }
                
                agri_wiz.location_manager.add_location(location_name, location_info)
        
        elif choice == "6":
            print("\nThank you for using Agri Wiz! Happy farming! 🌾")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()