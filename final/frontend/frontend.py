# AgriTech Streamlit Frontend
# Modern, farmer-friendly interface for crop price forecasting and recommendations

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import numpy as np

# Configure Streamlit page
st.set_page_config(
    page_title="AgriTech - Smart Farming Solutions",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# STYLING AND CONFIGURATION
# =============================================================================

# Custom CSS for modern, non-green design
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Header styling */
    .header {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        color: #333;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Metric styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Success message styling */
    .success-msg {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
    }
    
    /* Warning message styling */
    .warning-msg {
        background: linear-gradient(45deg, #f7931e, #ffb347);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
    }
    
    /* Hide Streamlit default styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

class AgriTechFrontend:
    """
    Frontend controller for AgriTech Streamlit app
    """
    
    def __init__(self):
        self.api_base_url = "http://localhost:5000"
        self.crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 
                     'Onion', 'Potato', 'Tomato', 'Soybean', 'Groundnut']
        self.states = ['Maharashtra', 'Karnataka', 'Andhra Pradesh', 'Tamil Nadu',
                      'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh']
    
    def call_api(self, endpoint, data):
        """
        Make API call to backend
        """
        try:
            response = requests.post(f"{self.api_base_url}/{endpoint}", 
                                   json=data, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def create_price_chart(self, predictions):
        """
        Create interactive price forecast chart
        """
        df = pd.DataFrame(predictions)
        df['date'] = pd.to_datetime(df['date'])
        
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['price'],
            mode='lines+markers',
            name='Predicted Price',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2'),
            hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> ₹%{y:.2f}<extra></extra>'
        ))
        
        # Add trend line
        x_numeric = np.arange(len(df))
        z = np.polyfit(x_numeric, df['price'], 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=p(x_numeric),
            mode='lines',
            name='Trend',
            line=dict(color='#ff6b6b', width=2, dash='dash'),
            hovertemplate='<b>Trend:</b> ₹%{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Price Forecast",
            xaxis_title="Date",
            yaxis_title="Price (₹/Quintal)",
            template="plotly_white",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_recommendations_chart(self, recommendations):
        """
        Create crop recommendations visualization
        """
        df = pd.DataFrame(recommendations)
        
        fig = px.bar(
            df, 
            x='suitability_score', 
            y='crop',
            orientation='h',
            color='suitability_score',
            color_continuous_scale='Viridis',
            title="Crop Suitability Scores"
        )
        
        fig.update_layout(
            xaxis_title="Suitability Score",
            yaxis_title="Crops",
            template="plotly_white",
            height=400
        )
        
        return fig

# Initialize frontend controller
frontend = AgriTechFrontend()

# =============================================================================
# MAIN INTERFACE
# =============================================================================

# Header
st.markdown("""
<div class="header">
    <h1>🌾 AgriTech - Smart Farming Solutions</h1>
    <p style="font-size: 1.2em; margin-top: 1rem; opacity: 0.9;">
        Empowering farmers with AI-driven crop price forecasts and intelligent recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Navigation")
app_mode = st.sidebar.selectbox(
    "Choose Application Mode",
    ["📈 Price Forecasting", "🌱 Crop Recommendations", "📊 Market Analytics", "ℹ️ About"]
)

# =============================================================================
# PRICE FORECASTING MODULE
# =============================================================================

if app_mode == "📈 Price Forecasting":
    st.markdown("## 📈 Crop Price Forecasting")
    st.markdown("Get AI-powered price predictions for the next 15 days to optimize your selling strategy.")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Forecast Parameters")
        
        # Input controls
        selected_crop = st.selectbox(
            "Select Crop",
            frontend.crops,
            help="Choose the crop for price forecasting"
        )
        
        forecast_days = st.slider(
            "Forecast Period (days)",
            min_value=5,
            max_value=30,
            value=15,
            step=1,
            help="Number of days to forecast"
        )
        
        # Predict button
        if st.button("🔮 Generate Forecast", use_container_width=True):
            with st.spinner("Generating price forecast..."):
                # Call API
                api_data = {
                    "crop": selected_crop,
                    "days": forecast_days
                }
                
                result = frontend.call_api("forecast-price", api_data)
                
                if "error" not in result:
                    # Store result in session state
                    st.session_state['forecast_result'] = result
                    st.success("✅ Forecast generated successfully!")
                else:
                    st.error(f"❌ {result['error']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'forecast_result' in st.session_state:
            result = st.session_state['forecast_result']
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Forecast Results")
            
            # Display summary metrics
            summary = result['summary']
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>₹{summary['average_price']}</h3>
                    <p>Avg Price</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2_2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{summary['price_trend'].title()}</h3>
                    <p>Trend</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2_3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>₹{summary['volatility']}</h3>
                    <p>Volatility</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Create and display chart
            chart = frontend.create_price_chart(result['predictions'])
            st.plotly_chart(chart, use_container_width=True)
            
            # Price recommendations
            if summary['price_trend'] == 'increasing':
                st.markdown("""
                <div class="success-msg">
                    💡 <strong>Recommendation:</strong> Prices are trending upward. 
                    Consider holding your harvest for better returns.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-msg">
                    ⚠️ <strong>Recommendation:</strong> Prices are declining. 
                    Consider selling soon to avoid further losses.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# CROP RECOMMENDATIONS MODULE
# =============================================================================

elif app_mode == "🌱 Crop Recommendations":
    st.markdown("## 🌱 Smart Crop Recommendations")
    st.markdown("Discover the best crops to grow based on your location, season, and market conditions.")
    
    # Recommendation mode selection
    rec_mode = st.radio(
        "Choose Recommendation Mode",
        ["📍 Location-Based", "🔍 Crop Analysis"],
        horizontal=True
    )
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        if rec_mode == "📍 Location-Based":
            st.markdown("### 🗺️ Location Parameters")
            
            selected_state = st.selectbox(
                "Select State",
                frontend.states,
                help="Choose your state"
            )
            
            selected_month = st.selectbox(
                "Select Month",
                range(1, 13),
                format_func=lambda x: datetime(2024, x, 1).strftime('%B'),
                index=datetime.now().month - 1,
                help="Choose planting month"
            )
            
            district = st.text_input(
                "District (Optional)",
                help="Enter your district name"
            )
            
            api_data = {
                "state": selected_state,
                "month": selected_month,
                "district": district if district else None
            }
            
        else:  # Crop Analysis
            st.markdown("### 🌾 Crop Analysis")
            
            selected_crop = st.selectbox(
                "Select Crop to Analyze",
                frontend.crops,
                help="Choose crop for detailed analysis"
            )
            
            selected_state = st.selectbox(
                "Select State (Optional)",
                ["General"] + frontend.states,
                help="Choose your state for region-specific analysis"
            )
            
            api_data = {
                "crop": selected_crop,
                "state": selected_state if selected_state != "General" else None
            }
        
        # Generate recommendations button
        if st.button("🎯 Get Recommendations", use_container_width=True):
            with st.spinner("Analyzing crop suitability..."):
                result = frontend.call_api("recommend-crop", api_data)
                
                if "error" not in result:
                    st.session_state['recommendation_result'] = result
                    st.success("✅ Recommendations generated!")
                else:
                    st.error(f"❌ {result['error']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'recommendation_result' in st.session_state:
            result = st.session_state['recommendation_result']
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Recommendations")
            
            if result['mode'] == 'location_based':
                st.markdown(f"**📍 Location:** {result['state']}")
                st.markdown(f"**📅 Month:** {result['month_name']}")
                st.markdown(f"**🌤️ Season:** {result['season']}")
                
                # Display recommendations
                for i, rec in enumerate(result['recommendations'], 1):
                    with st.expander(f"#{i} {rec['crop']} - Score: {rec['suitability_score']}", 
                                   expanded=(i <= 3)):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Suitability Score", f"{rec['suitability_score']}/100")
                            st.metric("Expected Yield", f"{rec['estimated_yield']} T/Ha")
                        with col_b:
                            st.write("**Season Match:**", 
                                   "✅ Yes" if rec['season_match'] else "❌ No")
                            st.write("**Region Suitable:**", 
                                   "✅ Yes" if rec['region_suitable'] else "⚠️ Moderate")
                        
                        st.info(f"💡 {rec['recommendation_reason']}")
                
                # Create visualization
                chart = frontend.create_recommendations_chart(result['recommendations'])
                st.plotly_chart(chart, use_container_width=True)
            
            else:  # Crop analysis mode
                analysis = result['analysis']
                st.markdown(f"**🌾 Crop:** {result['crop']}")
                st.markdown(f"**📍 Region:** {result['state']}")
                
                # Display analysis metrics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Suitability", f"{analysis['suitability_score']}/100")
                with col_b:
                    st.metric("Est. Yield", f"{analysis['estimated_yield']} T/Ha")
                with col_c:
                    market_outlook = result['market_outlook']
                    st.metric("Demand", market_outlook['demand'].title())
                
                st.info(f"💡 **Analysis:** {analysis['recommendation_reason']}")
                
                # Market outlook
                st.markdown("**📈 Market Outlook:**")
                st.write(f"• **Demand:** {market_outlook['demand'].title()}")
                st.write(f"• **Price Stability:** {market_outlook['price_stability'].title()}")
                st.write(f"• **Competition:** {market_outlook['competition'].title()}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# MARKET ANALYTICS MODULE
# =============================================================================

elif app_mode == "📊 Market Analytics":
    st.markdown("## 📊 Market Analytics Dashboard")
    st.markdown("Comprehensive market insights and trends analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📈 Price Trends")
        
        # Sample data for demonstration
        dates = pd.date_range(start='2024-01-01', end='2024-09-01', freq='M')
        crops_sample = ['Rice', 'Wheat', 'Maize']
        
        trend_data = []
        for crop in crops_sample:
            base_price = {'Rice': 2200, 'Wheat': 1900, 'Maize': 1600}[crop]
            prices = base_price + np.random.normal(0, 200, len(dates)).cumsum()
            trend_data.extend([{'Date': date, 'Crop': crop, 'Price': price} 
                             for date, price in zip(dates, prices)])
        
        df_trends = pd.DataFrame(trend_data)
        
        fig_trends = px.line(df_trends, x='Date', y='Price', color='Crop',
                           title="8-Month Price Trends")
        fig_trends.update_layout(template="plotly_white", height=350)
        st.plotly_chart(fig_trends, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🌾 Crop Distribution")
        
        # Sample crop distribution data
        crop_dist = {
            'Crop': ['Rice', 'Wheat', 'Maize', 'Cotton', 'Others'],
            'Area': [25, 22, 18, 15, 20]  # Percentage
        }
        df_dist = pd.DataFrame(crop_dist)
        
        fig_pie = px.pie(df_dist, values='Area', names='Crop', 
                        title="Crop Area Distribution")
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Market insights
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💡 Market Insights")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown("""
        **🔥 Hot Markets**
        - Cotton prices rising 15%
        - Onion demand increasing
        - Export opportunities for Rice
        """)
    
    with col4:
        st.markdown("""
        **⚠️ Market Alerts**
        - Monsoon affecting Wheat
        - Storage issues with Potato
        - Transportation costs up 8%
        """)
    
    with col5:
        st.markdown("""
        **📅 Upcoming Events**
        - Harvest season begins Oct
        - New MSP announcement
        - Agricultural expo next month
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# ABOUT MODULE
# =============================================================================

elif app_mode == "ℹ️ About":
    st.markdown("## ℹ️ About AgriTech")
    
    st.markdown("""
    <div class="card">
        <h3>🎯 Our Mission</h3>
        <p>AgriTech is designed to empower farmers with cutting-edge AI technology for making informed decisions about crop pricing and cultivation strategies.</p>
        
        <h3>🚀 Features</h3>
        <ul>
            <li><strong>AI-Powered Price Forecasting:</strong> 15-day price predictions using XGBoost models</li>
            <li><strong>Smart Crop Recommendations:</strong> Location and season-based crop suggestions</li>
            <li><strong>Market Analytics:</strong> Comprehensive market trends and insights</li>
            <li><strong>User-Friendly Interface:</strong> Intuitive design for farmers of all tech levels</li>
        </ul>
        
        <h3>🛠️ Technology Stack</h3>
        <ul>
            <li><strong>Machine Learning:</strong> XGBoost, scikit-learn</li>
            <li><strong>Backend:</strong> Flask REST API</li>
            <li><strong>Frontend:</strong> Streamlit</li>
            <li><strong>Data Sources:</strong> Agmarknet, Agricultural datasets</li>
        </ul>
        
        <h3>📊 Data Sources</h3>
        <ul>
            <li>Agmarknet Price Data</li>
            <li>Crop Yield Statistics</li>
            <li>Weather and Rainfall Data</li>
            <li>Market Demand Indicators</li>
        </ul>
        
        <h3>👥 How to Use</h3>
        <ol>
            <li><strong>Price Forecasting:</strong> Select your crop and get 15-day price predictions</li>
            <li><strong>Crop Recommendations:</strong> Enter your location and get personalized crop suggestions</li>
            <li><strong>Market Analytics:</strong> Explore market trends and insights</li>
        </ol>
        
        <h3>🤝 Support</h3>
        <p>For technical support or feature requests, please contact our development team.</p>
        
        <hr>
        <p><em>Built with ❤️ for Indian farmers</em></p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; opacity: 0.7;">
    <p>🌾 AgriTech v1.0 | Empowering Farmers with AI | Built for AgriTech Hackathon 2024</p>
</div>
""", unsafe_allow_html=True)