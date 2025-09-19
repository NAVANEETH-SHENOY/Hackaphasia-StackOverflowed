#!/usr/bin/env python3
"""
Test module for weather API integration
"""
import os
import unittest
from dotenv import load_dotenv
from backend.weather_service import WeatherService

# Load environment variables
load_dotenv()

class TestWeatherService(unittest.TestCase):
    """Test cases for WeatherService"""
    
    def setUp(self):
        self.weather_service = WeatherService()
        self.test_coordinates = {
            'Bangalore': (12.9716, 77.5946)
        }
        
    def test_weather_fetch(self):
        """Test weather data fetching"""
        lat, lon = self.test_coordinates['Bangalore']
        data = self.weather_service.get_weather_data(lat, lon)
        
        # Check structure and types
        self.assertIsInstance(data, dict)
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIn('rainfall', data)
        self.assertIn('wind_speed', data)
        
        # Check value ranges
        self.assertTrue(0 <= data['humidity'] <= 100)
        self.assertTrue(-20 <= data['temperature'] <= 50)
        self.assertTrue(data['rainfall'] >= 0)
        
    def test_district_lookup(self):
        """Test weather lookup by district name"""
        data = self.weather_service.get_weather_by_district(
            'Bangalore', self.test_coordinates
        )
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        
    def test_invalid_district(self):
        """Test handling of invalid district names"""
        data = self.weather_service.get_weather_by_district(
            'NonexistentDistrict', self.test_coordinates
        )
        self.assertIsNone(data)
        
    def test_fallback_behavior(self):
        """Test fallback behavior with invalid API key"""
        # Temporarily set invalid API key
        original_key = os.getenv('OPENWEATHERMAP_API_KEY')
        os.environ['OPENWEATHERMAP_API_KEY'] = 'invalid_key'
        
        lat, lon = self.test_coordinates['Bangalore']
        data = self.weather_service.get_weather_data(lat, lon)
        
        # Restore original key
        if original_key:
            os.environ['OPENWEATHERMAP_API_KEY'] = original_key
            
        # Check fallback data
        self.assertIsInstance(data, dict)
        self.assertIn('is_fallback', data)
        self.assertTrue(data['is_fallback'])
        
if __name__ == '__main__':
    unittest.main()

import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:5000"

def test_weather_api():
    """
    Test the weather API endpoint
    """
    print("🌤️ Testing AgriTech Weather API Integration")
    print("=" * 50)
    
    # Test districts
    test_districts = ["Bangalore", "Mumbai", "Delhi", "Pune", "Chennai"]
    
    for district in test_districts:
        print(f"\n📍 Testing weather for: {district}")
        print("-" * 30)
        
        try:
            # Make API call
            response = requests.get(
                f"{API_BASE_URL}/get-weather",
                params={"district": district},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Success!")
                print(f"   District: {data['district']}")
                print(f"   Coordinates: {data['coordinates']}")
                print(f"   Source: {data['source']}")
                
                # Current weather
                current = data['current']
                print(f"   🌡️ Temperature: {current['temperature']}°C")
                print(f"   💧 Humidity: {current['humidity']}%")
                print(f"   🌤️ Description: {current['description']}")
                
                # Forecast (first 3 days)
                forecast = data['forecast'][:3]
                print(f"   📅 3-Day Forecast:")
                for day in forecast:
                    print(f"      {day['date']}: {day['temperature']}°C, {day['description']}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    
    print(f"\n🎯 Weather API Test Complete!")
    print(f"📡 API Base URL: {API_BASE_URL}")
    print(f"🌐 Weather Endpoint: {API_BASE_URL}/get-weather?district=YourDistrict")

def test_api_health():
    """
    Test if the API is running
    """
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy!")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ API is not running. Please start the Flask server first.")
        print("   Run: python backend/backend.py")
        return False

if __name__ == "__main__":
    print("🚀 AgriTech Weather API Test Suite")
    print("=" * 50)
    
    # Check API health first
    if test_api_health():
        test_weather_api()
    else:
        print("\n💡 To start the API server:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up environment: Create .env file with AGRO_API_KEY")
        print("   3. Run server: python backend/backend.py")
        print("   4. Test again: python test_weather_api.py")
