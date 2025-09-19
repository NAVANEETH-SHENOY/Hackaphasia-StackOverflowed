"""
Price Forecasting Model Module
Uses XGBoost and Prophet for accurate 15-day price predictions
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from prophet import Prophet
import logging

logger = logging.getLogger(__name__)

class PriceForecastModel:
    """Price forecasting model combining XGBoost and Prophet"""
    
    def __init__(self):
        self.xgb_model = None
        self.prophet_model = None
        self.feature_names = []
        self.scaler = StandardScaler()
        
    def prepare_features(self, df):
        """Prepare features for price prediction"""
        feature_cols = [
            'Year', 'Month', 'Day', 'DayOfWeek', 'Quantity',
            'Price_MA_7', 'Price_MA_30', 'Price_Volatility',
            'Price_Lag_1', 'Price_Lag_3', 'Price_Lag_7',
            'State_encoded', 'Market_encoded', 'Commodity_encoded'
        ]
        
        # Filter available columns
        self.feature_names = [col for col in feature_cols if col in df.columns]
        return df[self.feature_names].copy()
        
    def train(self, df):
        """Train both XGBoost and Prophet models"""
        logger.info("Training price forecasting models...")
        
        X = self.prepare_features(df)
        y = df['Price'].copy()
        
        # Remove NaN values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        # Train-test split (80-20)
        split_idx = int(0.8 * len(X))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # Train XGBoost
        self.xgb_model = self._train_xgboost(X_train, y_train)
        
        # Train Prophet (using date and price only)
        prophet_df = df[['Date', 'Price']].rename(columns={'Date': 'ds', 'Price': 'y'})
        self.prophet_model = self._train_prophet(prophet_df)
        
        # Calculate metrics
        metrics = self._calculate_metrics(X_test, y_test)
        
        return metrics
        
    def _train_xgboost(self, X_train, y_train):
        """Train XGBoost model with optimized parameters"""
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
        
        model = XGBRegressor(**params)
        model.fit(X_train, y_train)
        return model
        
    def _train_prophet(self, df):
        """Train Prophet model with custom parameters"""
        model = Prophet(
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0,
            seasonality_mode='multiplicative',
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True
        )
        model.fit(df)
        return model
        
    def predict(self, input_data, days=15):
        """
        Generate ensemble forecast combining XGBoost and Prophet predictions
        """
        try:
            # XGBoost prediction for current conditions
            xgb_features = self.prepare_features(input_data)
            xgb_pred = self.xgb_model.predict(xgb_features)
            
            # Prophet prediction for trend and seasonality
            prophet_df = pd.DataFrame({'ds': pd.date_range(start=input_data['Date'].iloc[-1], periods=days+1)})
            prophet_forecast = self.prophet_model.predict(prophet_df)
            prophet_pred = prophet_forecast['yhat'].values[1:]  # Skip current day
            
            # Combine predictions (60% XGBoost, 40% Prophet)
            base_price = xgb_pred[-1]  # Use last known price as base
            combined_forecast = []
            
            for i in range(days):
                # XGBoost contribution
                xgb_factor = 0.6 * (xgb_pred[-1] / base_price)
                
                # Prophet contribution
                prophet_factor = 0.4 * (prophet_pred[i] / prophet_pred[0])
                
                # Combined prediction with uncertainty factor
                uncertainty = np.random.normal(0, 0.02)  # 2% random variation
                predicted_price = base_price * (xgb_factor + prophet_factor) * (1 + uncertainty)
                
                # Ensure reasonable bounds (±30% from base price)
                predicted_price = max(base_price * 0.7, min(base_price * 1.3, predicted_price))
                
                combined_forecast.append({
                    'date': (pd.Timestamp.now() + pd.Timedelta(days=i+1)).strftime('%Y-%m-%d'),
                    'price': round(predicted_price, 2)
                })
            
            return combined_forecast
            
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return None
            
    def _calculate_metrics(self, X_test, y_test):
        """Calculate model performance metrics"""
        y_pred = self.xgb_model.predict(X_test)
        
        return {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        }
        
    def get_feature_importance(self):
        """Get XGBoost feature importance"""
        if not self.xgb_model:
            return None
            
        importance = self.xgb_model.feature_importances_
        return dict(zip(self.feature_names, importance))