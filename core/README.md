# Karnataka Crop Demand Forecasting Platform

A comprehensive AI-powered platform designed to help Karnataka farmers make informed decisions about crop cultivation, market timing, and profitability analysis.

## 🌾 Overview

This platform provides three core functionalities:

### Part A – Dataset Discovery
- **Crop Calendar Data**: Sowing and harvest windows for major crops
- **Market Price Data**: Historical mandi prices and arrival quantities from Agmarknet
- **Weather Data**: Rainfall, temperature, humidity by district and season
- **Soil & Yield Data**: District-level agricultural statistics
- **Cost Data**: Cultivation costs per crop and district

### Part B – Farmer Recommendations
When given farmer inputs (district + month):
1. **Top 3 Crop Recommendations** with Kannada translations
2. **Growth Duration** (sowing → harvest timeline)
3. **Optimal Harvest & Selling Windows**
4. **Expected Price Ranges** in nearby mandis
5. **Profitability Analysis** (revenue - cost calculations)
6. **Risk Assessment** (oversupply, pests, weather risks)
7. **Alternative Crops** if risk is high
8. **Farmer-friendly Language** (Kannada + English mix)

### Part C – Data Gap Filling (Synthetic Data Generation)
- **Automatic Gap Filling**: Generates realistic data for missing information
- **Research-Based**: Uses ICRISAT, FAO, and government research patterns
- **Transparent Labeling**: All synthetic data clearly marked as "AI-Generated"
- **Plausible Values**: Ensures realistic agricultural parameters

## 🚀 Features

- **District-Level Analysis**: Covers all 30 districts of Karnataka
- **Season-Aware**: Kharif, Rabi, and Summer season recommendations
- **Multi-Language Support**: English and Kannada interface
- **Real-Time Data**: Integrates with government APIs where available
- **AI-Powered**: Uses machine learning for predictions and gap filling
- **Mobile-Friendly**: Responsive design for smartphone access

## 📊 Available Datasets

| Dataset | Source | Coverage | Quality |
|---------|--------|----------|---------|
| Crop Calendar | Agricultural Research | All districts | High |
| Market Prices | Agmarknet + Synthetic | Major mandis | Medium |
| Weather Data | IMD + KSNDMC | All districts | High |
| Cost Data | Government Reports | State level | Medium |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd karnataka-crop-forecasting
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the platform**
Open your browser and navigate to `http://localhost:5000`

## 📱 Usage

### Getting Crop Recommendations

1. **Select District**: Choose from 30 Karnataka districts
2. **Select Month**: Pick the month for cultivation planning
3. **Get Recommendations**: Receive top 3 crop suggestions with:
   - Kannada crop names
   - Sowing and harvest windows
   - Expected yields and prices
   - Profitability analysis
   - Risk assessment
   - Alternative options

### Example Output

**Input**: District = Mandya, Month = September

**Recommendations**:
1. **Paddy (ಅಕ್ಕಿ/ನರಿ)** - Kharif season
   - Sowing: Jun, Jul, Aug
   - Harvest: Oct, Nov, Dec
   - Duration: 120 days
   - Expected Profit: ₹10,000/acre

2. **Ragi (ರಾಗಿ)** - Kharif season
   - Sowing: Jun, Jul, Aug
   - Harvest: Oct, Nov, Dec
   - Duration: 110 days
   - Expected Profit: ₹15,750/acre

3. **Maize (ಮಕ್ಕಾ)** - Kharif season
   - Sowing: Jun, Jul
   - Harvest: Sep, Oct
   - Duration: 90 days
   - Expected Profit: ₹13,000/acre

## 🔧 API Endpoints

### GET /api/datasets
Returns summary of available datasets and synthetic data usage.

### POST /api/recommendations
```json
{
  "district": "Mandya",
  "month": 9
}
```
Returns crop recommendations for the specified district and month.

### POST /api/synthetic-data
```json
{
  "district": "Mandya",
  "crop": "Paddy",
  "data_type": "prices"
}
```
Generates synthetic data for missing information.

### GET /api/districts
Returns list of Karnataka districts.

### GET /api/crops
Returns list of major crops.

## 🌱 Supported Crops

### Cereals
- Paddy (Rice) - ಅಕ್ಕಿ/ನರಿ
- Maize - ಮಕ್ಕಾ
- Ragi (Finger Millet) - ರಾಗಿ
- Jowar (Sorghum) - ಜೋಳ
- Bajra (Pearl Millet) - ಸಜ್ಜೆ
- Wheat - ಗೋಧಿ

