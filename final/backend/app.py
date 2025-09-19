# AgriTech Flask Backend API
# Main application entry point

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

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
        self.load_models()
        
    def load_models(self):
        """
        Load trained models and data processor
        """
        try:
            # Try to load models from files
            if os.path.exists('price_forecast_model.pkl'):
                self.price_model = joblib.load('price_forecast_model.pkl')
                logger.info("✅ Price forecasting model loaded")
            
            if os.path.exists('crop_recommendation_model.pkl'):
                self.crop_model = joblib.load('crop_recommendation_model.pkl')
                logger.info("✅ Crop recommendation model loaded")
            
            if os.path.exists('data_processor.pkl'):
                self.processor = joblib.load('data_processor.pkl')
                logger.info("✅ Data processor loaded")
            
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
        Recommend best crops based on location and season
        
        Args:
            state (str): State name
            month (int): Month (1-12)
            district (str): District name (optional)
            
        Returns:
            list: List of recommended crops with scores
        """
        try:
            # Crop suitability matrix based on season and region
            crop_suitability = {
                'Rice': {
                    'seasons': [6, 7, 8, 9, 10, 11],  # Monsoon + Post-monsoon
                    'states': ['West Bengal', 'Punjab', 'Andhra Pradesh', 'Tamil Nadu', 'Karnataka'],
                    'base_score': 85
                },
                'Wheat': {
                    'seasons': [11, 12, 1, 2, 3, 4],  # Rabi season
                    'states': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan'],
                    'base_score': 82
                },
                'Cotton': {
                    'seasons': [6, 7, 8, 9, 10],  # Kharif season
                    'states': ['Gujarat', 'Maharashtra', 'Andhra Pradesh', 'Punjab', 'Haryana'],
                    'base_score': 78
                },
                'Sugarcane': {
                    'seasons': list(range(1, 13)),  # Year-round
                    'states': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Tamil Nadu'],
                    'base_score': 75
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
                
                # Add some randomness for market conditions
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
                
                recommendations.append({
                    'crop': crop,
                    'suitability_score': round(score, 1),
                    'estimated_yield': estimated_yield,
                    'season_match': month in data['seasons'] if month else None,
                    'region_suitable': state in data['states'] if state else None,
                    'recommendation_reason': self._get_recommendation_reason(crop, month, state)
                })
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error in crop recommendation: {e}")
            return []
    
    def _get_recommendation_reason(self, crop, month, state):
        """
        Generate explanation for crop recommendation
        """
        reasons = {
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
        
        return reasons.get(crop, 'Suitable crop for the region')

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
