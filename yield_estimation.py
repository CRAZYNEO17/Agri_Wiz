#!/usr/bin/env python
# Yield Estimation Module for Agri Wiz
# Estimates crop yields based on environment and growing conditions

class YieldEstimator:
    def __init__(self):
        """Initialize the yield estimator with base yield data."""
        self.base_yields = {
            # Crop name: [min_yield_per_hectare, max_yield_per_hectare] in tons/hectare
            # Field crops
            "Rice": [2.5, 7.0],
            "Wheat": [2.0, 6.5],
            "Corn": [4.0, 12.0],
            "Cotton": [0.5, 2.0],  # In fiber tons
            "Sugarcane": [50.0, 120.0],
            "Potato": [15.0, 40.0],
            "Soybean": [1.5, 4.0],
            "Barley": [1.8, 5.0],
            "Oats": [1.5, 4.0],
            "Chickpea": [0.7, 2.0],
            "Mustard": [0.8, 1.5],
            "Groundnut": [1.0, 3.0],
            "Sunflower": [0.8, 2.0],
            
            # Fruits
            "Mango": [8.0, 15.0],
            "Banana": [30.0, 60.0],
            "Orange": [15.0, 30.0],
            "Apple": [15.0, 40.0],
            "Grape": [8.0, 20.0],
            "Coconut": [5000, 15000],  # Nuts per hectare
            
            # Vegetables and spices
            "Tomato": [20.0, 80.0],
            "Onion": [25.0, 50.0],
            "Garlic": [8.0, 15.0],
            "Turmeric": [5.0, 8.0],
            "Ginger": [12.0, 25.0],
            "Chili Pepper": [2.0, 5.0],
            "Cardamom": [0.15, 0.3],
            "Black Pepper": [0.5, 2.0],
            
            # Cash crops
            "Coffee": [0.5, 1.5],
            "Tea": [1.0, 3.0],
            "Cashew": [0.5, 2.0],
        }
        
        # Factors that affect yield as multipliers
        self.soil_fertility_factors = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.3
        }
        
        self.water_availability_factors = {
            "low": 0.6,
            "medium": 1.0,
            "high": 1.2
        }
        
        self.climate_match_factors = {
            "poor": 0.6,
            "fair": 0.9,
            "good": 1.0,
            "excellent": 1.2
        }
    
    def estimate_yield(self, crop_name, conditions):
        """
        Estimate the yield of a crop based on given conditions.
        
        Args:
            crop_name: Name of the crop
            conditions: Dict with keys:
                - soil_fertility: low/medium/high
                - water_availability: low/medium/high
                - climate_match: poor/fair/good/excellent
                - farm_management: 0-1 scale (0=poor, 1=excellent)
                - land_area: in hectares
                
        Returns:
            Dict with estimated yield information
        """
        if crop_name not in self.base_yields:
            return {
                "status": "error",
                "message": f"Yield data not available for {crop_name}"
            }
        
        # Extract conditions with defaults
        soil_fertility = conditions.get("soil_fertility", "medium")
        water_availability = conditions.get("water_availability", "medium")
        climate_match = conditions.get("climate_match", "fair")
        farm_management = conditions.get("farm_management", 0.5)  # Default to average
        land_area = conditions.get("land_area", 1.0)  # Default to 1 hectare
        
        # Normalize farm_management to ensure it's between 0 and 1
        farm_management = max(0, min(1, farm_management))
        
        # Get base yield range
        min_yield, max_yield = self.base_yields[crop_name]
        
        # Apply condition factors
        soil_factor = self.soil_fertility_factors.get(soil_fertility, 1.0)
        water_factor = self.water_availability_factors.get(water_availability, 1.0)
        climate_factor = self.climate_match_factors.get(climate_match, 0.9)
        
        # Combine factors and adjust yield range
        combined_factor = soil_factor * water_factor * climate_factor
        
        # Adjust the yield range
        adjusted_min_yield = min_yield * combined_factor * 0.9  # 10% below the factor-adjusted min
        adjusted_max_yield = max_yield * combined_factor * 1.1  # 10% above the factor-adjusted max
        
        # Determine expected yield based on farm management level
        # Poor management (0.0) gets near min yield, excellent (1.0) gets near max yield
        expected_yield = adjusted_min_yield + farm_management * (adjusted_max_yield - adjusted_min_yield)
        
        # Calculate total expected yield for the given land area
        total_yield = expected_yield * land_area
        
        # Calculate confidence interval (±20% for simplicity)
        yield_range = {
            "low": total_yield * 0.8,
            "expected": total_yield,
            "high": total_yield * 1.2
        }
        
        # Format return data
        return {
            "status": "success",
            "crop_name": crop_name,
            "yield_per_hectare": expected_yield,
            "total_yield": total_yield,
            "yield_range": yield_range,
            "land_area": land_area,
            "unit": "tons" if crop_name != "Coconut" else "nuts",
            "factors": {
                "soil_fertility": soil_fertility,
                "soil_factor": soil_factor,
                "water_availability": water_availability,
                "water_factor": water_factor,
                "climate_match": climate_match,
                "climate_factor": climate_factor,
                "farm_management": farm_management,
                "combined_factor": combined_factor
            }
        }
    
    def estimate_revenue(self, yield_data, price_per_unit):
        """
        Estimate revenue based on yield and market price.
        
        Args:
            yield_data: Result from estimate_yield
            price_per_unit: Price per unit (ton/kg/etc.)
            
        Returns:
            Dict with revenue information
        """
        if yield_data.get("status") != "success":
            return {
                "status": "error",
                "message": "Cannot estimate revenue without valid yield data"
            }
        
        # Extract yield information
        expected_yield = yield_data["total_yield"]
        yield_range = yield_data["yield_range"]
        
        # Calculate revenue
        expected_revenue = expected_yield * price_per_unit
        revenue_range = {
            "low": yield_range["low"] * price_per_unit,
            "expected": expected_revenue,
            "high": yield_range["high"] * price_per_unit
        }
        
        return {
            "status": "success",
            "expected_revenue": expected_revenue,
            "revenue_range": revenue_range,
            "price_per_unit": price_per_unit,
            "currency": "local currency"
        }
    
    def determine_climate_match(self, crop_climate_preference, actual_climate):
        """Determine how well the actual climate matches the crop's preference."""
        if crop_climate_preference == actual_climate:
            return "excellent"
        
        # Climate compatibility mapping
        climate_compatibility = {
            "tropical": {
                "tropical": "excellent",
                "subtropical": "good",
                "temperate": "poor",
                "mediterranean": "fair"
            },
            "subtropical": {
                "tropical": "good",
                "subtropical": "excellent",
                "temperate": "fair",
                "mediterranean": "good"
            },
            "temperate": {
                "tropical": "poor",
                "subtropical": "fair",
                "temperate": "excellent",
                "mediterranean": "good"
            },
            "mediterranean": {
                "tropical": "fair",
                "subtropical": "good",
                "temperate": "good", 
                "mediterranean": "excellent"
            }
        }
        
        # Get the compatibility or default to "poor"
        crop_climate = crop_climate_preference.lower()
        actual = actual_climate.lower()
        
        if crop_climate in climate_compatibility:
            return climate_compatibility[crop_climate].get(actual, "poor")
        
        return "poor"
    
    def determine_water_availability(self, water_needs, rainfall_level):
        """Determine water availability based on crop needs and rainfall."""
        # Mapping water needs to required rainfall levels
        water_needs_mapping = {
            "low": {"low": "medium", "medium": "high", "high": "high"},
            "medium": {"low": "low", "medium": "medium", "high": "high"},
            "high": {"low": "low", "medium": "low", "high": "medium"}
        }
        
        # Get the water availability or default to "medium"
        needs = water_needs.lower()
        rainfall = rainfall_level.lower()
        
        if needs in water_needs_mapping:
            return water_needs_mapping[needs].get(rainfall, "medium")
        
        return "medium"

# Simple test if run directly
if __name__ == "__main__":
    estimator = YieldEstimator()
    
    # Test with rice in good conditions
    conditions = {
        "soil_fertility": "high",
        "water_availability": "high",
        "climate_match": "excellent",
        "farm_management": 0.8,
        "land_area": 5.0  # 5 hectares
    }
    
    yield_data = estimator.estimate_yield("Rice", conditions)
    print(f"Rice yield estimation:")
    print(f"Expected yield: {yield_data['yield_per_hectare']:.2f} tons/hectare")
    print(f"Total yield for {yield_data['land_area']} hectares: {yield_data['total_yield']:.2f} tons")
    print(f"Yield range: {yield_data['yield_range']['low']:.2f} - {yield_data['yield_range']['high']:.2f} tons")
    
    # Test revenue estimation with a price of $400 per ton
    price_per_ton = 400
    revenue_data = estimator.estimate_revenue(yield_data, price_per_ton)
    print(f"\nRevenue estimation:")
    print(f"Expected revenue: ${revenue_data['expected_revenue']:.2f}")
    print(f"Revenue range: ${revenue_data['revenue_range']['low']:.2f} - ${revenue_data['revenue_range']['high']:.2f}")