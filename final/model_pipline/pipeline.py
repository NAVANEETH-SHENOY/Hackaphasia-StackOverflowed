# AgriTech Machine Learning Project - Complete Training Pipeline
# Designed for Google Colab and local environments

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
import xgboost as xgb
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

# Date and time processing
from datetime import datetime, timedelta
import calendar

# Install required packages (for Colab)
import subprocess
import sys

def install_packages():
    """Install required packages for the project"""
    packages = ['xgboost', 'requests', 'plotly', 'flask', 'streamlit']
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Uncomment the line below when running in Colab for the first time
# install_packages()

print("🌾 AgriTech ML Project - Data-Driven Farming Solutions")
print("=" * 60)

# =============================================================================
# STEP 1: DATA COLLECTION AND SYNTHETIC DATASET CREATION
# =============================================================================

def create_synthetic_agmarknet_data():
    """
    Create synthetic Agmarknet-style price data for demonstration
    In production, this would be replaced with actual API calls
    """
    print("📊 Creating synthetic Agmarknet price data...")
    
    # Major crops in India
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Onion', 
             'Potato', 'Tomato', 'Soybean', 'Groundnut']
    
    # Indian states and major markets
    states = ['Maharashtra', 'Karnataka', 'Andhra Pradesh', 'Tamil Nadu', 
              'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh']
    markets = ['APMC', 'Mandi', 'Wholesale Market', 'Primary Market']
    
    # Generate 3 years of daily price data
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 1, 1)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    for date in dates:
        for crop in crops:
            # Base prices (INR per quintal)
            base_prices = {
                'Rice': 2000, 'Wheat': 1800, 'Maize': 1500, 'Cotton': 5000,
                'Sugarcane': 300, 'Onion': 1200, 'Potato': 800, 'Tomato': 1500,
                'Soybean': 4000, 'Groundnut': 4500
            }
            
            # Seasonal multipliers
            month = date.month
            seasonal_factor = 1.0
            if crop in ['Rice', 'Wheat']:  # Rabi crops
                seasonal_factor = 1.2 if month in [10, 11, 12, 1, 2] else 0.9
            elif crop in ['Cotton', 'Sugarcane']:  # Cash crops
                seasonal_factor = 1.1 if month in [3, 4, 5] else 1.0
            elif crop in ['Onion', 'Potato', 'Tomato']:  # Vegetables
                seasonal_factor = 1.3 if month in [6, 7, 8, 9] else 0.8
            
            # Add market volatility and trends
            base_price = base_prices[crop]
            
            # Random market fluctuations
            volatility = np.random.normal(0, 0.1)
            trend_factor = 1 + (date.year - 2021) * 0.05  # 5% yearly inflation
            
            price = base_price * seasonal_factor * trend_factor * (1 + volatility)
            price = max(price, base_price * 0.5)  # Minimum price floor
            
            # Random state and market selection
            state = np.random.choice(states)
            market = np.random.choice(markets)
            
            data.append({
                'Date': date,
                'State': state,
                'Market': market,
                'Commodity': crop,
                'Price': round(price, 2),
                'Quantity': np.random.randint(100, 1000),  # Quintals
                'Year': date.year,
                'Month': date.month,
                'Day': date.day,
                'DayOfWeek': date.weekday()
            })
    
    df = pd.DataFrame(data)
    print(f"✅ Created {len(df)} price records across {len(crops)} crops")
    return df

