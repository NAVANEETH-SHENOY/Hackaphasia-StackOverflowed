"""
Weather Service Module
Handles weather data fetching and processing from OpenWeatherMap API
"""
import os
import json
import logging
from typing import Dict, Tuple, Optional
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class WeatherService:
    """
    Service for fetching and processing weather data
    """
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.cache = {}  # Simple in-memory cache
        self.cache_duration = timedelta(hours=1)  # Cache weather data for 1 hour
        
    def get_weather_data(self, lat: float, lon: float) -> Dict:
        """
        Fetch weather data for given coordinates with caching and error handling
        """
        cache_key = f"{lat},{lon}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                logger.info(f"Using cached weather data for {cache_key}")
                return cached_data
        
        try:
            # Make API request
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius for temperature
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Process and format the response
            raw_data = response.json()
            weather_data = {
                'temperature': raw_data['main']['temp'],
                'humidity': raw_data['main']['humidity'],
                'rainfall': self._get_rainfall(raw_data),
                'wind_speed': raw_data['wind']['speed'],
                'description': raw_data['weather'][0]['description'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache the results
            self.cache[cache_key] = (weather_data, datetime.now())
            
            return weather_data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._get_fallback_weather(lat, lon)
            
    def get_weather_by_district(self, district: str, coordinates_map: Dict) -> Optional[Dict]:
        """
        Get weather data for a district using district-to-coordinates mapping
        """
        if district not in coordinates_map:
            logger.error(f"District {district} not found in coordinates mapping")
            return None
            
        lat, lon = coordinates_map[district]
        return self.get_weather_data(lat, lon)
        
    def _get_rainfall(self, raw_data: Dict) -> float:
        """
        Extract rainfall data from API response with fallback
        """
        try:
            # Check rain data for last 1h or 3h
            if 'rain' in raw_data:
                return raw_data['rain'].get('1h', 0) or raw_data['rain'].get('3h', 0)
            return 0
        except Exception:
            return 0
            
    def _get_fallback_weather(self, lat: float, lon: float) -> Dict:
        """
        Provide reasonable fallback values based on location and season
        """
        month = datetime.now().month
        
        # Simplified seasonal estimation
        is_summer = month in [3, 4, 5]
        is_monsoon = month in [6, 7, 8, 9]
        is_winter = month in [11, 12, 1]
        
        if is_summer:
            temp = 35
            humidity = 50
            rainfall = 0
        elif is_monsoon:
            temp = 28
            humidity = 80
            rainfall = 5
        elif is_winter:
            temp = 20
            humidity = 60
            rainfall = 0
        else:
            temp = 25
            humidity = 65
            rainfall = 0
            
        return {
            'temperature': temp,
            'humidity': humidity,
            'rainfall': rainfall,
            'wind_speed': 10,
            'description': 'Fallback data',
            'timestamp': datetime.now().isoformat(),
            'is_fallback': True
        }