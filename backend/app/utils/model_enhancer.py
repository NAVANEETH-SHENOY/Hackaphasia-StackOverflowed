from typing import Dict, Optional, Union, List
import numpy as np

class ModelEnhancer:
    @staticmethod
    def enhance_crop_recommendation(
        base_prediction: Dict,
        weather_data: Optional[Dict] = None,
        soil_data: Optional[Dict] = None
    ) -> Dict:
        """
        Enhance crop recommendation with weather and soil data
        """
        if not weather_data:
            return base_prediction
            
        try:
            # Weather-based adjustments
            temperature = weather_data.get('temperature', 25)  # Default to 25°C
            humidity = weather_data.get('humidity', 60)  # Default to 60%
            rainfall = weather_data.get('rainfall', 0)
            
            # Adjust confidence scores based on weather conditions
            predictions = base_prediction['predictions']
            for crop in predictions:
                score = predictions[crop]
                
                # Temperature adjustment
                if 20 <= temperature <= 30:  # Optimal range
                    score *= 1.1
                elif temperature < 10 or temperature > 35:
                    score *= 0.8
                    
                # Humidity adjustment
                if 50 <= humidity <= 70:  # Optimal range
                    score *= 1.1
                elif humidity < 30 or humidity > 90:
                    score *= 0.9
                    
                # Rainfall impact
                if 0 <= rainfall <= 30:  # Light rain
                    score *= 1.05
                elif rainfall > 100:  # Heavy rain
                    score *= 0.7
                    
                predictions[crop] = min(score, 1.0)  # Cap at 1.0
                
            # Normalize scores
            total = sum(predictions.values())
            if total > 0:
                predictions = {k: v/total for k, v in predictions.items()}
                
            base_prediction['predictions'] = predictions
            base_prediction['weather_context'] = {
                'temperature': temperature,
                'humidity': humidity,
                'rainfall': rainfall
            }
            
            return base_prediction
            
        except Exception as e:
            print(f"Error enhancing crop recommendation: {str(e)}")
            return base_prediction
            
    @staticmethod
    def tune_prophet_params(
        historical_data: List[Dict],
        weather_data: Optional[Dict] = None
    ) -> Dict:
        """
        Tune Prophet parameters based on data characteristics
        """
        params = {
            'seasonality_mode': 'multiplicative',
            'changepoint_prior_scale': 0.05,
            'seasonality_prior_scale': 10.0
        }
        
        try:
            if len(historical_data) < 30:
                # Less data = more conservative
                params['changepoint_prior_scale'] = 0.01
                params['seasonality_prior_scale'] = 5.0
                
            # Check for high volatility
            prices = [d['price'] for d in historical_data]
            volatility = np.std(prices) / np.mean(prices)
            
            if volatility > 0.3:  # High volatility
                params['changepoint_prior_scale'] = 0.1
                
            # Weather impact on seasonality
            if weather_data:
                extreme_weather = (
                    weather_data.get('temperature', 25) > 35 or
                    weather_data.get('rainfall', 0) > 100
                )
                if extreme_weather:
                    params['seasonality_mode'] = 'additive'
                    
            return params
            
        except Exception as e:
            print(f"Error tuning Prophet parameters: {str(e)}")
            return params