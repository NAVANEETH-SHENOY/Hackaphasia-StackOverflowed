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
            'Rice': {'peak_months': [11, 12, 1], 'lean_months': [5, 6, 7], 'demand': 'high', 'volatility': 'low'},
            'Wheat': {'peak_months': [3, 4, 5], 'lean_months': [8, 9, 10], 'demand': 'high', 'volatility': 'low'},
            'Maize': {'peak_months': [9, 10, 11], 'lean_months': [2, 3, 4], 'demand': 'moderate', 'volatility': 'moderate'},
            'Cotton': {'peak_months': [10, 11, 12], 'lean_months': [4, 5, 6], 'demand': 'high', 'volatility': 'high'},
            'Sugarcane': {'peak_months': [1, 2, 3], 'lean_months': [7, 8, 9], 'demand': 'moderate', 'volatility': 'low'},
            'Onion': {'peak_months': [4, 5, 6], 'lean_months': [1, 2, 12], 'demand': 'high', 'volatility': 'very_high'},
            'Potato': {'peak_months': [2, 3, 4], 'lean_months': [7, 8, 9], 'demand': 'high', 'volatility': 'moderate'},
            'Tomato': {'peak_months': [6, 7, 8], 'lean_months': [1, 2, 12], 'demand': 'high', 'volatility': 'very_high'},
            'Soybean': {'peak_months': [10, 11, 12], 'lean_months': [4, 5, 6], 'demand': 'moderate', 'volatility': 'high'},
            'Groundnut': {'peak_months': [11, 12, 1], 'lean_months': [5, 6, 7], 'demand': 'moderate', 'volatility': 'moderate'}
        }
        
        # Regional market strengths
        self.regional_market_strength = {
            'Maharashtra': {
                'Onion': 1.2, 'Cotton': 1.1, 'Soybean': 1.15,
                'Sugarcane': 1.1, 'Groundnut': 1.05
            },
            'Karnataka': {
                'Rice': 1.15, 'Maize': 1.2, 'Sugarcane': 1.1,
                'Tomato': 1.15, 'Onion': 1.1
            },
            'Andhra Pradesh': {
                'Rice': 1.2, 'Cotton': 1.15, 'Groundnut': 1.2,
                'Tomato': 1.1, 'Maize': 1.1
            },
            'Tamil Nadu': {
                'Rice': 1.15, 'Sugarcane': 1.2, 'Groundnut': 1.15,
                'Cotton': 1.1, 'Tomato': 1.1
            },
            'Gujarat': {
                'Cotton': 1.25, 'Groundnut': 1.2, 'Potato': 1.15,
                'Tomato': 1.1, 'Wheat': 1.1
            },
            'Madhya Pradesh': {
                'Soybean': 1.25, 'Wheat': 1.2, 'Cotton': 1.15,
                'Onion': 1.1, 'Maize': 1.1
            },
            'Uttar Pradesh': {
                'Wheat': 1.25, 'Sugarcane': 1.2, 'Potato': 1.2,
                'Rice': 1.15, 'Maize': 1.1
            }
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
    
    def get_market_analysis(self, crop: str, state: str = None) -> Dict:
        """
        Get comprehensive market analysis for a crop in a specific state
        """
        try:
            current_month = datetime.now().month
            current_day = datetime.now().day
            seasonal_info = self.seasonal_factors.get(crop, {})
            
            # Base demand calculation with daily variation
            base_demand = seasonal_info.get('demand', 'moderate')
            base_volatility = seasonal_info.get('volatility', 'moderate')
            
            # Add daily randomization factor
            daily_seed = int(f"{current_month}{current_day}")
            random.seed(daily_seed)
            daily_factor = random.uniform(0.8, 1.2)
            
            # Seasonal adjustment
            is_peak_season = current_month in seasonal_info.get('peak_months', [])
            is_lean_season = current_month in seasonal_info.get('lean_months', [])
            
            # Calculate demand with dynamic factors
            if is_peak_season:
                demand = self._upgrade_level(base_demand)
                if daily_factor > 1.1:
                    demand = self._upgrade_level(demand)
            elif is_lean_season:
                demand = self._downgrade_level(base_demand)
                if daily_factor < 0.9:
                    demand = self._downgrade_level(demand)
            else:
                demand = base_demand
                if daily_factor > 1.1:
                    demand = self._upgrade_level(demand)
                elif daily_factor < 0.9:
                    demand = self._downgrade_level(demand)
                
            # Generate dynamic regional factors
            if state and state in self.regional_market_strength:
                regional_strength = self.regional_market_strength[state].get(crop, 1.0)
                # Add daily variation to regional strength
                regional_variation = random.uniform(-0.05, 0.05)
                regional_strength = max(1.0, regional_strength + regional_variation)
                
                if regional_strength > 1.2:
                    demand = self._upgrade_level(demand)
                    competition = 'high' if daily_factor > 1.0 else 'moderate'
                elif regional_strength > 1.1:
                    competition = 'moderate' if daily_factor > 1.0 else 'low'
                else:
                    competition = 'low'
            else:
                regional_strength = 1.0
                competition = ['low', 'moderate', 'high'][int(random.uniform(0, 3))]
                
            # Dynamic price stability calculation
            stability_factors = []
            
            # Base volatility factor
            if base_volatility in ['high', 'very_high']:
                stability_factors.append('volatile')
            
            # Seasonal factor with daily variation
            if is_peak_season and daily_factor > 1.0:
                stability_factors.append('stable')
            elif is_lean_season or daily_factor < 0.9:
                stability_factors.append('volatile')
            
            # Market conditions factor
            market_condition = random.uniform(0, 1)
            if market_condition > 0.8:  # 20% chance of additional volatility
                stability_factors.append('volatile')
            
            # Calculate final price stability
            volatile_count = stability_factors.count('volatile')
            price_stability = 'volatile' if volatile_count >= 2 else 'stable'
                
            # Generate dynamic price history with trends
            base_price = self.base_prices.get(crop, 2000)
            price_history = []
            trend_factor = random.uniform(-0.2, 0.2)  # Random trend direction
            
            for i in range(30):
                day_factor = 1.0 + (trend_factor * (i/30))  # Progressive trend
                daily_noise = random.uniform(-0.05, 0.05)  # Daily variation
                seasonal_impact = 1.1 if is_peak_season else 0.9 if is_lean_season else 1.0
                
                price = base_price * day_factor * (1 + daily_noise) * seasonal_impact
                price_history.append({'price': price})
            
            # Calculate trend and volatility
            prices = [p['price'] for p in price_history]
            recent_prices = prices[-7:]  # Last week's prices
            
            # Dynamic trend calculation
            price_change = (prices[-1] - prices[0]) / prices[0]
            if abs(price_change) < 0.02:
                trend = 'stable'
            else:
                trend = 'increasing' if price_change > 0 else 'decreasing'
            
            # Calculate volatility with recent emphasis
            recent_volatility = np.std(recent_prices)
            overall_volatility = np.std(prices)
            volatility = (recent_volatility * 0.7 + overall_volatility * 0.3)  # Weighted average
                
            # Calculate market confidence score
            confidence_factors = {
                'data_quality': random.uniform(0.7, 1.0),
                'market_predictability': 0.8 if price_stability == 'stable' else 0.5,
                'seasonal_certainty': 1.0 if is_peak_season or is_lean_season else 0.7
            }
            confidence_score = sum(confidence_factors.values()) / len(confidence_factors)
            
            # Calculate price range
            avg_price = np.mean(prices)
            price_range = {
                'min': round(min(recent_prices), 2),
                'max': round(max(recent_prices), 2),
                'avg': round(avg_price, 2)
            }
            
            # Generate forward-looking forecast
            future_outlook = 'positive' if all([
                demand in ['high', 'very_high'],
                price_stability == 'stable',
                trend == 'increasing'
            ]) else 'negative' if all([
                demand in ['low'],
                price_stability == 'volatile',
                trend == 'decreasing'
            ]) else 'neutral'
            
            return {
                'demand': demand,
                'price_stability': price_stability,
                'competition': competition,
                'trend': trend,
                'regional_strength': round((regional_strength - 1) * 100) if state else 0,
                'seasonal_timing': 'peak' if is_peak_season else 'lean' if is_lean_season else 'normal',
                'market_volatility': round(volatility, 2),
                'confidence_score': round(confidence_score * 100),
                'price_range': price_range,
                'future_outlook': future_outlook,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error in market analysis: {str(e)}")
            return {
                'demand': 'moderate',
                'price_stability': 'stable',
                'competition': 'moderate',
                'trend': 'stable',
                'regional_strength': 0,
                'seasonal_timing': 'normal',
                'market_volatility': 0
            }
    
    def _upgrade_level(self, current_level: str) -> str:
        """Helper to upgrade demand/competition level"""
        levels = ['low', 'moderate', 'high', 'very_high']
        try:
            current_index = levels.index(current_level)
            return levels[min(current_index + 1, len(levels) - 1)]
        except ValueError:
            return current_level
    
    def _downgrade_level(self, current_level: str) -> str:
        """Helper to downgrade demand/competition level"""
        levels = ['low', 'moderate', 'high', 'very_high']
        try:
            current_index = levels.index(current_level)
            return levels[max(current_index - 1, 0)]
        except ValueError:
            return current_level
            
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