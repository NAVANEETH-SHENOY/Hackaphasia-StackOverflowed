# AgriTech Backend

AI-powered crop price forecasting and recommendation system backend API.

## Features

- 🌾 **Crop Price Forecasting**: 15-day price predictions using ML models
- 🌱 **Smart Crop Recommendations**: Location and season-based crop suggestions
- 📊 **Market Analytics**: Comprehensive market insights
- 🚀 **RESTful API**: Clean, well-documented endpoints
- 🔧 **Easy Deployment**: Simple setup and configuration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Price forecast
curl -X POST http://localhost:5000/forecast-price \
  -H "Content-Type: application/json" \
  -d '{"crop": "Rice", "days": 15}'

# Crop recommendations
curl -X POST http://localhost:5000/recommend-crop \
  -H "Content-Type: application/json" \
  -d '{"state": "Maharashtra", "month": 6}'
```

## API Endpoints

### Health Check
- **GET** `/health` - Check API status

### Price Forecasting
- **POST** `/forecast-price` - Get crop price predictions
  ```json
  {
    "crop": "Rice",
    "days": 15
  }
  ```

### Crop Recommendations
- **POST** `/recommend-crop` - Get crop recommendations
  ```json
  {
    "state": "Maharashtra",
    "month": 6,
    "district": "Pune"
  }
  ```

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export PORT=5000
```

## Model Files

The backend directory contains all trained model files:
- `price_forecast_model.pkl` - XGBoost price forecasting model
- `crop_recommendation_model.pkl` - XGBoost crop recommendation model
- `data_processor.pkl` - Data preprocessing pipeline
- `agritech_analysis_dashboard.png` - Generated analysis dashboard
- `price_forecast_sample.png` - Sample forecast visualization

If model files are not found, the API will use simplified prediction functions for demonstration.

## Development

### Running Tests

```bash
pytest
```

### Code Structure

```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── models/            # Trained model files (optional)
    ├── price_forecast_model.pkl
    ├── crop_recommendation_model.pkl
    └── data_processor.pkl
```

## Support

For issues and questions, please check the main project documentation.
