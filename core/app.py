"""
Karnataka Crop Demand Forecasting Platform
A comprehensive system for helping Karnataka farmers make informed decisions
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from data_models import CropDataManager, RecommendationEngine, SyntheticDataGenerator
from utils import translate_to_kannada, format_currency, calculate_season

app = Flask(__name__)

# Initialize data managers
crop_data_manager = CropDataManager()
recommendation_engine = RecommendationEngine(crop_data_manager)
synthetic_generator = SyntheticDataGenerator(crop_data_manager)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/datasets')
def get_datasets():
    """API endpoint to get available datasets summary"""
    datasets = crop_data_manager.get_datasets_summary()
    return jsonify(datasets)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get crop recommendations for a farmer"""
    try:
        data = request.get_json()
        district = data.get('district')
        month = data.get('month')
        
        if not district or not month:
            return jsonify({'error': 'District and month are required'}), 400
        
        recommendations = recommendation_engine.get_recommendations(district, month)
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/synthetic-data', methods=['POST'])
def generate_synthetic_data():
    """API endpoint to generate synthetic data for missing information"""
    try:
        data = request.get_json()
        district = data.get('district')
        crop = data.get('crop')
        data_type = data.get('data_type')  # 'prices', 'yields', 'costs', 'weather'
        
        synthetic_data = synthetic_generator.generate_data(district, crop, data_type)
        return jsonify(synthetic_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/districts')
def get_districts():
    """Get list of Karnataka districts"""
    districts = crop_data_manager.get_karnataka_districts()
    return jsonify(districts)

@app.route('/api/crops')
def get_crops():
    """Get list of major crops"""
    crops = crop_data_manager.get_major_crops()
    return jsonify(crops)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