### Pulses
- Tur (Pigeon Pea) - ತೊಗರಿ
- Chickpea - ಕಡಲೆ
- Green Gram - ಹೆಸರು
- Black Gram - ಉದ್ದು
- Soybean - ಸೋಯಾಬೀನ್

### Oilseeds
- Groundnut - ಶೇಂಗಾ
- Sunflower - ಸೂರ್ಯಕಾಂತಿ
- Sesame - ಎಳ್ಳು

### Commercial Crops
- Cotton - ಹತ್ತಿ
- Sugarcane - ಕಬ್ಬು

### Vegetables
- Onion - ಈರುಳ್ಳಿ
- Tomato - ಟೊಮೇಟೊ
- Potato - ಆಲೂಗಡ್ಡೆ
- Cabbage - ಎಲೆಕೋಸು
- Cauliflower - ಹೂವೆಲೆಕೋಸು
- Brinjal - ಬದನೆಕಾಯಿ
- Chilli - ಮೆಣಸಿನಕಾಯಿ

## 🗺️ Karnataka Districts Covered

1. Bagalkot
2. Ballari
3. Belagavi
4. Bengaluru Rural
5. Bengaluru Urban
6. Bidar
7. Chamarajanagara
8. Chikballapur
9. Chikkamagaluru
10. Chitradurga
11. Dakshina Kannada
12. Davanagere
13. Dharwad
14. Gadag
15. Hassan
16. Haveri
17. Kalaburagi
18. Kodagu
19. Kolar
20. Koppal
21. Mandya
22. Mysuru
23. Raichur
24. Ramanagara
25. Shivamogga
26. Tumakuru
27. Udupi
28. Uttara Kannada
29. Vijayapura
30. Yadgir

## 🔬 Data Sources

### Real Data Sources
- **Agmarknet**: Market prices and arrival quantities
- **IMD**: Weather data (rainfall, temperature, humidity)
- **KSNDMC**: Karnataka State Natural Disaster Monitoring Centre
- **Government Reports**: Cost of cultivation and yield data
- **Agricultural Research**: Crop calendars and best practices

### Synthetic Data Generation
When real data is missing or incomplete, the platform generates synthetic data based on:
- Similar districts with comparable climate/soil conditions
- Published agricultural research (ICRISAT, FAO, Government reports)
- Historical averages and trends
- Machine learning patterns from available data

All synthetic data is clearly labeled as **"AI-Generated (based on real patterns)"** for transparency.

## 🎯 Key Features

### Smart Recommendations
- **Season-Aware**: Considers Kharif, Rabi, and Summer seasons
- **District-Specific**: Tailored to local climate and soil conditions
- **Profitability-Focused**: Prioritizes crops with better profit potential
- **Risk-Aware**: Identifies and suggests alternatives for high-risk crops

### User-Friendly Interface
- **Bilingual Support**: English and Kannada language options
- **Mobile Responsive**: Works on smartphones and tablets
- **Visual Analytics**: Charts and graphs for better understanding
- **Simple Navigation**: Easy-to-use interface for farmers

### Data Quality Assurance
- **Transparent Sources**: Clear indication of data sources
- **Quality Metrics**: Assessment of data reliability
- **Gap Identification**: Automatic detection of missing data
- **Synthetic Data Labeling**: Clear marking of AI-generated content

## 🔮 Future Enhancements

- **Real-Time Weather Integration**: Live weather data from IMD
- **Market Price APIs**: Direct integration with Agmarknet
- **Mobile App**: Native Android/iOS applications
- **SMS Alerts**: Price and weather notifications
- **Farmer Community**: Social features for knowledge sharing
- **IoT Integration**: Sensor data from farms
- **Blockchain**: Transparent supply chain tracking

## 🤝 Contributing

We welcome contributions from:
- Agricultural researchers
- Data scientists
- Software developers
- Farmers and agricultural experts
- Government agencies

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- **Email**: support@karnataka-crop-forecasting.com
- **Phone**: +91-80-XXXX-XXXX
- **Website**: https://karnataka-crop-forecasting.com

## 🙏 Acknowledgments

- **Karnataka State Government** for agricultural data
- **IMD** for weather data
- **Agmarknet** for market price data
- **ICRISAT** for agricultural research
- **FAO** for global agricultural patterns
- **Local Farmers** for feedback and validation

---

**Built with ❤️ for Karnataka Farmers**

*Empowering farmers with data-driven decisions for sustainable agriculture*
