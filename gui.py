#!/usr/bin/env python
# GUI Module for Agri Wiz
# Provides a graphical user interface for the crop recommendation system

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from agri_wiz import AgriWiz
from weather_api import WeatherAPI, get_humidity_level, get_rainfall_level
import datetime
import requests
import json

class AgriWizGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agri Wiz - Crop Recommendation System")
        self.root.geometry("800x600")
        
        # Initialize backend systems
        self.agri_wiz = AgriWiz()
        self.weather_api = WeatherAPI()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.create_recommendation_tab()
        self.create_location_tab()
        self.create_crops_tab()
        
    def create_recommendation_tab(self):
        """Create the main recommendation tab"""
        rec_frame = ttk.Frame(self.notebook)
        self.notebook.add(rec_frame, text="Get Recommendations")
        
        # Input frame
        input_frame = ttk.LabelFrame(rec_frame, text="Input Parameters", padding=10)
        input_frame.pack(fill='x', padx=5, pady=5)
        
        # Location input
        ttk.Label(input_frame, text="Location:").grid(row=0, column=0, sticky='w', pady=2)
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(input_frame, textvariable=self.location_var)
        self.location_entry.grid(row=0, column=1, sticky='ew', pady=2)
        ttk.Button(input_frame, text="Use Location", command=self.use_location).grid(row=0, column=2, padx=5)
        
        # Soil type input
        ttk.Label(input_frame, text="Soil Type:").grid(row=1, column=0, sticky='w', pady=2)
        self.soil_var = tk.StringVar()
        soil_types = ['clay', 'loamy', 'sandy', 'black soil']
        self.soil_combo = ttk.Combobox(input_frame, textvariable=self.soil_var, values=soil_types)
        self.soil_combo.grid(row=1, column=1, sticky='ew', pady=2)
        
        # Climate input
        ttk.Label(input_frame, text="Climate:").grid(row=2, column=0, sticky='w', pady=2)
        self.climate_var = tk.StringVar()
        climates = ['tropical', 'subtropical', 'temperate']
        self.climate_combo = ttk.Combobox(input_frame, textvariable=self.climate_var, values=climates)
        self.climate_combo.grid(row=2, column=1, sticky='ew', pady=2)
        
        # Season input
        ttk.Label(input_frame, text="Season:").grid(row=3, column=0, sticky='w', pady=2)
        self.season_var = tk.StringVar()
        seasons = ['summer', 'winter', 'rainy', 'spring', 'fall']
        self.season_combo = ttk.Combobox(input_frame, textvariable=self.season_var, values=seasons)
        self.season_combo.grid(row=3, column=1, sticky='ew', pady=2)
        ttk.Button(input_frame, text="Use Current Season", command=self.use_current_season).grid(row=3, column=2, padx=5)
        
        # Optional parameters
        ttk.Label(input_frame, text="Rainfall:").grid(row=4, column=0, sticky='w', pady=2)
        self.rainfall_var = tk.StringVar()
        rainfalls = ['', 'low', 'medium', 'high']
        ttk.Combobox(input_frame, textvariable=self.rainfall_var, values=rainfalls).grid(row=4, column=1, sticky='ew', pady=2)
        
        ttk.Label(input_frame, text="Humidity:").grid(row=5, column=0, sticky='w', pady=2)
        self.humidity_var = tk.StringVar()
        humidities = ['', 'low', 'medium', 'high']
        ttk.Combobox(input_frame, textvariable=self.humidity_var, values=humidities).grid(row=5, column=1, sticky='ew', pady=2)
        
        ttk.Label(input_frame, text="Soil Fertility:").grid(row=6, column=0, sticky='w', pady=2)
        self.fertility_var = tk.StringVar()
        fertilities = ['', 'low', 'medium', 'high']
        ttk.Combobox(input_frame, textvariable=self.fertility_var, values=fertilities).grid(row=6, column=1, sticky='ew', pady=2)
        
        # Submit button
        ttk.Button(input_frame, text="Get Recommendations", command=self.get_recommendations).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(rec_frame, text="Recommendations", padding=10)
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create scrolled text widget for results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10)
        self.results_text.pack(fill='both', expand=True)
        
    def create_location_tab(self):
        """Create the location management tab"""
        loc_frame = ttk.Frame(self.notebook)
        self.notebook.add(loc_frame, text="Manage Locations")
        
        # Locations list
        list_frame = ttk.LabelFrame(loc_frame, text="Available Locations", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for locations
        columns = ('Location', 'Climate', 'Soil Types', 'Rainfall')
        self.location_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.location_tree.heading(col, text=col)
            self.location_tree.column(col, width=100)
        
        self.location_tree.pack(fill='both', expand=True)
        
        # Add location frame
        add_frame = ttk.LabelFrame(loc_frame, text="Add New Location", padding=10)
        add_frame.pack(fill='x', padx=5, pady=5)
        
        # Location name
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.new_location_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_location_var).grid(row=0, column=1, sticky='ew', pady=2)
        
        # Add button
        ttk.Button(add_frame, text="Add Location", command=self.add_location).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Load locations
        self.load_locations()
        
    def create_crops_tab(self):
        """Create the crops management tab"""
        crops_frame = ttk.Frame(self.notebook)
        self.notebook.add(crops_frame, text="Manage Crops")
        
        # Crops list
        list_frame = ttk.LabelFrame(crops_frame, text="Available Crops", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for crops
        columns = ('Crop', 'Soil Types', 'Climate', 'Seasons', 'Water Needs')
        self.crops_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.crops_tree.heading(col, text=col)
            self.crops_tree.column(col, width=100)
        
        self.crops_tree.pack(fill='both', expand=True)
        
        # Add crop frame
        add_frame = ttk.LabelFrame(crops_frame, text="Add New Crop", padding=10)
        add_frame.pack(fill='x', padx=5, pady=5)
        
        # Crop name
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.new_crop_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_crop_var).grid(row=0, column=1, sticky='ew', pady=2)
        
        # Add button
        ttk.Button(add_frame, text="Add Crop", command=self.add_crop).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Load crops
        self.load_crops()
        
    def use_location(self):
        """Use device's current location to populate fields"""
        try:
            # Get current location using IP geolocation
            response = requests.get('https://ipapi.co/json/')
            if response.status_code == 200:
                location_data = response.json()
                location = f"{location_data['city']}"
                self.location_var.set(location)
                
                # Try to get location info from our database
                location_info = self.agri_wiz.location_manager.get_location_info(location)
                if not location_info:
                    # If location not in database, create a new entry with weather API data
                    weather_data = self.weather_api.get_weather_data(location)
                    
                    # Determine climate based on latitude and temperature
                    lat = location_data['latitude']
                    if abs(lat) <= 23.5:
                        climate = 'tropical'
                    elif abs(lat) <= 35:
                        climate = 'subtropical'
                    else:
                        climate = 'temperate'
                    
                    # Create new location info
                    new_location = {
                        "common_soil_types": ["loamy"],  # Default soil type
                        "climate": climate,
                        "rainfall": get_rainfall_level(weather_data.get("rainfall", 0)),
                        "humidity": get_humidity_level(weather_data.get("humidity", 0)),
                        "soil_fertility": "medium",  # Default fertility
                        "seasons": {
                            "winter": ["december", "january", "february"],
                            "spring": ["march", "april", "may"],
                            "summer": ["june", "july", "august"],
                            "fall": ["september", "october", "november"]
                        }
                    }
                    
                    # Add new location to database
                    self.agri_wiz.location_manager.add_location(location, new_location)
                    location_info = new_location
                
                # Set fields based on location info
                if location_info.get('common_soil_types'):
                    self.soil_var.set(location_info['common_soil_types'][0])
                    
                if location_info.get('climate'):
                    self.climate_var.set(location_info['climate'])
                    
                current_season = self.agri_wiz.location_manager.get_current_season_for_location(location)
                if current_season:
                    self.season_var.set(current_season)
                    
                if location_info.get('rainfall'):
                    self.rainfall_var.set(location_info['rainfall'])
                if location_info.get('humidity'):
                    self.humidity_var.set(location_info['humidity'])
                if location_info.get('soil_fertility'):
                    self.fertility_var.set(location_info['soil_fertility'])
                    
                messagebox.showinfo("Location Detected", f"Successfully detected and loaded data for {location}")
            else:
                messagebox.showerror("Location Error", "Failed to detect current location")
                
        except Exception as e:
            messagebox.showerror("Location Error", f"Error detecting location: {str(e)}\nPlease enter location manually.")
            
    def use_current_season(self):
        """Set the current season based on weather data and location"""
        location = self.location_var.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location to get accurate season information.")
            return
            
        # Get weather data for the location
        try:
            weather_data = self.weather_api.get_weather_data(location)
            
            # First try to get season from location data
            season = self.agri_wiz.location_manager.get_current_season_for_location(location)
            
            if not season:
                # If no location-specific season, determine from weather
                temp = weather_data["temperature"]
                if temp > 25:  # Hot
                    if weather_data["rainfall"] > 1.5:  # High rainfall
                        season = "rainy"
                    else:
                        season = "summer"
                elif temp < 15:  # Cold
                    season = "winter"
                else:  # Moderate temperatures
                    current_month = datetime.datetime.now().month
                    if 3 <= current_month <= 5:
                        season = "spring"
                    elif 9 <= current_month <= 11:
                        season = "fall"
                    else:
                        season = "winter"
            
            self.season_var.set(season)
            
            # Update other weather-related fields
            self.humidity_var.set(get_humidity_level(weather_data["humidity"]))
            self.rainfall_var.set(get_rainfall_level(weather_data["rainfall"]))
            
            # Show weather information
            messagebox.showinfo("Weather Information", 
                f"Current weather in {location}:\n"
                f"Temperature: {weather_data['temperature']}°C\n"
                f"Humidity: {weather_data['humidity']}%\n"
                f"Rainfall: {weather_data['rainfall']}mm\n"
                f"Season detected: {season.title()}")
                
        except Exception as e:
            messagebox.showerror("Weather Error", 
                f"Could not fetch weather data: {str(e)}\n"
                "Using default season based on date.")
            # Fallback to basic season detection
            season = self.agri_wiz.get_current_season()
            self.season_var.set(season)
        
    def get_recommendations(self):
        """Get and display crop recommendations"""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Get input values
        soil_type = self.soil_var.get()
        climate = self.climate_var.get()
        season = self.season_var.get()
        rainfall = self.rainfall_var.get()
        humidity = self.humidity_var.get()
        soil_fertility = self.fertility_var.get()
        
        # Validate required inputs
        if not all([soil_type, climate, season]):
            messagebox.showerror("Input Error", "Please provide soil type, climate, and season.")
            return
        
        # Get recommendations
        recommendations = self.agri_wiz.get_recommendations(
            soil_type, climate, season, rainfall, humidity, soil_fertility
        )
        
        if recommendations:
            self.results_text.insert(tk.END, f"Found {len(recommendations)} suitable crops:\n\n")
            for i, crop in enumerate(recommendations, 1):
                self.results_text.insert(tk.END, 
                    f"{i}. {crop['crop_name']}\n"
                    f"   Water needs: {crop['water_needs']}\n"
                    f"   Humidity: {crop.get('humidity_preference', 'N/A')}\n"
                    f"   Soil fertility: {crop.get('soil_fertility', 'N/A')}\n\n"
                )
        else:
            self.results_text.insert(tk.END, "No crops match your criteria exactly.\n")
            # Get alternative recommendations with lower match requirements
            alternatives = []
            for crop in self.agri_wiz.crop_data:
                matches = 0
                total_parameters = 3
                
                if any(s.strip().lower() == soil_type.lower() for s in crop["soil_types"].split(",")):
                    matches += 1
                if any(c.strip().lower() == climate.lower() for c in crop["climates"].split(",")):
                    matches += 1
                if any(s.strip().lower() == season.lower() for s in crop["seasons"].split(",")):
                    matches += 1
                
                match_percentage = (matches / total_parameters) * 100
                if match_percentage >= 60:
                    alternatives.append((crop, match_percentage))
            
            if alternatives:
                self.results_text.insert(tk.END, "\nConsider these alternatives:\n\n")
                for crop, percentage in sorted(alternatives, key=lambda x: x[1], reverse=True)[:5]:
                    self.results_text.insert(tk.END,
                        f"{crop['crop_name']} - {percentage:.0f}% match\n"
                        f"   Water needs: {crop['water_needs']}\n"
                        f"   Humidity: {crop.get('humidity_preference', 'N/A')}\n"
                        f"   Soil fertility: {crop.get('soil_fertility', 'N/A')}\n\n"
                    )
                    
    def load_locations(self):
        """Load locations into the treeview"""
        # Clear existing items
        for item in self.location_tree.get_children():
            self.location_tree.delete(item)
            
        # Add locations
        locations = self.agri_wiz.location_manager.get_all_locations()
        for location in locations:
            info = self.agri_wiz.location_manager.get_location_info(location)
            self.location_tree.insert('', 'end', values=(
                location.replace('_', ' ').title(),
                info['climate'],
                ', '.join(info['common_soil_types']),
                info['rainfall']
            ))
            
    def load_crops(self):
        """Load crops into the treeview"""
        # Clear existing items
        for item in self.crops_tree.get_children():
            self.crops_tree.delete(item)
            
        # Add crops
        for crop in self.agri_wiz.crop_data:
            self.crops_tree.insert('', 'end', values=(
                crop['crop_name'],
                crop['soil_types'],
                crop['climates'],
                crop['seasons'],
                crop['water_needs']
            ))
            
    def add_location(self):
        """Add a new location (simplified version)"""
        location_name = self.new_location_var.get()
        if location_name:
            # Show dialog to get location details
            dialog = LocationDialog(self.root, self.agri_wiz.location_manager)
            if dialog.result:
                self.load_locations()
                self.new_location_var.set('')
        else:
            messagebox.showwarning("Input Error", "Please enter a location name.")
            
    def add_crop(self):
        """Add a new crop (simplified version)"""
        crop_name = self.new_crop_var.get()
        if crop_name:
            # Show dialog to get crop details
            dialog = CropDialog(self.root, self.agri_wiz)
            if dialog.result:
                self.load_crops()
                self.new_crop_var.set('')
        else:
            messagebox.showwarning("Input Error", "Please enter a crop name.")
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

