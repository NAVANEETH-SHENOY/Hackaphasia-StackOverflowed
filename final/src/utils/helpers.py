"""
Utility functions for the AgriTech project
"""
import os
import logging
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_district_coordinates() -> Dict[str, Tuple[float, float]]:
    """
    Load district to coordinates mapping
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
        "Lucknow": (26.8467, 80.9462)
    }

def create_feature_engineering_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create standard features for model training
    """
    df = df.copy()
    
    # Time-based features
    if 'Date' in df.columns:
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
        df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    
    # Rolling statistics for price data
    if 'Price' in df.columns:
        for window in [7, 14, 30]:
            df[f'Price_MA_{window}'] = df.groupby('Commodity')['Price'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            df[f'Price_Volatility_{window}'] = df.groupby('Commodity')['Price'].transform(
                lambda x: x.rolling(window=window, min_periods=1).std()
            )
    
    return df

def validate_input_data(data: Dict, required_fields: List[str]) -> Tuple[bool, str]:
    """
    Validate input data for API endpoints
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, "Data validation successful"

def format_price_response(prices: List[Dict]) -> Dict:
    """
    Format price forecast response
    """
    if not prices:
        return {
            'success': False,
            'error': 'No price data available'
        }
    
    return {
        'success': True,
        'forecast': [
            {
                'date': price['date'],
                'price': price['price'],
                'formatted_price': f"₹{price['price']:,.2f}"
            }
            for price in prices
        ]
    }

def format_crop_response(recommendations: List[Dict]) -> Dict:
    """
    Format crop recommendation response
    """
    if not recommendations:
        return {
            'success': False,
            'error': 'No recommendations available'
        }
    
    return {
        'success': True,
        'recommendations': [
            {
                'crop': rec['crop'],
                'suitability_score': rec['suitability_score'],
                'season_match': rec['season_match'],
                'weather_suitable': rec.get('weather_suitable', None),
                'confidence': 'High' if rec['suitability_score'] >= 80 else 
                            'Medium' if rec['suitability_score'] >= 60 else 'Low'
            }
            for rec in recommendations
        ]
    }

def get_current_season() -> str:
    """
    Get current agricultural season based on month
    """
    month = datetime.now().month
    
    if month in [6, 7, 8, 9]:
        return 'Kharif'
    elif month in [10, 11, 12, 1, 2]:
        return 'Rabi'
    else:
        return 'Zaid'