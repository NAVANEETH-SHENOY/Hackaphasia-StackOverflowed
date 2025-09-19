import os
import requests
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather_by_coords(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch weather data for given coordinates
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rainfall': data.get('rain', {}).get('1h', 0),  # Rain in last 1 hour
                'description': data['weather'][0]['description']
            }
        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
            return None
    
    def get_weather_by_district(self, district: str) -> Optional[Dict]:
        """
        Fetch weather data for given district by first converting to coordinates
        """
        try:
            # Geocoding API to convert district to coordinates
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': f"{district},IN",  # IN for India
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(geocoding_url, params=params)
            response.raise_for_status()
            location_data = response.json()
            
            if not location_data:
                return None
                
            lat = location_data[0]['lat']
            lon = location_data[0]['lon']
            
            return self.get_weather_by_coords(lat, lon)
            
        except Exception as e:
            print(f"Error in district weather lookup: {str(e)}")
            return None