class LocationDialog:
    """Dialog for adding a new location"""
    def __init__(self, parent, location_manager):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Location")
        self.dialog.geometry("400x600")
        self.dialog.resizable(False, False)
        self.location_manager = location_manager
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create and show the dialog contents
        self.create_widgets()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
        
    def create_widgets(self):
        """Create the dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Location name
        ttk.Label(main_frame, text="Location Name:").pack(fill='x', pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).pack(fill='x', pady=2)
        
        # Climate
        ttk.Label(main_frame, text="Climate:").pack(fill='x', pady=2)
        self.climate_var = tk.StringVar()
        climates = ['tropical', 'subtropical', 'temperate', 'mediterranean']
        ttk.Combobox(main_frame, textvariable=self.climate_var, values=climates).pack(fill='x', pady=2)
        
        # Soil types
        ttk.Label(main_frame, text="Soil Types (comma-separated):").pack(fill='x', pady=2)
        self.soil_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.soil_var).pack(fill='x', pady=2)
        
        # Rainfall
        ttk.Label(main_frame, text="Rainfall Level:").pack(fill='x', pady=2)
        self.rainfall_var = tk.StringVar()
        rainfalls = ['low', 'medium', 'high']
        ttk.Combobox(main_frame, textvariable=self.rainfall_var, values=rainfalls).pack(fill='x', pady=2)
        
        # Humidity
        ttk.Label(main_frame, text="Humidity Level:").pack(fill='x', pady=2)
        self.humidity_var = tk.StringVar()
        humidities = ['low', 'medium', 'high']
        ttk.Combobox(main_frame, textvariable=self.humidity_var, values=humidities).pack(fill='x', pady=2)
        
        # Seasons frame
        seasons_frame = ttk.LabelFrame(main_frame, text="Seasons", padding="5")
        seasons_frame.pack(fill='x', pady=10)
        
        # Season months
        self.season_vars = {}
        seasons = ['winter', 'spring', 'summer', 'fall', 'rainy']
        
        for season in seasons:
            season_frame = ttk.Frame(seasons_frame)
            season_frame.pack(fill='x', pady=2)
            
            ttk.Label(season_frame, text=f"{season.title()} Months:").pack(side='left')
            var = tk.StringVar()
            ttk.Entry(season_frame, textvariable=var).pack(side='left', fill='x', expand=True, padx=5)
            self.season_vars[season] = var
            
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Add Location", command=self.save).pack(side='right')
        
    def save(self):
        """Save the location data"""
        # Get values
        name = self.name_var.get().strip()
        climate = self.climate_var.get().strip()
        soil_types = [s.strip() for s in self.soil_var.get().split(',') if s.strip()]
        rainfall = self.rainfall_var.get().strip()
        humidity = self.humidity_var.get().strip()
        
        # Validate required fields
        if not all([name, climate, soil_types, rainfall]):
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return
        
        # Process seasons
        seasons = {}
        for season, var in self.season_vars.items():
            months = [m.strip().lower() for m in var.get().split(',') if m.strip()]
            if months:
                seasons[season] = months
        
        # Create location info
        location_info = {
            "common_soil_types": soil_types,
            "climate": climate,
            "rainfall": rainfall,
            "humidity": humidity if humidity else None,
            "seasons": seasons
        }
        
        # Add location
        try:
            self.location_manager.add_location(name, location_info)
            self.result = True
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add location: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = False
        self.dialog.destroy()

class CropDialog:
    """Dialog for adding a new crop"""
    def __init__(self, parent, agri_wiz):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Crop")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.agri_wiz = agri_wiz
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create and show the dialog contents
        self.create_widgets()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
        
    def create_widgets(self):
        """Create the dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Crop name
        ttk.Label(main_frame, text="Crop Name:").pack(fill='x', pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).pack(fill='x', pady=2)
        
        # Soil types
        ttk.Label(main_frame, text="Suitable Soil Types (comma-separated):").pack(fill='x', pady=2)
        self.soil_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.soil_var).pack(fill='x', pady=2)
        
        # Climates
        ttk.Label(main_frame, text="Suitable Climates (comma-separated):").pack(fill='x', pady=2)
        self.climate_var = tk.StringVar()
        climates = ['tropical', 'subtropical', 'temperate', 'mediterranean']
        climate_frame = ttk.Frame(main_frame)
        climate_frame.pack(fill='x', pady=2)
        for climate in climates:
            ttk.Checkbutton(climate_frame, text=climate, variable=tk.StringVar(), 
                          command=lambda c=climate: self.toggle_climate(c)).pack(side='left')
        
        # Seasons
        ttk.Label(main_frame, text="Suitable Seasons (comma-separated):").pack(fill='x', pady=2)
        self.season_var = tk.StringVar()
        seasons = ['summer', 'winter', 'rainy', 'spring', 'fall']
        season_frame = ttk.Frame(main_frame)
        season_frame.pack(fill='x', pady=2)
        for season in seasons:
            ttk.Checkbutton(season_frame, text=season, variable=tk.StringVar(),
                          command=lambda s=season: self.toggle_season(s)).pack(side='left')
        
        # Water needs
        ttk.Label(main_frame, text="Water Needs:").pack(fill='x', pady=2)
        self.water_var = tk.StringVar()
        water_needs = ['low', 'medium', 'high']
        ttk.Combobox(main_frame, textvariable=self.water_var, values=water_needs).pack(fill='x', pady=2)
        
        # Humidity preference
        ttk.Label(main_frame, text="Humidity Preference (comma-separated):").pack(fill='x', pady=2)
        self.humidity_var = tk.StringVar()
        humidity_frame = ttk.Frame(main_frame)
        humidity_frame.pack(fill='x', pady=2)
        humidities = ['low', 'medium', 'high']
        for humidity in humidities:
            ttk.Checkbutton(humidity_frame, text=humidity, variable=tk.StringVar(),
                          command=lambda h=humidity: self.toggle_humidity(h)).pack(side='left')
        
        # Soil fertility
        ttk.Label(main_frame, text="Soil Fertility Requirements (comma-separated):").pack(fill='x', pady=2)
        self.fertility_var = tk.StringVar()
        fertility_frame = ttk.Frame(main_frame)
        fertility_frame.pack(fill='x', pady=2)
        fertilities = ['low', 'medium', 'high']
        for fertility in fertilities:
            ttk.Checkbutton(fertility_frame, text=fertility, variable=tk.StringVar(),
                          command=lambda f=fertility: self.toggle_fertility(f)).pack(side='left')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Add Crop", command=self.save).pack(side='right')
        
        # Initialize sets for multi-select options
        self.selected_climates = set()
        self.selected_seasons = set()
        self.selected_humidities = set()
        self.selected_fertilities = set()
        
    def toggle_climate(self, climate):
        """Toggle a climate selection"""
        if climate in self.selected_climates:
            self.selected_climates.remove(climate)
        else:
            self.selected_climates.add(climate)
        self.climate_var.set(','.join(sorted(self.selected_climates)))
        
    def toggle_season(self, season):
        """Toggle a season selection"""
        if season in self.selected_seasons:
            self.selected_seasons.remove(season)
        else:
            self.selected_seasons.add(season)
        self.season_var.set(','.join(sorted(self.selected_seasons)))
        
    def toggle_humidity(self, humidity):
        """Toggle a humidity selection"""
        if humidity in self.selected_humidities:
            self.selected_humidities.remove(humidity)
        else:
            self.selected_humidities.add(humidity)
        self.humidity_var.set(','.join(sorted(self.selected_humidities)))
        
    def toggle_fertility(self, fertility):
        """Toggle a fertility selection"""
        if fertility in self.selected_fertilities:
            self.selected_fertilities.remove(fertility)
        else:
            self.selected_fertilities.add(fertility)
        self.fertility_var.set(','.join(sorted(self.selected_fertilities)))
        
    def save(self):
        """Save the crop data"""
        # Get values
        name = self.name_var.get().strip()
        soil_types = self.soil_var.get().strip()
        climates = self.climate_var.get().strip()
        seasons = self.season_var.get().strip()
        water_needs = self.water_var.get().strip()
        humidity = self.humidity_var.get().strip()
        fertility = self.fertility_var.get().strip()
        
        # Validate required fields
        if not all([name, soil_types, climates, seasons, water_needs]):
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return
        
        # Create crop data
        crop_data = {
            "crop_name": name,
            "soil_types": soil_types,
            "climates": climates,
            "seasons": seasons,
            "water_needs": water_needs,
            "humidity_preference": humidity,
            "soil_fertility": fertility
        }
        
        # Add crop
        try:
            self.agri_wiz.add_crop(crop_data)
            self.result = True
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add crop: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = False
        self.dialog.destroy()

def main():
    """Main function to start the GUI application"""
    app = AgriWizGUI()
    app.run()

if __name__ == "__main__":
    main()