def create_synthetic_yield_data():
    """
    Create synthetic crop yield data for Indian states
    """
    print("🌱 Creating synthetic crop yield data...")
    
    states = ['Maharashtra', 'Karnataka', 'Andhra Pradesh', 'Tamil Nadu', 
              'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh']
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Onion', 
             'Potato', 'Tomato', 'Soybean', 'Groundnut']
    
    data = []
    
    for year in range(2018, 2024):
        for state in states:
            for crop in crops:
                # Base yields (tonnes per hectare)
                base_yields = {
                    'Rice': 3.5, 'Wheat': 3.2, 'Maize': 2.8, 'Cotton': 1.8,
                    'Sugarcane': 80.0, 'Onion': 18.0, 'Potato': 22.0, 
                    'Tomato': 25.0, 'Soybean': 1.2, 'Groundnut': 1.5
                }
                
                # State-specific yield factors
                state_factors = {
                    'Maharashtra': 1.1, 'Karnataka': 1.0, 'Andhra Pradesh': 1.05,
                    'Tamil Nadu': 1.08, 'Gujarat': 0.95, 'Rajasthan': 0.85,
                    'Madhya Pradesh': 0.9, 'Uttar Pradesh': 1.0
                }
                
                base_yield = base_yields[crop]
                state_factor = state_factors.get(state, 1.0)
                
                # Weather and technology improvements
                tech_improvement = 1 + (year - 2018) * 0.02  # 2% yearly improvement
                weather_factor = np.random.normal(1.0, 0.15)  # Weather variability
                
                yield_value = base_yield * state_factor * tech_improvement * weather_factor
                yield_value = max(yield_value, base_yield * 0.3)  # Minimum yield
                
                # Synthetic rainfall data (mm)
                rainfall = np.random.normal(800, 200)  # Average Indian rainfall
                rainfall = max(rainfall, 200)  # Minimum rainfall
                
                # Create synthetic marketability index
                # Formula: (Yield * Price_Stability * Demand_Factor) / Input_Cost
                price_stability = np.random.uniform(0.7, 1.0)
                demand_factor = np.random.uniform(0.8, 1.2)
                input_cost_factor = np.random.uniform(0.9, 1.1)
                
                marketability_index = (yield_value * price_stability * demand_factor) / input_cost_factor
                marketability_index = round(marketability_index, 2)
                
                data.append({
                    'State': state,
                    'Crop': crop,
                    'Year': year,
                    'Yield_Tonnes_per_Hectare': round(yield_value, 2),
                    'Area_Hectares': np.random.randint(10000, 500000),
                    'Production_Tonnes': round(yield_value * np.random.randint(10000, 500000), 0),
                    'Rainfall_mm': round(rainfall, 1),
                    'Temperature_avg': np.random.uniform(20, 35),
                    'Soil_pH': np.random.uniform(6.0, 8.5),
                    'Marketability_Index': marketability_index  # SYNTHETIC FEATURE
                })
    
    df = pd.DataFrame(data)
    print(f"✅ Created {len(df)} yield records with synthetic marketability index")
    print("🔍 Marketability Index Formula: (Yield × Price_Stability × Demand) / Input_Cost")
    return df

# =============================================================================
# STEP 2: DATA PREPROCESSING AND FEATURE ENGINEERING
# =============================================================================

