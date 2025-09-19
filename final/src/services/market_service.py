"""
Market Data Service Module
Handles market data collection and processing
"""
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for fetching and processing agricultural market data"""
    
    def __init__(self):
        """Initialize market data service"""
        load_dotenv()
        self.api_key = os.getenv('AGMARKNET_API_KEY')
        self.cache = {}
        self.cache_duration = timedelta(days=1)
        
    def get_price_history(self, commodity: str, days: int = 30) -> Optional[pd.DataFrame]:
        """
        Get historical price data for a commodity
        
        Args:
            commodity: Name of the commodity
            days: Number of days of history to fetch
            
        Returns:
            DataFrame with price history or None if failed
        """
        cache_key = f"{commodity}_{days}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data
        
        try:
            # In production, this would make an API call to Agmarknet
            # For hackathon demo, we'll generate synthetic data
            data = self._generate_synthetic_prices(commodity, days)
            
            # Cache the results
            self.cache[cache_key] = (data, datetime.now())
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching price history: {e}")
            return None
            
    def get_market_insights(self, commodity: str) -> Dict:
        """
        Get market insights for a commodity
        
        Args:
            commodity: Name of the commodity
            
        Returns:
            dict: Market insights including trend, volatility, etc.
        """
        price_history = self.get_price_history(commodity)
        
        if price_history is None:
            return {
                'trend': 'unknown',
                'volatility': 'unknown',
                'recommendation': 'insufficient data'
            }
            
        try:
            # Calculate basic statistics
            prices = price_history['price']
            current_price = prices.iloc[-1]
            avg_price = prices.mean()
            std_price = prices.std()
            
            # Determine trend
            short_ma = prices.rolling(window=7).mean().iloc[-1]
            long_ma = prices.rolling(window=30).mean().iloc[-1]
            
            if short_ma > long_ma:
                trend = 'upward'
            elif short_ma < long_ma:
                trend = 'downward'
            else:
                trend = 'stable'
                
            # Calculate volatility
            volatility = (std_price / avg_price) * 100
            
            # Generate insights
            insights = {
                'trend': trend,
                'current_price': round(current_price, 2),
                'average_price': round(avg_price, 2),
                'volatility_pct': round(volatility, 1),
                'recommendation': self._get_market_recommendation(
                    trend, volatility, current_price, avg_price
                )
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating market insights: {e}")
            return {
                'trend': 'unknown',
                'volatility': 'unknown',
                'recommendation': 'error in analysis'
            }
            
    def _generate_synthetic_prices(self, commodity: str, days: int) -> pd.DataFrame:
        """Generate synthetic price data for demo purposes"""
        base_prices = {
            'Rice': 2000, 'Wheat': 1800, 'Maize': 1500,
            'Cotton': 5000, 'Sugarcane': 300, 'Onion': 1200,
            'Potato': 800, 'Tomato': 1500
        }
        
        base_price = base_prices.get(commodity, 1000)
        dates = pd.date_range(end=datetime.now(), periods=days)
        
        # Generate prices with trend and seasonality
        trend = np.linspace(0, 0.1, days)  # Small upward trend
        seasonality = 0.1 * np.sin(np.linspace(0, 4*np.pi, days))  # Seasonal pattern
        noise = np.random.normal(0, 0.02, days)  # Random variations
        
        prices = base_price * (1 + trend + seasonality + noise)
        
        return pd.DataFrame({
            'date': dates,
            'price': prices.round(2)
        })
        
    def _get_market_recommendation(
        self,
        trend: str,
        volatility: float,
        current_price: float,
        avg_price: float
    ) -> str:
        """Generate market recommendation based on analysis"""
        if volatility > 20:
            return "High market volatility - exercise caution"
            
        price_diff_pct = ((current_price - avg_price) / avg_price) * 100
        
        if trend == 'upward':
            if price_diff_pct > 15:
                return "Consider selling - prices significantly above average"
            else:
                return "Upward trend - hold for potential gains"
        elif trend == 'downward':
            if price_diff_pct < -15:
                return "Prices below average - consider holding"
            else:
                return "Downward trend - sell if storage costs are high"
        else:
            return "Stable market - decide based on your storage capacity"