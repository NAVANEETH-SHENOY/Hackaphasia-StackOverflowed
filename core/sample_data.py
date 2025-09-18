"""
Sample data and test cases for Karnataka Crop Demand Forecasting Platform
"""

import json
from data_models import CropDataManager, RecommendationEngine, SyntheticDataGenerator

def test_platform():
    """Test the platform with sample data"""
    
    # Initialize components
    data_manager = CropDataManager()
    recommendation_engine = RecommendationEngine(data_manager)
    synthetic_generator = SyntheticDataGenerator(data_manager)
    
    print("🌾 Karnataka Crop Demand Forecasting Platform - Test Results")
    print("=" * 60)
    
    # Test 1: Dataset Summary
    print("\n📊 Dataset Summary:")
    datasets = data_manager.get_datasets_summary()
    for dataset in datasets["datasets"]:
        print(f"• {dataset['name']}: {dataset['coverage']} ({dataset['years']})")
    
    # Test 2: Sample Recommendations
    print("\n🌱 Sample Recommendations:")
    test_cases = [
        {"district": "Mandya", "month": 9, "description": "Mandya - September (Kharif)"},
        {"district": "Belagavi", "month": 11, "description": "Belagavi - November (Rabi)"},
        {"district": "Mysuru", "month": 6, "description": "Mysuru - June (Kharif)"}
    ]
    
    for test_case in test_cases:
        print(f"\n📍 {test_case['description']}")
        recommendations = recommendation_engine.get_recommendations(
            test_case["district"], test_case["month"]
        )
        
        for i, rec in enumerate(recommendations["recommendations"], 1):
            print(f"  {i}. {rec['crop']} ({rec['kannada_name']})")
            print(f"     Season: {rec['season'].upper()}")
            print(f"     Duration: {rec['duration_days']} days")
            print(f"     Profit: ₹{rec['profitability']['profit_per_acre']:,.0f}/acre")
            print(f"     Risks: {', '.join(rec['risks'][:2])}")
    
    # Test 3: Synthetic Data Generation
    print("\n🤖 Synthetic Data Generation:")
    synthetic_tests = [
        {"district": "Mandya", "crop": "Paddy (Rice)", "data_type": "prices"},
        {"district": "Belagavi", "crop": "Maize", "data_type": "yields"},
        {"district": "Mysuru", "crop": "Tomato", "data_type": "costs"}
    ]
    
    for test in synthetic_tests:
        print(f"\n🔧 Generating {test['data_type']} data for {test['crop']} in {test['district']}")
        synthetic_data = synthetic_generator.generate_data(
            test["district"], test["crop"], test["data_type"]
        )
        
        if "error" not in synthetic_data:
            print(f"   ✅ Generated {len(synthetic_data['generated_data'])} records")
            print(f"   📝 Methodology: {synthetic_data['methodology']}")
            print(f"   🏷️  Label: {synthetic_data['label']}")
        else:
            print(f"   ❌ Error: {synthetic_data['error']}")
    
    # Test 4: Data Quality Assessment
    print("\n📈 Data Quality Assessment:")
    districts = data_manager.get_karnataka_districts()
    crops = data_manager.get_major_crops()
    
    print(f"   • Districts covered: {len(districts)}")
    print(f"   • Crops supported: {len(crops)}")
    print(f"   • Crop calendars: {len(data_manager.crop_calendars)}")
    print(f"   • Market data: {len(data_manager.market_data)}")
    print(f"   • Weather patterns: {len(data_manager.weather_data)}")
    print(f"   • Cost data: {len(data_manager.cost_data)}")
    
    print("\n✅ Platform testing completed successfully!")
    return True

def generate_sample_output():
    """Generate sample output for documentation"""
    
    data_manager = CropDataManager()
    recommendation_engine = RecommendationEngine(data_manager)
    
    # Generate sample recommendation
    sample_rec = recommendation_engine.get_recommendations("Mandya", 9)
    
    # Save to JSON file
    with open("sample_recommendation.json", "w", encoding="utf-8") as f:
        json.dump(sample_rec, f, indent=2, ensure_ascii=False)
    
    print("📄 Sample recommendation saved to sample_recommendation.json")
    
    # Generate sample synthetic data
    synthetic_generator = SyntheticDataGenerator(data_manager)
    sample_synthetic = synthetic_generator.generate_data("Mandya", "Paddy (Rice)", "prices")
    
    with open("sample_synthetic_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_synthetic, f, indent=2, ensure_ascii=False)
    
    print("📄 Sample synthetic data saved to sample_synthetic_data.json")

if __name__ == "__main__":
    test_platform()
    generate_sample_output()
