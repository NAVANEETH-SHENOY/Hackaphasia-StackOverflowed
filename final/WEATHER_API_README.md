# 🌤️ AgriTech Weather API Integration

## Overview
This integration adds real-time weather data capabilities to the AgriTech ML project using the OpenWeatherMap API. The weather data enhances crop recommendations and price forecasting with current weather conditions, improving the accuracy of agricultural predictions.

## 🚀 Features

### ✅ **Current Weather Data**
- Temperature (current and feels-like)
- Humidity percentage
- Atmospheric pressure
- Weather description
- Real-time conditions

### ✅ **5-Day Weather Forecast**
- Daily temperature predictions
- Humidity forecasts
- Rainfall predictions (when available)
- Weather condition descriptions

### ✅ **Comprehensive District Coverage**
- 100+ Indian agricultural districts
- Automatic coordinate mapping
- Fallback to Bangalore coordinates for unknown districts

### ✅ **Robust Error Handling**
- Graceful fallback when API is unavailable
- Random but realistic weather data generation
- Comprehensive logging and error reporting

## 📋 Setup Instructions

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Environment Configuration**
Create a `.env` file in the project root:
```env
# Agro API Key for weather data
# Get your free API key from: https://agromonitoring.com/
AGRO_API_KEY=your_agro_api_key_here
```

### 3. **Get Agro API Key**
1. Visit [agromonitoring.com](https://agromonitoring.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

### 4. **Run the API Server**
```bash
python backend/backend.py
```

## 🔌 API Endpoints

### **GET /get-weather**
Get current weather and 5-day forecast for a district.

**Query Parameters:**
- `district` (required): District name (e.g., "Bangalore", "Mumbai")

**Example Request:**
```bash
curl "http://localhost:5000/get-weather?district=Bangalore"
```

**Example Response:**
```json
{
  "district": "Bangalore",
  "coordinates": {
    "lat": 12.9716,
    "lon": 77.5946
  },
  "current": {
    "temperature": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "feels_like": 30.2,
    "description": "partly cloudy"
  },
  "forecast": [
    {
      "date": "2024-01-15",
      "temperature": 29.1,
      "humidity": 62,
      "description": "clear sky",
      "rainfall": 0.0
    },
    {
      "date": "2024-01-16",
      "temperature": 27.8,
      "humidity": 68,
      "description": "light rain",
      "rainfall": 2.5
    }
  ],
  "source": "agro_api",
  "timestamp": "2024-01-14T10:30:00"
}
```

## 🧪 Testing

### **Run Test Suite**
```bash
python test_weather_api.py
```

### **Manual Testing**
```bash
# Test specific district
curl "http://localhost:5000/get-weather?district=Mumbai"

# Test API health
curl "http://localhost:5000/health"
```

## 📊 Supported Districts

The API supports 100+ Indian agricultural districts including:

### **Major Cities**
- Bangalore, Mumbai, Delhi, Chennai, Kolkata
- Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow

### **Agricultural Hubs**
- Ludhiana, Amritsar, Chandigarh
- Coimbatore, Mysore, Salem
- Nashik, Aurangabad, Kolhapur
- And many more...

### **Adding New Districts**
To add a new district, update the `_init_district_mapping()` method in `backend/backend.py`:

```python
"NewDistrict": (latitude, longitude)
```

## 🔧 Configuration

### **API Settings**
- **Timeout**: 10 seconds for API calls
- **Forecast Days**: 5 days
- **Fallback**: Enabled when API is unavailable

### **Error Handling**
- **API Key Missing**: Uses fallback data
- **District Not Found**: Falls back to Bangalore coordinates
- **API Unavailable**: Generates realistic random data
- **Network Issues**: Graceful degradation

## 🌐 Integration with Frontend

The weather data can be integrated into the Streamlit frontend:

```python
# In frontend.py
def get_weather_data(district):
    response = requests.get(f"{API_BASE_URL}/get-weather?district={district}")
    return response.json() if response.status_code == 200 else None
```

## 📈 Use Cases

### **1. Enhanced Crop Recommendations**
- Weather-based crop suitability
- Seasonal planting recommendations
- Risk assessment for weather-sensitive crops

### **2. Price Forecasting**
- Weather impact on crop prices
- Supply chain disruption predictions
- Market volatility analysis

### **3. Farm Management**
- Irrigation planning
- Pest and disease risk assessment
- Harvest timing optimization

## 🚨 Troubleshooting

### **Common Issues**

1. **API Key Not Working**
   - Verify key is correct in `.env` file
   - Check API key permissions on agromonitoring.com
   - Ensure no extra spaces in the key

2. **District Not Found**
   - Check spelling and case sensitivity
   - Add district to mapping if needed
   - API will fallback to Bangalore coordinates

3. **API Timeout**
   - Check internet connection
   - Verify agromonitoring.com is accessible
   - API will use fallback data

4. **Server Not Starting**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)
   - Verify port 5000 is available

### **Debug Mode**
Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📝 API Limits

### **Agro API Limits**
- Free tier: 1000 calls/day
- Rate limit: 60 calls/minute
- Data retention: 5 days

### **Fallback Data**
- Generated when API limits exceeded
- Realistic random weather patterns
- Maintains API response structure

## 🔮 Future Enhancements

- [ ] Historical weather data integration
- [ ] Weather alerts and notifications
- [ ] Integration with soil moisture data
- [ ] Advanced weather analytics
- [ ] Multi-language support for districts

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs for error messages
3. Test with the provided test script
4. Verify Agro API status

---

**Built with ❤️ for Indian farmers** | **AgriTech Weather Integration v1.0**
