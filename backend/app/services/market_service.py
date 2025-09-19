from typing import Dict, Optional, List
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd
from prophet import Prophet

class AgmarknetService:
    def __init__(self):
        # Base prices for different crops (INR per quintal)
        self.base_prices = {
            'Rice': 2200,
            'Wheat': 1950,
            'Maize': 1650,
            'Cotton': 5200,
            'Sugarcane': 350,
            'Onion': 1400,
            'Potato': 900,
            'Tomato': 1800,
            'Soybean': 4200,
            'Groundnut': 4800
        }
        self.seasonal_factors = {
            'Rice': {'peak_months': [11, 12, 1], 'lean_months': [5, 6, 7]},
            'Wheat': {'peak_months': [3, 4, 5], 'lean_months': [8, 9, 10]},
            'Maize': {'peak_months': [9, 10, 11], 'lean_months': [2, 3, 4]},
            'Cotton': {'peak_months': [10, 11, 12], 'lean_months': [4, 5, 6]},
            'Sugarcane': {'peak_months': [1, 2, 3], 'lean_months': [7, 8, 9]},
            'Onion': {'peak_months': [4, 5, 6], 'lean_months': [1, 2, 12]},
            'Potato': {'peak_months': [2, 3, 4], 'lean_months': [7, 8, 9]},
            'Tomato': {'peak_months': [6, 7, 8], 'lean_months': [1, 2, 12]},
            'Soybean': {'peak_months': [10, 11, 12], 'lean_months': [4, 5, 6]},
            'Groundnut': {'peak_months': [11, 12, 1], 'lean_months': [5, 6, 7]}
        }
    
    def get_price_history(self, commodity: str, market: str, days: int = 30) -> Optional[List[Dict]]:
        """
        Generate realistic mock historical price data using seasonal patterns
        """
        try:
            base_price = self.base_prices.get(commodity, 2000)
            end_date = datetime.now()
            price_history = []
            
            seasonal_info = self.seasonal_factors.get(commodity, {
                'peak_months': [7, 8, 9],
                'lean_months': [1, 2, 3]
            })
            
            for i in range(days):
                date = end_date - timedelta(days=i)
                
                # Seasonal adjustment
                month = date.month
                if month in seasonal_info['peak_months']:
                    seasonal_factor = random.uniform(1.1, 1.3)  # 10-30% higher in peak season
                elif month in seasonal_info['lean_months']:
                    seasonal_factor = random.uniform(0.7, 0.9)  # 10-30% lower in lean season
                else:
                    seasonal_factor = random.uniform(0.9, 1.1)  # Normal variation
                    
                # Add some random market variation
                market_variation = random.uniform(-0.1, 0.1)  # ±10% variation
                
                # Calculate final price
                price = base_price * seasonal_factor * (1 + market_variation)
                
                price_history.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': round(price, 2),
                    'min_price': round(price * 0.9, 2),
                    'max_price': round(price * 1.1, 2),
                    'arrivals': round(random.uniform(100, 1000), 2)
                })
            
            return price_history
            
        except Exception as e:
            print(f"Error fetching market data: {str(e)}")
            return None
            
    def enhance_forecast(self, prophet_forecast: Dict, commodity: str, market: str) -> Dict:
        """
        Enhance forecast using Prophet and market patterns
        """
        try:
            # Get historical data
            history = self.get_price_history(commodity, market, days=90)  # Get 90 days of history
            if not history:
                return prophet_forecast
                
            # Prepare data for Prophet
            df = pd.DataFrame(history)
            df['ds'] = pd.to_datetime(df['date'])
            df['y'] = df['price']
            
            # Initialize and fit Prophet model
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                seasonality_mode='multiplicative'
            )
            
            # Add commodity-specific seasonality
            seasonal_info = self.seasonal_factors.get(commodity, {})
            if seasonal_info:
                peak_months = seasonal_info.get('peak_months', [])
                for month in peak_months:
                    model.add_seasonality(
                        name=f'peak_month_{month}',
                        period=30.5,
                        fourier_order=5
                    )
                    
            model.fit(df)
            
            # Make future dataframe
            if 'forecast' in prophet_forecast:
                future_dates = pd.DataFrame([
                    {'ds': datetime.strptime(p['date'], '%Y-%m-%d')}
                    for p in prophet_forecast['forecast']
                ])
                
                # Predict
                forecast = model.predict(future_dates)
                
                # Update original forecast with Prophet predictions
                for i, point in enumerate(prophet_forecast['forecast']):
                    orig_price = point['price']
                    prophet_price = forecast.iloc[i]['yhat']
                    
                    # Blend original and Prophet predictions
                    blended_price = (orig_price + prophet_price) / 2
                    
                    point['price'] = round(blended_price, 2)
                    point['confidence_lower'] = round(forecast.iloc[i]['yhat_lower'], 2)
                    point['confidence_upper'] = round(forecast.iloc[i]['yhat_upper'], 2)
                    
                # Add market insights
                recent_prices = [h['price'] for h in history[:7]]  # Last 7 days
                prophet_forecast['market_insights'] = {
                    'recent_average': round(np.mean(recent_prices), 2),
                    'volatility': round(np.std(recent_prices), 2),
                    'trend': 'increasing' if forecast['trend'].iloc[-1] > forecast['trend'].iloc[0] else 'decreasing',
                    'seasonal_pattern': 'peak' if datetime.now().month in seasonal_info.get('peak_months', [])
                                      else 'lean' if datetime.now().month in seasonal_info.get('lean_months', [])
                                      else 'normal',
                    'confidence_score': 'high' if len(history) >= 60 else 'medium'
                }
            
            return prophet_forecast
            
        except Exception as e:
            print(f"Error enhancing forecast: {str(e)}")
            return prophet_forecast  # Return original forecast if enhancement fails