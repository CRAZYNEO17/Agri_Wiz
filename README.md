# Agri Wiz - Crop Recommendation System

Agri Wiz is an intelligent crop recommendation system designed to help farmers make informed decisions about which crops to plant based on their specific environmental conditions. The application uses data such as soil type, climate, season, rainfall, humidity, and soil fertility to provide tailored crop recommendations.

## Features

- **Location-Based Recommendations**: Get crop recommendations based on preset location data
- **Custom Recommendations**: Input your specific environmental parameters for personalized crop suggestions
- **Extensive Crop Database**: Contains data for 30+ crops with detailed information on growth requirements
- **Alternative Suggestions**: When exact matches aren't found, receive alternative crops with a match percentage
- **User-Friendly Interface**: Simple command-line interface with clear instructions
- **Expandable Database**: Easily add new crops and locations to the database

## Requirements

- Python 3.6 or higher
- No additional libraries required (uses only standard Python libraries)

## Installation

1. Clone or download this repository to your local machine
2. Navigate to the project directory
3. No additional installation steps needed - the application is ready to run!

## Usage

### Running the Application

To start the application, run the following command in your terminal:

```
python agri_wiz.py
```

### Main Menu Options

When you run the application, you'll see the following menu:

1. **Get crop recommendations**: Input soil type, climate, and other parameters to get personalized crop recommendations
2. **Get recommendations by location**: Select from pre-defined locations to get region-specific recommendations
3. **Add new crop to database**: Expand the crop database with new entries
4. **View all crops in database**: Browse the complete crop database
5. **Manage locations**: View or add location information
6. **Exit**: Quit the application

### Getting Recommendations

#### Option 1: Custom Recommendations

This option allows you to input specific parameters:
- Soil type (clay/loamy/sandy/black soil)
- Climate (tropical/subtropical/temperate)
- Season (summer/winter/rainy/spring/fall)
- Rainfall level (optional)
- Humidity level (optional)
- Soil fertility (optional)

Based on these inputs, the application will recommend suitable crops or provide alternatives if no exact matches are found.

#### Option 2: Location-Based Recommendations

This option uses predefined location data:
1. Select from available locations
2. Optionally provide additional parameters like humidity and soil fertility
3. Receive recommendations based on the location's soil, climate, and current season

### Database Management

#### Adding New Crops

You can add new crops to the database with the following information:
- Crop name
- Suitable soil types
- Suitable climates
- Suitable seasons
- Water needs
- Humidity preference
- Soil fertility requirements

#### Adding New Locations

You can add new locations with the following details:
- Location name
- Common soil types
- Climate
- Rainfall level
- Humidity level
- Seasonal information (months for each season)

## Data Structure

### Crop Data

The application stores crop data in a CSV file (`crop_data.csv`) with the following fields:
- `crop_name`: Name of the crop
- `soil_types`: Comma-separated list of suitable soil types
- `climates`: Comma-separated list of suitable climates
- `seasons`: Comma-separated list of suitable growing seasons
- `water_needs`: Low/medium/high
- `humidity_preference`: Preferred humidity levels
- `soil_fertility`: Required soil fertility levels

### Location Data

Location data is stored in a JSON file (`location_data.json`) with the following structure for each location:
- `common_soil_types`: Array of common soil types in the region
- `climate`: Predominant climate of the region
- `rainfall`: Typical rainfall level
- `humidity`: Typical humidity level
- `seasons`: Object mapping season names to arrays of month names

## Extending the Application

### Adding More Parameters

To add new crop parameters:
1. Update the `create_sample_data` method in `AgriWiz` class
2. Update the `get_recommendations` method to consider the new parameter
3. Modify the user interface in the `main` function to collect the new parameter

## Example Workflow

1. Run the application: `python agri_wiz.py`
2. Choose option 2 for location-based recommendations
3. Enter "Punjab India" as your location
4. Optionally specify humidity and soil fertility
5. Review the recommendations tailored for Punjab's environment

## Contributing

Contributions to improve Agri Wiz are welcome! Ways to contribute:
- Add more crops to the database
- Add more locations with accurate environmental data
- Improve the recommendation algorithm
- Enhance the user interface

## License

This project is open-source and available under the MIT License.

---

Created by Agri Wiz Team