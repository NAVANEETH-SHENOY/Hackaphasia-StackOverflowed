@echo off
echo Reorganizing AgriTech project structure...

echo.
echo Step 1: Moving model files to backend...
move crop_recommendation_model.pkl backend\
move data_processor.pkl backend\
move price_forecast_model.pkl backend\
move agritech_analysis_dashboard.png backend\
move price_forecast_sample.png backend\

echo.
echo Step 2: Deleting Streamlit frontend...
rmdir /s /q frontend

echo.
echo Step 3: Renaming react-frontend to frontend...
move react-frontend frontend

echo.
echo ✅ Project structure reorganized successfully!
echo.
echo New structure:
echo final/
echo ├── backend/          # Complete backend with models
echo ├── frontend/         # React frontend
echo ├── model_pipline/    # ML training
echo └── README.md         # Project docs
echo.
pause
