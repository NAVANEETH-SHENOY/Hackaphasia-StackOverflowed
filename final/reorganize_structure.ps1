Write-Host "Reorganizing AgriTech project structure..." -ForegroundColor Green

Write-Host "`nStep 1: Moving model files to backend..." -ForegroundColor Yellow
Move-Item "crop_recommendation_model.pkl" "backend\" -Force
Move-Item "data_processor.pkl" "backend\" -Force
Move-Item "price_forecast_model.pkl" "backend\" -Force
Move-Item "agritech_analysis_dashboard.png" "backend\" -Force
Move-Item "price_forecast_sample.png" "backend\" -Force

Write-Host "`nStep 2: Deleting Streamlit frontend..." -ForegroundColor Yellow
Remove-Item "frontend" -Recurse -Force

Write-Host "`nStep 3: Renaming react-frontend to frontend..." -ForegroundColor Yellow
Move-Item "react-frontend" "frontend" -Force

Write-Host "`n✅ Project structure reorganized successfully!" -ForegroundColor Green
Write-Host "`nNew structure:" -ForegroundColor Cyan
Write-Host "final/" -ForegroundColor White
Write-Host "├── backend/          # Complete backend with models" -ForegroundColor White
Write-Host "├── frontend/         # React frontend" -ForegroundColor White
Write-Host "├── model_pipline/    # ML training" -ForegroundColor White
Write-Host "└── README.md         # Project docs" -ForegroundColor White

Read-Host "`nPress Enter to continue"
