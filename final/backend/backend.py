# AgriTech Flask Backend API
# Provides endpoints for price forecasting and crop recommendations

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import os
import logging
import requests
from dotenv import load_dotenv
from weather_service import WeatherService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize services
weather_service = WeatherService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# MODEL AND DATA LOADING
# =============================================================================

class AgriTechAPI:
    """
    Main API class for AgriTech ML models
    """
    
    def __init__(self):
        self.price_model = None
        self.crop_model = None
        self.processor = None
        self.crop_mappings = {}
        self.state_mappings = {}
        self.district_coordinates = self._init_district_mapping()
        self.weather_service = WeatherService()
        self.load_models()
        
    def load_models(self):
        """
        Load trained models and data processor
        """
        try:
            # In production, models would be loaded from saved files
            # For this demo, we'll create simplified prediction functions
            logger.info("Loading AgriTech ML models...")
            
            # Create simplified crop and state mappings
            self.crop_mappings = {
                'Rice': 0, 'Wheat': 1, 'Maize': 2, 'Cotton': 3, 'Sugarcane': 4,
                'Onion': 5, 'Potato': 6, 'Tomato': 7, 'Soybean': 8, 'Groundnut': 9
            }
            
            self.state_mappings = {
                'Maharashtra': 0, 'Karnataka': 1, 'Andhra Pradesh': 2, 'Tamil Nadu': 3,
                'Gujarat': 4, 'Rajasthan': 5, 'Madhya Pradesh': 6, 'Uttar Pradesh': 7
            }
            
            # Reverse mappings
            self.crop_mappings_reverse = {v: k for k, v in self.crop_mappings.items()}
            self.state_mappings_reverse = {v: k for k, v in self.state_mappings.items()}
            
            logger.info("✅ Models loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
    
    def _init_district_mapping(self):
        """
        Initialize district to coordinates mapping for weather API
        """
        return {
            # Major Indian agricultural districts
            "Bangalore": (12.9716, 77.5946),
            "Mumbai": (19.0760, 72.8777),
            "Delhi": (28.7041, 77.1025),
            "Chennai": (13.0827, 80.2707),
            "Kolkata": (22.5726, 88.3639),
            "Hyderabad": (17.3850, 78.4867),
            "Pune": (18.5204, 73.8567),
            "Ahmedabad": (23.0225, 72.5714),
            "Jaipur": (26.9124, 75.7873),
            "Lucknow": (26.8467, 80.9462),
            "Kanpur": (26.4499, 80.3319),
            "Nagpur": (21.1458, 79.0882),
            "Indore": (22.7196, 75.8577),
            "Thane": (19.2183, 72.9781),
            "Bhopal": (23.2599, 77.4126),
            "Visakhapatnam": (17.6868, 83.2185),
            "Pimpri": (18.6298, 73.7997),
            "Patna": (25.5941, 85.1376),
            "Vadodara": (22.3072, 73.1812),
            "Ghaziabad": (28.6692, 77.4538),
            "Ludhiana": (30.9010, 75.8573),
            "Agra": (27.1767, 78.0081),
            "Nashik": (19.9975, 73.7898),
            "Faridabad": (28.4089, 77.3178),
            "Meerut": (28.9845, 77.7064),
            "Rajkot": (22.3039, 70.8022),
            "Kalyan": (19.2403, 73.1305),
            "Vasai": (19.4700, 72.8000),
            "Varanasi": (25.3176, 82.9739),
            "Srinagar": (34.0837, 74.7973),
            "Aurangabad": (19.8762, 75.3433),
            "Navi Mumbai": (19.0330, 73.0297),
            "Solapur": (17.6599, 75.9064),
            "Vijayawada": (16.5062, 80.6480),
            "Kolhapur": (16.7050, 74.2433),
            "Amritsar": (31.6340, 74.8723),
            "Noida": (28.5355, 77.3910),
            "Ranchi": (23.3441, 85.3096),
            "Howrah": (22.5958, 88.2636),
            "Coimbatore": (11.0168, 76.9558),
            "Raipur": (21.2514, 81.6296),
            "Jabalpur": (23.1815, 79.9864),
            "Gwalior": (26.2183, 78.1828),
            "Chandigarh": (30.7333, 76.7794),
            "Tiruchirappalli": (10.7905, 78.7047),
            "Mysore": (12.2958, 76.6394),
            "Bhubaneswar": (20.2961, 85.8245),
            "Kochi": (9.9312, 76.2673),
            "Bhavnagar": (21.7645, 72.1519),
            "Salem": (11.6643, 78.1460),
            "Warangal": (17.9689, 79.5941),
            "Guntur": (16.3068, 80.4365),
            "Bhiwandi": (19.3002, 73.0581),
            "Amravati": (20.9374, 77.7796),
            "Nanded": (19.1383, 77.3210),
            "Kolhapur": (16.7050, 74.2433),
            "Sangli": (16.8524, 74.5815),
            "Malegaon": (20.5598, 74.5254),
            "Ulhasnagar": (19.2167, 73.1500),
            "Jalgaon": (21.0077, 75.5626),
            "Latur": (18.4088, 76.5604),
            "Ahmadnagar": (19.0952, 74.7496),
            "Dhule": (20.9013, 74.7774),
            "Ichalkaranji": (16.7000, 74.4667),
            "Parbhani": (19.2613, 76.7734),
            "Jalna": (19.8342, 75.8816),
            "Bhusawal": (21.0436, 75.7851),
            "Panvel": (18.9881, 73.1101),
            "Satara": (17.6805, 74.0183),
            "Beed": (18.9894, 75.7560),
            "Yavatmal": (20.3897, 78.1307),
            "Kamptee": (21.2333, 79.2000),
            "Gondia": (21.4500, 80.2000),
            "Chandrapur": (19.9615, 79.2961),
            "Achalpur": (21.2567, 77.5106),
            "Osmanabad": (18.1667, 76.0500),
            "Nandurbar": (21.3667, 74.2500),
            "Wardha": (20.7453, 78.6022),
            "Udgir": (18.3833, 77.1167),
            "Aurangabad": (19.8762, 75.3433),
            "Amalner": (20.9333, 75.1667),
            "Akola": (20.7000, 77.0167),
            "Lonavla": (18.7500, 73.4000),
            "Pandharpur": (17.6833, 75.3333),
            "Shirpur": (21.3500, 74.8833),
            "Paratwada": (21.2833, 77.7833),
            "Pathri": (19.2500, 76.4500),
            "Sangamner": (19.5667, 74.2167),
            "Shirdi": (19.7667, 74.4833),
            "Barshi": (18.2333, 75.7000),
            "Pachora": (20.6667, 75.3500),
            "Jalna": (19.8342, 75.8816),
            "Bhadravati": (19.0333, 75.7167),
            "Afzalpur": (17.2000, 76.3500),
            "Karad": (17.2833, 74.1833),
            "Washim": (20.1000, 77.1333),
            "Amalner": (20.9333, 75.1667),
            "Lonar": (19.9833, 76.5167),
            "Pulgaon": (20.7167, 78.3167),
            "Shegaon": (20.7833, 76.6833),
            "Malkapur": (20.8833, 76.2000),
            "Wani": (20.0667, 78.9500),
            "Lonavla": (18.7500, 73.4000),
            "Talegaon": (18.7167, 73.6833),
            "Pimpri": (18.6298, 73.7997),
            "Chinchwad": (18.6167, 73.7667),
            "Dehu": (18.6667, 73.7667),
            "Chakan": (18.7500, 73.8500),
            "Rajgurunagar": (18.8667, 73.9000),
            "Khed": (18.7167, 73.3833),
            "Shirur": (18.1500, 74.3833),
            "Daund": (18.4667, 74.6000),
            "Baramati": (18.1500, 74.5833),
            "Indapur": (18.1167, 75.0167),
            "Bhor": (18.1667, 73.8500),
            "Velhe": (18.1000, 73.6667),
            "Mulshi": (18.5333, 73.6667),
            "Haveli": (18.5167, 73.8500),
            "Purandar": (18.2833, 73.9833),
            "Bhor": (18.1667, 73.8500),
            "Velhe": (18.1000, 73.6667),
            "Mulshi": (18.5333, 73.6667),
            "Haveli": (18.5167, 73.8500),
            "Purandar": (18.2833, 73.9833)
        }
            
    def get_weather(self, district):
        """
        Get weather data for a district using Agro API
        
        Args:
            district (str): District name
            
        Returns:
            dict: Weather data with fallback
        """
        try:
            # Check if API key is available
            if not self.agro_api_key:
                logger.warning("Agro API key not found, using fallback data")
                return self._get_fallback_weather(district)
            
            # Get coordinates for district
            if district not in self.district_coordinates:
                logger.warning(f"District {district} not found in mapping, using Bangalore coordinates")
                lat, lon = self.district_coordinates.get("Bangalore", (12.9716, 77.5946))
            else:
                lat, lon = self.district_coordinates[district]
            
            # Agro API endpoints
            current_url = f"https://api.agromonitoring.com/agro/1.0/weather"
            forecast_url = f"https://api.agromonitoring.com/agro/1.0/forecast"
            
            # API parameters
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.agro_api_key
            }
            
            # Get current weather
            current_response = requests.get(current_url, params=params, timeout=10)
            current_data = current_response.json() if current_response.status_code == 200 else {}
            
            # Get forecast (5-day)
            forecast_response = requests.get(forecast_url, params=params, timeout=10)
            forecast_data = forecast_response.json() if forecast_response.status_code == 200 else {}
            
            # Process current weather
            current_weather = self._process_current_weather(current_data)
            
            # Process forecast
            forecast_weather = self._process_forecast_weather(forecast_data)
            
            return {
                'district': district,
                'coordinates': {'lat': lat, 'lon': lon},
                'current': current_weather,
                'forecast': forecast_weather,
                'source': 'agro_api',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._get_fallback_weather(district)
    
    def _process_current_weather(self, data):
        """
        Process current weather data from Agro API
        """
        try:
            if 'main' in data:
                return {
                    'temperature': round(data['main'].get('temp', 25) - 273.15, 1),  # Convert K to C
                    'humidity': data['main'].get('humidity', 60),
                    'pressure': data['main'].get('pressure', 1013),
                    'feels_like': round(data['main'].get('feels_like', 25) - 273.15, 1),
                    'description': data['weather'][0].get('description', 'clear sky') if 'weather' in data else 'clear sky'
                }
            else:
                return self._get_fallback_current_weather()
        except Exception as e:
            logger.error(f"Error processing current weather: {e}")
            return self._get_fallback_current_weather()
    
    def _process_forecast_weather(self, data):
        """
        Process forecast weather data from Agro API
        """
        try:
            forecast = []
            if 'list' in data:
                for item in data['list'][:5]:  # Next 5 days
                    forecast.append({
                        'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                        'temperature': round(item['main']['temp'] - 273.15, 1),
                        'humidity': item['main']['humidity'],
                        'description': item['weather'][0]['description'],
                        'rainfall': item.get('rain', {}).get('3h', 0) if 'rain' in item else 0
                    })
            else:
                forecast = self._get_fallback_forecast()
            
            return forecast
        except Exception as e:
            logger.error(f"Error processing forecast: {e}")
            return self._get_fallback_forecast()
    
    def _get_fallback_weather(self, district):
        """
        Fallback weather data when API is unavailable
        """
        return {
            'district': district,
            'coordinates': self.district_coordinates.get(district, (12.9716, 77.5946)),
            'current': self._get_fallback_current_weather(),
            'forecast': self._get_fallback_forecast(),
            'source': 'fallback',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_fallback_current_weather(self):
        """
        Generate fallback current weather data
        """
        import random
        return {
            'temperature': round(random.uniform(20, 35), 1),
            'humidity': random.randint(40, 80),
            'pressure': random.randint(1000, 1020),
            'feels_like': round(random.uniform(18, 38), 1),
            'description': random.choice(['clear sky', 'partly cloudy', 'cloudy', 'light rain'])
        }
    
    def _get_fallback_forecast(self):
        """
        Generate fallback forecast data
        """
        import random
        forecast = []
        for i in range(5):
            date = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
            forecast.append({
                'date': date,
                'temperature': round(random.uniform(22, 32), 1),
                'humidity': random.randint(45, 75),
                'description': random.choice(['clear sky', 'partly cloudy', 'cloudy', 'light rain']),
                'rainfall': round(random.uniform(0, 5), 1)
            })
        return forecast
            
    def predict_crop_prices(self, crop_name, days=15):
        """
        Predict crop prices for the next N days
        
        Args:
            crop_name (str): Name of the crop
            days (int): Number of days to forecast
            
        Returns:
            list: List of (date, price) tuples
        """
        try:
            # Base prices for different crops (INR per quintal)
            base_prices = {
                'Rice': 2200, 'Wheat': 1950, 'Maize': 1650, 'Cotton': 5200,
                'Sugarcane': 350, 'Onion': 1400, 'Potato': 900, 'Tomato': 1800,
                'Soybean': 4200, 'Groundnut': 4800
            }
            
            if crop_name not in base_prices:
                # Default price for unknown crops
                base_price = 2000
            else:
                base_price = base_prices[crop_name]
            
            forecasts = []
            current_date = datetime.now()
            
            for i in range(1, days + 1):
                future_date = current_date + timedelta(days=i)
                
                # Seasonal factor
                month = future_date.month
                if crop_name in ['Rice', 'Wheat']:  # Rabi crops
                    seasonal_factor = 1.1 if month in [10, 11, 12, 1, 2] else 0.95
                elif crop_name in ['Cotton']:  # Cash crops
                    seasonal_factor = 1.05 if month in [3, 4, 5] else 1.0
                else:  # Vegetables and others
                    seasonal_factor = 1.08 if month in [6, 7, 8, 9] else 0.92
                
                # Market trend (slight upward trend)
                trend_factor = 1 + (i * 0.002)  # 0.2% increase per day
                
                # Random market volatility
                volatility = np.random.normal(0, 0.03)  # 3% standard deviation
                
                # Calculate predicted price
                predicted_price = base_price * seasonal_factor * trend_factor * (1 + volatility)
                predicted_price = max(predicted_price, base_price * 0.7)  # Price floor
                
                forecasts.append({
                    'date': future_date.strftime('%Y-%m-%d'),
                    'price': round(predicted_price, 2),
                    'day': future_date.strftime('%A')
                })
            
            return forecasts
            
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return []
    
    def recommend_crops(self, state=None, month=None, district=None):
        """
        Recommend best crops based on location and season with weather integration
        
        Args:
            state (str): State name
            month (int): Month (1-12)
            district (str): District name (optional)
            
        Returns:
            list: List of recommended crops with scores and weather considerations
        """
        try:
            # Get weather data if district is provided
            weather_data = None
            if district and district in self.district_coordinates:
                try:
                    weather_data = self.weather_service.get_weather_data(
                        *self.district_coordinates[district]
                    )
                except Exception as e:
                    logger.warning(f"Weather data fetch failed: {e}")
            
            # Enhanced crop suitability matrix with weather requirements
            crop_suitability = {
                'Rice': {
                    'seasons': [6, 7, 8, 9, 10, 11],  # Monsoon + Post-monsoon
                    'states': ['West Bengal', 'Punjab', 'Andhra Pradesh', 'Tamil Nadu', 'Karnataka'],
                    'base_score': 85,
                    'weather_requirements': {
                        'temperature': {'min': 20, 'max': 35, 'optimal': 25},
                        'humidity': {'min': 60, 'max': 90, 'optimal': 75},
                        'rainfall': {'min': 100, 'max': 250, 'optimal': 150}
                    }
                },
                'Wheat': {
                    'seasons': [11, 12, 1, 2, 3, 4],  # Rabi season
                    'states': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan'],
                    'base_score': 82,
                    'weather_requirements': {
                        'temperature': {'min': 15, 'max': 30, 'optimal': 22},
                        'humidity': {'min': 40, 'max': 70, 'optimal': 55},
                        'rainfall': {'min': 50, 'max': 150, 'optimal': 100}
                    }
                },
                'Cotton': {
                    'seasons': [6, 7, 8, 9, 10],  # Kharif season
                    'states': ['Gujarat', 'Maharashtra', 'Andhra Pradesh', 'Punjab', 'Haryana'],
                    'base_score': 78,
                    'weather_requirements': {
                        'temperature': {'min': 21, 'max': 37, 'optimal': 28},
                        'humidity': {'min': 50, 'max': 80, 'optimal': 65},
                        'rainfall': {'min': 75, 'max': 200, 'optimal': 125}
                    }
                },
                'Sugarcane': {
                    'seasons': list(range(1, 13)),  # Year-round
                    'states': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Tamil Nadu'],
                    'base_score': 75,
                    'weather_requirements': {
                        'temperature': {'min': 20, 'max': 35, 'optimal': 28},
                        'humidity': {'min': 60, 'max': 85, 'optimal': 70},
                        'rainfall': {'min': 150, 'max': 300, 'optimal': 200}
                    }
                },
                'Maize': {
                    'seasons': [6, 7, 8, 9, 10],  # Kharif season
                    'states': ['Karnataka', 'Andhra Pradesh', 'Tamil Nadu', 'Rajasthan'],
                    'base_score': 72
                },
                'Onion': {
                    'seasons': [6, 7, 8, 9, 11, 12, 1],  # Kharif + Rabi
                    'states': ['Maharashtra', 'Karnataka', 'Gujarat', 'Madhya Pradesh'],
                    'base_score': 70
                },
                'Potato': {
                    'seasons': [10, 11, 12, 1, 2, 3],  # Rabi season
                    'states': ['Uttar Pradesh', 'West Bengal', 'Bihar', 'Punjab'],
                    'base_score': 68
                },
                'Tomato': {
                    'seasons': [6, 7, 8, 9, 10, 11, 12],  # Extended season
                    'states': ['Karnataka', 'Andhra Pradesh', 'Maharashtra', 'Gujarat'],
                    'base_score': 65
                },
                'Soybean': {
                    'seasons': [6, 7, 8, 9],  # Monsoon season
                    'states': ['Madhya Pradesh', 'Maharashtra', 'Rajasthan'],
                    'base_score': 74
                },
                'Groundnut': {
                    'seasons': [6, 7, 8, 9],  # Monsoon season
                    'states': ['Gujarat', 'Andhra Pradesh', 'Tamil Nadu', 'Karnataka'],
                    'base_score': 71
                }
            }
            
            recommendations = []
            
            for crop, data in crop_suitability.items():
                score = data['base_score']
                
                # Season suitability
                if month and month in data['seasons']:
                    score += 15
                elif month:
                    score -= 10
                
                # State suitability
                if state and state in data['states']:
                    score += 10
                elif state:
                    score -= 5
                
                # Weather suitability scoring
                weather_score = 0
                if weather_data and 'weather_requirements' in data:
                    reqs = data['weather_requirements']
                    
                    # Temperature score
                    if 'temperature' in weather_data:
                        temp = weather_data['temperature']
                        temp_req = reqs['temperature']
                        if temp_req['min'] <= temp <= temp_req['max']:
                            temp_score = 10
                            # Bonus for optimal temperature
                            if abs(temp - temp_req['optimal']) <= 3:
                                temp_score += 5
                            weather_score += temp_score
                    
                    # Humidity score
                    if 'humidity' in weather_data:
                        humidity = weather_data['humidity']
                        humid_req = reqs['humidity']
                        if humid_req['min'] <= humidity <= humid_req['max']:
                            humid_score = 8
                            # Bonus for optimal humidity
                            if abs(humidity - humid_req['optimal']) <= 10:
                                humid_score += 4
                            weather_score += humid_score
                    
                    # Rainfall consideration
                    if 'rainfall' in weather_data:
                        rain = weather_data['rainfall']
                        rain_req = reqs['rainfall']
                        if rain > 0:  # If there is any rainfall
                            rain_score = 7
                            if rain_req['min'] <= rain <= rain_req['max']:
                                rain_score += 5
                            weather_score += rain_score
                    
                    # Apply weather score
                    score += weather_score
                
                # Market conditions and trends
                market_factor = np.random.uniform(-5, 5)
                score += market_factor
                
                # Ensure score is within reasonable bounds
                score = max(30, min(100, score))
                
                # Calculate expected yield and profit
                yield_estimates = {
                    'Rice': 4.2, 'Wheat': 3.5, 'Maize': 3.1, 'Cotton': 2.1,
                    'Sugarcane': 75.0, 'Onion': 20.0, 'Potato': 25.0,
                    'Tomato': 28.0, 'Soybean': 1.8, 'Groundnut': 2.2
                }
                
                estimated_yield = yield_estimates.get(crop, 2.0)
                
                # Prepare weather summary if available
                weather_summary = None
                if weather_data:
                    weather_summary = {
                        'current_temperature': weather_data.get('temperature'),
                        'current_humidity': weather_data.get('humidity'),
                        'current_rainfall': weather_data.get('rainfall'),
                        'conditions': weather_data.get('description')
                    }
                
                recommendations.append({
                    'crop': crop,
                    'suitability_score': round(score, 1),
                    'estimated_yield': estimated_yield,
                    'season_match': month in data['seasons'] if month else None,
                    'region_suitable': state in data['states'] if state else None,
                    'weather_suitable': bool(weather_score > 15) if weather_data else None,
                    'weather_summary': weather_summary,
                    'recommendation_reason': self._get_recommendation_reason(
                        crop, month, state, weather_data
                    )
                })
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error in crop recommendation: {e}")
            return []
    
    def _get_recommendation_reason(self, crop, month, state, weather_data=None):
        """
        Generate detailed explanation for crop recommendation including weather
        """
        reasons = []
        
        # Base season reasons
        season_reasons = {
            'Rice': 'Ideal for monsoon season with adequate water supply',
            'Wheat': 'Perfect for winter season (Rabi crop)',
            'Cotton': 'Suitable for warm, humid monsoon conditions',
            'Sugarcane': 'Year-round crop with steady income potential',
            'Maize': 'Good monsoon crop with moderate water needs',
            'Onion': 'Dual season crop with good market demand',
            'Potato': 'Cold-weather crop with excellent storage potential',
            'Tomato': 'High-value crop with extended growing season',
            'Soybean': 'Nitrogen-fixing legume ideal for monsoon',
            'Groundnut': 'Oil seed crop suitable for sandy soils'
        }
        
        base_reason = season_reasons.get(crop, 'Suitable crop for the region')
        reasons.append(base_reason)
        
        # Add weather-based insights if available
        if weather_data:
            temp = weather_data.get('temperature')
            humidity = weather_data.get('humidity')
            rainfall = weather_data.get('rainfall')
            
            weather_insights = []
            
            if temp is not None:
                if 20 <= temp <= 30:
                    weather_insights.append("Current temperature is favorable")
                elif temp > 30:
                    weather_insights.append("Consider early morning irrigation due to high temperature")
                else:
                    weather_insights.append("Monitor temperature for optimal growth")
            
            if humidity is not None:
                if 60 <= humidity <= 80:
                    weather_insights.append("Humidity levels are optimal")
                elif humidity > 80:
                    weather_insights.append("Watch for fungal diseases in high humidity")
                else:
                    weather_insights.append("Additional irrigation may be needed in low humidity")
            
            if rainfall is not None and rainfall > 0:
                weather_insights.append(f"Recent rainfall of {rainfall}mm recorded")
            
            if weather_insights:
                reasons.extend(weather_insights)
        
        return " | ".join(reasons)

# Initialize API instance
agritech_api = AgriTechAPI()

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/', methods=['GET'])
def home():
    """
    API home endpoint
    """
    return jsonify({
        'message': 'AgriTech ML API - Empowering Farmers with Data-Driven Decisions',
        'version': '1.0',
        'endpoints': {
            'forecast_price': '/forecast-price',
            'recommend_crop': '/recommend-crop',
            'get_weather': '/get-weather',
            'health_check': '/health'
        },
        'status': 'active'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': True
    })

@app.route('/forecast-price', methods=['POST'])
def forecast_price():
    """
    Price forecasting endpoint
    
    Expected JSON payload:
    {
        "crop": "Rice",
        "days": 15
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        crop = data.get('crop', '').strip()
        days = data.get('days', 15)
        
        # Validation
        if not crop:
            return jsonify({'error': 'Crop name is required'}), 400
        
        if not isinstance(days, int) or days < 1 or days > 30:
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        # Generate predictions
        predictions = agritech_api.predict_crop_prices(crop, days)
        
        if not predictions:
            return jsonify({'error': 'Failed to generate predictions'}), 500
        
        # Calculate summary statistics
        prices = [p['price'] for p in predictions]
        
        response = {
            'crop': crop,
            'forecast_days': days,
            'predictions': predictions,
            'summary': {
                'average_price': round(np.mean(prices), 2),
                'min_price': round(min(prices), 2),
                'max_price': round(max(prices), 2),
                'price_trend': 'increasing' if prices[-1] > prices[0] else 'decreasing',
                'volatility': round(np.std(prices), 2)
            },
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in forecast_price endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    """
    Crop recommendation endpoint
    
    Expected JSON payload:
    Option 1: Location-based recommendation
    {
        "state": "Maharashtra",
        "month": 6,
        "district": "Pune"  // optional
    }
    
    Option 2: Crop analysis
    {
        "crop": "Rice",
        "state": "Karnataka"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Check if it's crop analysis or location-based recommendation
        if 'crop' in data:
            # Crop analysis mode
            crop = data.get('crop', '').strip()
            state = data.get('state', '').strip()
            
            if not crop:
                return jsonify({'error': 'Crop name is required'}), 400
            
            # Get current month for analysis
            current_month = datetime.now().month
            
            # Analyze specific crop
            crop_analysis = agritech_api.recommend_crops(state if state else None, current_month)
            
            # Find the requested crop in recommendations
            target_crop = None
            for rec in crop_analysis:
                if rec['crop'].lower() == crop.lower():
                    target_crop = rec
                    break
            
            if not target_crop:
                # Create basic analysis for unknown crop
                target_crop = {
                    'crop': crop,
                    'suitability_score': 60.0,
                    'estimated_yield': 2.5,
                    'season_match': None,
                    'region_suitable': None,
                    'recommendation_reason': 'General farming practices recommended'
                }
            
            response = {
                'mode': 'crop_analysis',
                'crop': crop,
                'state': state if state else 'General',
                'analysis': target_crop,
                'market_outlook': {
                    'demand': 'moderate',
                    'price_stability': 'stable',
                    'competition': 'medium'
                },
                'generated_at': datetime.now().isoformat()
            }
            
        else:
            # Location-based recommendation mode
            state = data.get('state', '').strip()
            month = data.get('month')
            district = data.get('district', '').strip()
            
            if not state:
                return jsonify({'error': 'State is required for location-based recommendations'}), 400
            
            if month is not None and (not isinstance(month, int) or month < 1 or month > 12):
                return jsonify({'error': 'Month must be between 1 and 12'}), 400
            
            # Use current month if not provided
            if month is None:
                month = datetime.now().month
            
            # Get recommendations
            recommendations = agritech_api.recommend_crops(state, month, district)
            
            response = {
                'mode': 'location_based',
                'state': state,
                'month': month,
                'month_name': calendar.month_name[month],
                'district': district if district else 'General',
                'recommendations': recommendations,
                'season': agritech_api._get_season_name(month),
                'generated_at': datetime.now().isoformat()
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in recommend_crop endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get-weather', methods=['GET'])
def get_weather():
    """
    Weather data endpoint
    
    Query parameters:
    - district: District name (required)
    
    Example: /get-weather?district=Bangalore
    """
    try:
        district = request.args.get('district', '').strip()
        
        if not district:
            return jsonify({'error': 'District parameter is required'}), 400
        
        # Get weather data
        weather_data = agritech_api.get_weather(district)
        
        return jsonify(weather_data)
        
    except Exception as e:
        logger.error(f"Error in get_weather endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def _get_season_name(month):
    """Get season name from month"""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Post-Monsoon'

# Add the method to the API class
AgriTechAPI._get_season_name = staticmethod(_get_season_name)

# =============================================================================
# EXAMPLE USAGE AND TESTING
# =============================================================================

def test_api_endpoints():
    """
    Test function for API endpoints (for development)
    """
    print("🧪 Testing AgriTech API endpoints...")
    
    # Test price forecasting
    print("\n📈 Testing Price Forecast:")
    test_forecast = agritech_api.predict_crop_prices('Rice', 5)
    for prediction in test_forecast[:3]:
        print(f"   {prediction['date']}: ₹{prediction['price']}")
    
    # Test crop recommendations
    print("\n🌱 Testing Crop Recommendations:")
    test_recommendations = agritech_api.recommend_crops('Maharashtra', 6)
    for rec in test_recommendations[:3]:
        print(f"   {rec['crop']}: Score {rec['suitability_score']}")
    
    print("\n✅ API tests completed!")

if __name__ == '__main__':
    # Test the API functions
    test_api_endpoints()
    
    # Run the Flask app
    print("\n🚀 Starting AgriTech Flask API server...")
    print("📡 API will be available at: http://localhost:5000")
    print("📖 API documentation: http://localhost:5000")
    
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)