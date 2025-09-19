"""
Crop Recommendation Model Module
Uses ensemble learning for accurate crop suggestions based on multiple factors
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import logging

logger = logging.getLogger(__name__)

class CropRecommendationModel:
    """Crop recommendation model with weather integration"""
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.scaler = StandardScaler()
        self.crop_suitability = self._init_crop_suitability()
        
    def _init_crop_suitability(self):
        """Initialize crop suitability requirements"""
        return {
            'Rice': {
                'seasons': [6, 7, 8, 9, 10, 11],  # Monsoon + Post-monsoon
                'weather': {
                    'temperature': {'min': 20, 'max': 35, 'optimal': 25},
                    'humidity': {'min': 60, 'max': 90, 'optimal': 75},
                    'rainfall': {'min': 100, 'max': 250, 'optimal': 150}
                }
            },
            'Wheat': {
                'seasons': [11, 12, 1, 2, 3, 4],  # Rabi season
                'weather': {
                    'temperature': {'min': 15, 'max': 30, 'optimal': 22},
                    'humidity': {'min': 40, 'max': 70, 'optimal': 55},
                    'rainfall': {'min': 50, 'max': 150, 'optimal': 100}
                }
            },
            'Cotton': {
                'seasons': [6, 7, 8, 9, 10],  # Kharif season
                'weather': {
                    'temperature': {'min': 21, 'max': 37, 'optimal': 28},
                    'humidity': {'min': 50, 'max': 80, 'optimal': 65},
                    'rainfall': {'min': 75, 'max': 200, 'optimal': 125}
                }
            }
            # Add more crops with their requirements
        }
        
    def prepare_features(self, df):
        """Prepare features for crop recommendation"""
        feature_cols = [
            'State_encoded', 'Month', 'Month_sin', 'Month_cos',
            'Yield_Tonnes_per_Hectare', 'Rainfall_mm', 'Temperature_avg',
            'Soil_pH', 'Marketability_Index'
        ]
        
        # Filter available columns
        self.feature_names = [col for col in feature_cols if col in df.columns]
        return df[self.feature_names].copy()
        
    def train(self, df):
        """Train the crop recommendation model"""
        logger.info("Training crop recommendation model...")
        
        X = self.prepare_features(df)
        y = df['Crop_encoded'].copy()
        
        # Remove NaN values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.model = self._train_xgboost(X_train, y_train)
        
        # Calculate metrics
        train_accuracy = accuracy_score(y_train, self.model.predict(X_train))
        test_accuracy = accuracy_score(y_test, self.model.predict(X_test))
        
        return {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy
        }
        
    def _train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier with optimized parameters"""
        params = {
            'objective': 'multi:softprob',
            'n_estimators': 800,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
        
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)
        return model
        
    def recommend_crops(self, location_data, weather_data=None):
        """
        Generate crop recommendations based on location and weather data
        
        Args:
            location_data (dict): Contains state, month, soil_ph, etc.
            weather_data (dict): Optional current weather conditions
        """
        try:
            recommendations = []
            current_month = location_data.get('month', pd.Timestamp.now().month)
            
            for crop, data in self.crop_suitability.items():
                score = self._calculate_base_score(crop, location_data)
                
                # Weather suitability if data available
                if weather_data:
                    weather_score = self._calculate_weather_score(crop, weather_data)
                    score += weather_score
                
                # Season suitability
                if current_month in data['seasons']:
                    score += 15
                else:
                    score -= 10
                
                # Ensure score is within bounds
                score = max(30, min(100, score))
                
                recommendations.append({
                    'crop': crop,
                    'suitability_score': round(score, 1),
                    'season_match': current_month in data['seasons'],
                    'weather_suitable': weather_data is not None
                })
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error in crop recommendation: {e}")
            return []
            
    def _calculate_base_score(self, crop, location_data):
        """Calculate base suitability score"""
        base_score = 70  # Default base score
        
        # Adjust based on soil pH if available
        if 'soil_ph' in location_data:
            ph = location_data['soil_ph']
            if 6.0 <= ph <= 7.5:  # Optimal range for most crops
                base_score += 10
            elif 5.5 <= ph <= 8.0:  # Acceptable range
                base_score += 5
            else:
                base_score -= 5
        
        return base_score
        
    def _calculate_weather_score(self, crop, weather_data):
        """Calculate weather suitability score"""
        if crop not in self.crop_suitability:
            return 0
            
        weather_score = 0
        crop_weather = self.crop_suitability[crop]['weather']
        
        # Temperature score
        if 'temperature' in weather_data:
            temp = weather_data['temperature']
            temp_req = crop_weather['temperature']
            if temp_req['min'] <= temp <= temp_req['max']:
                weather_score += 10
                if abs(temp - temp_req['optimal']) <= 3:
                    weather_score += 5
                    
        # Humidity score
        if 'humidity' in weather_data:
            humidity = weather_data['humidity']
            humid_req = crop_weather['humidity']
            if humid_req['min'] <= humidity <= humid_req['max']:
                weather_score += 8
                
        # Rainfall score
        if 'rainfall' in weather_data:
            rain = weather_data['rainfall']
            rain_req = crop_weather['rainfall']
            if rain > 0 and rain_req['min'] <= rain <= rain_req['max']:
                weather_score += 7
                
        return weather_score
        
    def get_feature_importance(self):
        """Get feature importance scores"""
        if not self.model:
            return None
            
        importance = self.model.feature_importances_
        return dict(zip(self.feature_names, importance))