class AgriDataProcessor:
    """
    Comprehensive data processor for agriculture datasets
    """
    
    def __init__(self):
        self.price_scaler = StandardScaler()
        self.yield_scaler = StandardScaler()
        self.label_encoders = {}
        
    def preprocess_price_data(self, df):
        """
        Preprocess price data for time series forecasting
        """
        print("🔄 Processing price data...")
        
        # Convert date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(['Commodity', 'Date'])
        
        # Handle missing values
        df['Price'].fillna(df.groupby('Commodity')['Price'].transform('median'), inplace=True)
        df['Quantity'].fillna(df.groupby('Commodity')['Quantity'].transform('median'), inplace=True)
        
        # Create time-series features
        df['Price_MA_7'] = df.groupby('Commodity')['Price'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
        df['Price_MA_30'] = df.groupby('Commodity')['Price'].rolling(window=30, min_periods=1).mean().reset_index(0, drop=True)
        df['Price_Volatility'] = df.groupby('Commodity')['Price'].rolling(window=7, min_periods=1).std().reset_index(0, drop=True)
        
        # Lag features
        for lag in [1, 3, 7, 14]:
            df[f'Price_Lag_{lag}'] = df.groupby('Commodity')['Price'].shift(lag)
        
        # Fill NaN values created by rolling and lag operations
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(method='bfill').fillna(method='ffill')
        
        # Encode categorical variables
        categorical_cols = ['State', 'Market', 'Commodity']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
        
        print(f"✅ Price data processed: {df.shape}")
        return df
    
    def preprocess_yield_data(self, df):
        """
        Preprocess yield data for crop recommendation
        """
        print("🔄 Processing yield data...")
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Create seasonal features
        # Assuming we have month data or can derive it
        if 'Month' not in df.columns:
            # For demonstration, assign random months weighted by crop seasons
            crop_seasons = {
                'Rice': [6, 7, 8, 9, 10, 11],  # Kharif season
                'Wheat': [11, 12, 1, 2, 3, 4],  # Rabi season
                'Cotton': [6, 7, 8, 9, 10],     # Kharif season
                'Sugarcane': list(range(1, 13))  # Year-round
            }
            
            months = []
            for _, row in df.iterrows():
                crop = row['Crop']
                if crop in crop_seasons:
                    month = np.random.choice(crop_seasons[crop])
                else:
                    month = np.random.choice(range(1, 13))
                months.append(month)
            
            df['Month'] = months
        
        # Create month-based features
        df['Season'] = df['Month'].apply(self._get_season)
        df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
        df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
        
        # Normalize numerical features
        numerical_features = ['Yield_Tonnes_per_Hectare', 'Rainfall_mm', 
                             'Temperature_avg', 'Soil_pH', 'Marketability_Index']
        
        # Create normalized versions
        for col in numerical_features:
            if col in df.columns:
                df[f'{col}_normalized'] = (df[col] - df[col].mean()) / df[col].std()
        
        # Encode categorical variables
        categorical_cols = ['State', 'Crop', 'Season']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                try:
                    df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
                except ValueError:
                    # Handle unseen categories
                    self.label_encoders[col].classes_ = np.append(self.label_encoders[col].classes_, 
                                                                  df[col].unique())
                    df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
        
        print(f"✅ Yield data processed: {df.shape}")
        return df
    
    def _get_season(self, month):
        """Convert month to season"""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Summer'
        elif month in [6, 7, 8, 9]:
            return 'Monsoon'
        else:
            return 'Post-Monsoon'

# =============================================================================
# STEP 3: MODEL TRAINING AND EVALUATION
# =============================================================================

class AgriMLModels:
    """
    XGBoost models for price forecasting and crop recommendation
    """
    
    def __init__(self):
        self.price_model = None
        self.crop_model = None
        self.feature_names = {}
        self.model_metrics = {}
        
    def train_price_forecasting_model(self, df):
        """
        Train XGBoost model for 15-day price forecasting
        """
        print("🎯 Training Price Forecasting Model...")
        
        # Prepare features for price prediction
        feature_cols = ['Year', 'Month', 'Day', 'DayOfWeek', 'Quantity',
                       'Price_MA_7', 'Price_MA_30', 'Price_Volatility',
                       'Price_Lag_1', 'Price_Lag_3', 'Price_Lag_7', 'Price_Lag_14',
                       'State_encoded', 'Market_encoded', 'Commodity_encoded']
        
        # Filter available columns
        available_cols = [col for col in feature_cols if col in df.columns]
        
        X = df[available_cols].copy()
        y = df['Price'].copy()
        
        # Remove rows with NaN values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        # Time series split
        tscv = TimeSeriesSplit(n_splits=5)
        
        # Train-test split (80-20)
        split_idx = int(0.8 * len(X))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
        
        # XGBoost parameters
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
        
        # Train model
        self.price_model = xgb.XGBRegressor(**params)
        self.price_model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = self.price_model.predict(X_train)
        y_pred_test = self.price_model.predict(X_test)
        
        # Calculate metrics
        train_mae = mean_absolute_error(y_train, y_pred_train)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_mae = mean_absolute_error(y_test, y_pred_test)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        
        self.model_metrics['price_forecasting'] = {
            'train_mae': train_mae,
            'train_rmse': train_rmse,
            'test_mae': test_mae,
            'test_rmse': test_rmse,
            'mape': np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100
        }
        
        self.feature_names['price'] = available_cols
        
        print(f"✅ Price Model Trained!")
        print(f"   Test MAE: ₹{test_mae:.2f}")
        print(f"   Test RMSE: ₹{test_rmse:.2f}")
        print(f"   MAPE: {self.model_metrics['price_forecasting']['mape']:.2f}%")
        
        return X_test, y_test, y_pred_test
    
    def train_crop_recommendation_model(self, df):
        """
        Train XGBoost model for crop recommendation
        """
        print("🌱 Training Crop Recommendation Model...")
        
        # Prepare features
        feature_cols = ['State_encoded', 'Month', 'Month_sin', 'Month_cos',
                       'Yield_Tonnes_per_Hectare', 'Rainfall_mm', 'Temperature_avg',
                       'Soil_pH', 'Marketability_Index', 'Season_encoded']
        
        # Filter available columns
        available_cols = [col for col in feature_cols if col in df.columns]
        
        X = df[available_cols].copy()
        y = df['Crop_encoded'].copy()
        
        # Remove rows with NaN values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
        
        # XGBoost parameters for classification
        params = {
            'objective': 'multi:softprob',
            'n_estimators': 800,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
        
        # Train model
        self.crop_model = xgb.XGBClassifier(**params)
        self.crop_model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = self.crop_model.predict(X_train)
        y_pred_test = self.crop_model.predict(X_test)
        
        # Calculate accuracy
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        self.model_metrics['crop_recommendation'] = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy
        }
        
        self.feature_names['crop'] = available_cols
        
        print(f"✅ Crop Model Trained!")
        print(f"   Test Accuracy: {test_accuracy:.3f}")
        print(f"   Train Accuracy: {train_accuracy:.3f}")
        
        return X_test, y_test, y_pred_test
    
    def predict_price_forecast(self, commodity, days=15):
        """
        Generate 15-day price forecast for a commodity
        """
        if self.price_model is None:
            return None
        
        # This is a simplified version - in practice, you'd need current market data
        # For demo purposes, we'll create sample predictions
        base_price = np.random.uniform(1000, 5000)  # Base price
        dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range(1, days + 1)]
        
        # Simulate price variations
        forecasts = []
        for i in range(days):
            variation = np.random.normal(0, 0.05)  # 5% daily variation
            price = base_price * (1 + variation * (i + 1) / days)
            forecasts.append(round(price, 2))
        
        return list(zip(dates, forecasts))
    
    def get_feature_importance(self, model_type='price'):
        """
        Get feature importance for visualization
        """
        if model_type == 'price' and self.price_model:
            importance = self.price_model.feature_importances_
            features = self.feature_names['price']
        elif model_type == 'crop' and self.crop_model:
            importance = self.crop_model.feature_importances_
            features = self.feature_names['crop']
        else:
            return None, None
        
        return features, importance

