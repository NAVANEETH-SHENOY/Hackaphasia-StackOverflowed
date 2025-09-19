"""
AgriTech ML Project - Main Demo Script
Demonstrates the usage of the refactored modules
"""
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from src.models import PriceForecastModel, CropRecommendationModel
from src.services import WeatherService, MarketDataService
from src.utils.helpers import load_district_coordinates, format_crop_response

def main():
    """
    Main demo function showing the usage of the refactored modules
    """
    print("🌾 AgriTech ML Project Demo")
    print("=" * 50)
    
    # Initialize services and models
    weather_service = WeatherService()
    market_service = MarketDataService()
    price_model = PriceForecastModel()
    crop_model = CropRecommendationModel()
    
    # 1. Get Weather Data
    print("\n📍 Getting weather data for Bangalore...")
    weather_data = weather_service.get_weather_by_district(
        "Bangalore",
        load_district_coordinates()
    )
    
    if weather_data:
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Rainfall: {weather_data['rainfall']} mm")
    
    # 2. Get Market Data
    print("\n💹 Getting market insights for Rice...")
    market_insights = market_service.get_market_insights("Rice")
    print(f"Market Trend: {market_insights['trend']}")
    print(f"Current Price: ₹{market_insights['current_price']}")
    print(f"Recommendation: {market_insights['recommendation']}")
    
    # 3. Get Crop Recommendations
    print("\n🌱 Getting crop recommendations for Karnataka...")
    location_data = {
        'state': 'Karnataka',
        'month': datetime.now().month,
        'soil_ph': 6.5
    }
    
    recommendations = crop_model.recommend_crops(
        location_data=location_data,
        weather_data=weather_data
    )
    
    formatted_recs = format_crop_response(recommendations)
    if formatted_recs['success']:
        print("\nTop Recommended Crops:")
        for rec in formatted_recs['recommendations']:
            print(f"- {rec['crop']}: {rec['suitability_score']}% suitable " +
                  f"(Confidence: {rec['confidence']})")
    
    # 4. Get Price Forecast
    print("\n📈 Getting 15-day price forecast for Rice...")
    sample_data = pd.DataFrame({
        'Date': pd.date_range(end=datetime.now(), periods=30),
        'Price': market_service.get_price_history('Rice', 30)['price']
    })
    
    forecast = price_model.predict(sample_data)
    if forecast:
        print("\nPrice Forecast:")
        for pred in forecast[:5]:  # Show first 5 days
            print(f"- {pred['date']}: ₹{pred['price']}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run demo
    main()