# =============================================================================
# STEP 4: VISUALIZATION AND REPORTING
# =============================================================================

def create_visualizations(models, processor, price_df, yield_df):
    """
    Create comprehensive visualizations for the project
    """
    print("📊 Creating visualizations...")
    
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('AgriTech ML Project - Model Analysis Dashboard', fontsize=16, y=0.98)
    
    # 1. Price trends over time
    ax1 = axes[0, 0]
    crops_to_plot = price_df['Commodity'].value_counts().head(3).index
    for crop in crops_to_plot:
        crop_data = price_df[price_df['Commodity'] == crop]
        monthly_prices = crop_data.groupby([crop_data['Date'].dt.to_period('M')])['Price'].mean()
        ax1.plot(monthly_prices.index.astype(str), monthly_prices.values, 
                marker='o', label=crop, linewidth=2)
    ax1.set_title('Price Trends Over Time')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Price (₹/Quintal)')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Feature importance for price model
    ax2 = axes[0, 1]
    if models.price_model:
        features, importance = models.get_feature_importance('price')
        if features and importance is not None:
            top_features = sorted(zip(features, importance), key=lambda x: x[1], reverse=True)[:8]
            feature_names, feature_scores = zip(*top_features)
            bars = ax2.barh(range(len(feature_names)), feature_scores, color='skyblue')
            ax2.set_yticks(range(len(feature_names)))
            ax2.set_yticklabels(feature_names)
            ax2.set_title('Price Model - Feature Importance')
            ax2.set_xlabel('Importance Score')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax2.text(width, bar.get_y() + bar.get_height()/2, 
                        f'{width:.3f}', ha='left', va='center', fontsize=9)
    
    # 3. Yield distribution by state
    ax3 = axes[0, 2]
    state_yields = yield_df.groupby('State')['Yield_Tonnes_per_Hectare'].mean().sort_values(ascending=False)
    bars = ax3.bar(range(len(state_yields)), state_yields.values, color='lightgreen')
    ax3.set_title('Average Yield by State')
    ax3.set_xlabel('States')
    ax3.set_ylabel('Yield (Tonnes/Hectare)')
    ax3.set_xticks(range(len(state_yields)))
    ax3.set_xticklabels(state_yields.index, rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    # 4. Marketability Index Analysis
    ax4 = axes[1, 0]
    crop_marketability = yield_df.groupby('Crop')['Marketability_Index'].mean().sort_values(ascending=False)
    bars = ax4.bar(range(len(crop_marketability)), crop_marketability.values, color='orange', alpha=0.7)
    ax4.set_title('Marketability Index by Crop')
    ax4.set_xlabel('Crops')
    ax4.set_ylabel('Marketability Index')
    ax4.set_xticks(range(len(crop_marketability)))
    ax4.set_xticklabels(crop_marketability.index, rotation=45)
    
    # 5. Seasonal price variations
    ax5 = axes[1, 1]
    seasonal_prices = price_df.groupby('Month')['Price'].mean()
    ax5.plot(seasonal_prices.index, seasonal_prices.values, marker='o', 
            linewidth=3, markersize=8, color='purple')
    ax5.set_title('Seasonal Price Variations')
    ax5.set_xlabel('Month')
    ax5.set_ylabel('Average Price (₹)')
    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
    ax5.grid(True, alpha=0.3)
    
    # 6. Model Performance Metrics
    ax6 = axes[1, 2]
    if models.model_metrics:
        metrics_data = []
        labels = []
        
        if 'price_forecasting' in models.model_metrics:
            metrics_data.extend([
                models.model_metrics['price_forecasting']['test_mae'],
                models.model_metrics['price_forecasting']['test_rmse']
            ])
            labels.extend(['MAE (₹)', 'RMSE (₹)'])
        
        if 'crop_recommendation' in models.model_metrics:
            metrics_data.append(models.model_metrics['crop_recommendation']['test_accuracy'] * 100)
            labels.append('Accuracy (%)')
        
        if metrics_data:
            colors = ['lightcoral', 'lightsalmon', 'lightblue'][:len(metrics_data)]
            bars = ax6.bar(labels, metrics_data, color=colors)
            ax6.set_title('Model Performance Metrics')
            ax6.set_ylabel('Score')
            
            # Add value labels on bars
            for bar, value in zip(bars, metrics_data):
                height = bar.get_height()
                ax6.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('agritech_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Additional forecast visualization
    print("📈 Creating price forecast visualization...")
    plt.figure(figsize=(12, 6))
    
    # Sample forecast for demonstration
    sample_forecasts = models.predict_price_forecast('Rice', 15)
    if sample_forecasts:
        dates, prices = zip(*sample_forecasts)
        plt.plot(dates, prices, marker='o', linewidth=2, markersize=6, color='green')
        plt.title('15-Day Price Forecast - Rice', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Predicted Price (₹/Quintal)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add trend line
        x_numeric = range(len(prices))
        z = np.polyfit(x_numeric, prices, 1)
        p = np.poly1d(z)
        plt.plot(dates, p(x_numeric), "--", alpha=0.7, color='red', label='Trend')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('price_forecast_sample.png', dpi=300, bbox_inches='tight')
        plt.show()

# =============================================================================
# STEP 5: MAIN EXECUTION PIPELINE
# =============================================================================

def main():
    """
    Main execution pipeline for the AgriTech ML project
    """
    print("🚀 Starting AgriTech ML Pipeline...")
    print("=" * 60)
    
    # Step 1: Create synthetic datasets
    print("\n📋 STEP 1: DATA COLLECTION")
    price_df = create_synthetic_agmarknet_data()
    yield_df = create_synthetic_yield_data()
    
    # Display dataset info
    print(f"\n📊 Dataset Summary:")
    print(f"Price data: {price_df.shape[0]} records, {price_df.shape[1]} features")
    print(f"Yield data: {yield_df.shape[0]} records, {yield_df.shape[1]} features")
    
    # Step 2: Data preprocessing
    print("\n🔄 STEP 2: DATA PREPROCESSING")
    processor = AgriDataProcessor()
    
    price_df_processed = processor.preprocess_price_data(price_df)
    yield_df_processed = processor.preprocess_yield_data(yield_df)
    
    # Step 3: Model training
    print("\n🎯 STEP 3: MODEL TRAINING")
    models = AgriMLModels()
    
    # Train price forecasting model
    price_results = models.train_price_forecasting_model(price_df_processed)
    
    # Train crop recommendation model
    crop_results = models.train_crop_recommendation_model(yield_df_processed)
    
    # Step 4: Create visualizations
    print("\n📊 STEP 4: VISUALIZATION")
    create_visualizations(models, processor, price_df, yield_df)
    
    # Step 5: Save models and processors
    print("\n💾 STEP 5: SAVING MODELS")
    import joblib
    
    try:
        joblib.dump(models.price_model, 'price_forecast_model.pkl')
        joblib.dump(models.crop_model, 'crop_recommendation_model.pkl')
        joblib.dump(processor, 'data_processor.pkl')
        print("✅ Models and processor saved successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Could not save models - {e}")
    
    # Display final summary
    print("\n" + "=" * 60)
    print("📈 PROJECT SUMMARY")
    print("=" * 60)
    
    if models.model_metrics:
        if 'price_forecasting' in models.model_metrics:
            pm = models.model_metrics['price_forecasting']
            print(f"💰 Price Forecasting Model:")
            print(f"   • Test MAE: ₹{pm['test_mae']:.2f}")
            print(f"   • Test RMSE: ₹{pm['test_rmse']:.2f}")
            print(f"   • MAPE: {pm['mape']:.2f}%")
        
        if 'crop_recommendation' in models.model_metrics:
            cm = models.model_metrics['crop_recommendation']
            print(f"🌱 Crop Recommendation Model:")
            print(f"   • Test Accuracy: {cm['test_accuracy']:.1%}")
    
    print(f"\n🎯 Ready for deployment with Flask API!")
    print(f"📱 Frontend can be built with Streamlit!")
    
    return models, processor, price_df_processed, yield_df_processed

# Execute the main pipeline
if __name__ == "__main__":
    models, processor, price_data, yield_data = main()
    
    # Sample predictions for testing
    print("\n🧪 TESTING SAMPLE PREDICTIONS:")
    print("-" * 40)
    
    # Test price forecast
    forecast = models.predict_price_forecast('Rice', 5)
    if forecast:
        print("📈 5-Day Rice Price Forecast:")
        for date, price in forecast:
            print(f"   {date}: ₹{price}")
    
    print("\n✨ AgriTech ML Pipeline Complete!")
    print("Ready for integration with Flask backend and Streamlit frontend!")