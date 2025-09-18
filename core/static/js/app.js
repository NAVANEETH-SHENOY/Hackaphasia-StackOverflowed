// Karnataka Crop Forecasting Platform JavaScript

class CropForecastingApp {
    constructor() {
        this.init();
    }

    init() {
        this.loadDistricts();
        this.loadDatasets();
        this.setupEventListeners();
    }

    setupEventListeners() {
        const form = document.getElementById('recommendation-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.getRecommendations();
        });
    }

    async loadDistricts() {
        try {
            const response = await fetch('/api/districts');
            const districts = await response.json();
            
            const districtSelect = document.getElementById('district');
            districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading districts:', error);
        }
    }

    async loadDatasets() {
        try {
            const response = await fetch('/api/datasets');
            const data = await response.json();
            this.displayDatasets(data);
        } catch (error) {
            console.error('Error loading datasets:', error);
            this.showError('Failed to load datasets');
        }
    }

    displayDatasets(data) {
        const container = document.getElementById('datasets-container');
        
        let html = '<div class="row">';
        
        data.datasets.forEach(dataset => {
            html += `
                <div class="col-md-6 mb-3">
                    <div class="card dataset-card fade-in">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-database me-2"></i>
                                ${dataset.name}
                            </h5>
                        </div>
                        <div class="card-body">
                            <p><strong>Source:</strong> ${dataset.source}</p>
                            <p><strong>Coverage:</strong> ${dataset.coverage}</p>
                            <p><strong>Years:</strong> ${dataset.years}</p>
                            <p><strong>Fields:</strong> ${dataset.fields}</p>
                            <p><strong>Format:</strong> ${dataset.format}</p>
                            <p><strong>License:</strong> ${dataset.license}</p>
                            <p><strong>Quality:</strong> ${dataset.quality}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        // Add synthetic data usage section
        html += `
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-robot me-2"></i>
                                Synthetic Data Usage
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Market Prices</h6>
                                    <p class="small">${data.synthetic_data_usage.market_prices}</p>
                                </div>
                                <div class="col-md-6">
                                    <h6>Weather Patterns</h6>
                                    <p class="small">${data.synthetic_data_usage.weather_patterns}</p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Cost Estimates</h6>
                                    <p class="small">${data.synthetic_data_usage.cost_estimates}</p>
                                </div>
                                <div class="col-md-6">
                                    <h6>Yield Projections</h6>
                                    <p class="small">${data.synthetic_data_usage.yield_projections}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    async getRecommendations() {
        const district = document.getElementById('district').value;
        const month = document.getElementById('month').value;
        
        if (!district || !month) {
            this.showError('Please select both district and month');
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch('/api/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ district, month: parseInt(month) })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
            } else {
                this.displayRecommendations(data);
            }
        } catch (error) {
            console.error('Error getting recommendations:', error);
            this.showError('Failed to get recommendations');
        }
    }

    displayRecommendations(data) {
        const container = document.getElementById('results-container');
        
        let html = `
            <div class="row mb-3">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="text-center mb-3">
                                <i class="fas fa-seedling me-2"></i>
                                Recommendations for ${data.district} - ${this.getMonthName(data.month)}
                            </h4>
                            <p class="text-center text-muted">
                                Season: <span class="season-badge season-${data.season}">${data.season.toUpperCase()}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        data.recommendations.forEach((rec, index) => {
            html += `
                <div class="row mb-3">
                    <div class="col-12">
                        <div class="card recommendation-card fade-in">
                            <div class="card-header">
                                <div class="row align-items-center">
                                    <div class="col-md-8">
                                        <h5 class="mb-0">
                                            <span class="crop-icon me-2">${index + 1}</span>
                                            ${rec.crop}
                                            <span class="kannada-text ms-2">(${rec.kannada_name})</span>
                                        </h5>
                                    </div>
                                    <div class="col-md-4 text-end">
                                        <span class="season-badge season-${rec.season}">${rec.season.toUpperCase()}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6><i class="fas fa-calendar me-2"></i>Timing</h6>
                                        <p><strong>Sowing:</strong> ${rec.sowing_window}</p>
                                        <p><strong>Harvest:</strong> ${rec.harvest_window}</p>
                                        <p><strong>Duration:</strong> ${rec.duration_days} days</p>
                                        
                                        <h6 class="mt-3"><i class="fas fa-chart-line me-2"></i>Expected Yield</h6>
                                        <p>${rec.expected_yield.toFixed(1)} ${this.getYieldUnit(rec.crop)} per acre</p>
                                        
                                        <h6 class="mt-3"><i class="fas fa-rupee-sign me-2"></i>Price Range</h6>
                                        <p class="price-range">
                                            ₹${rec.price_range.min.toFixed(0)} - ₹${rec.price_range.max.toFixed(0)} 
                                            <small>(${this.getPriceUnit(rec.crop)})</small>
                                        </p>
                                    </div>
                                    <div class="col-md-6">
                                        <h6><i class="fas fa-calculator me-2"></i>Profitability</h6>
                                        <div class="mb-2">
                                            <strong>Revenue:</strong> ₹${rec.profitability.revenue_per_acre.toFixed(0)}/acre<br>
                                            <strong>Cost:</strong> ₹${rec.profitability.cost_per_acre.toFixed(0)}/acre<br>
                                            <strong>Profit:</strong> 
                                            <span class="${rec.profitability.profit_per_acre > 0 ? 'profit-positive' : 'profit-negative'}">
                                                ₹${rec.profitability.profit_per_acre.toFixed(0)}/acre
                                            </span>
                                        </div>
                                        <p class="small text-muted">
                                            Margin: ${rec.profitability.profit_margin.toFixed(1)}%
                                        </p>
                                        
                                        <h6 class="mt-3"><i class="fas fa-exclamation-triangle me-2"></i>Risks</h6>
                                        <ul class="small">
                                            ${rec.risks.map(risk => `<li>${risk}</li>`).join('')}
                                        </ul>
                                        
                                        ${rec.alternatives.length > 0 ? `
                                            <h6 class="mt-3"><i class="fas fa-exchange-alt me-2"></i>Alternatives</h6>
                                            <p class="small">${rec.alternatives.join(', ')}</p>
                                        ` : ''}
                                    </div>
                                </div>
                                
                                <div class="row mt-3">
                                    <div class="col-12">
                                        <div class="alert alert-info">
                                            <i class="fas fa-info-circle me-2"></i>
                                            <strong>Recommendation:</strong> ${rec.recommendation_text}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        // Add data sources section
        html += `
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-info-circle me-2"></i>
                                Data Sources & Methodology
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Data Sources</h6>
                                    <ul class="small">
                                        ${data.data_sources.map(source => `<li>${source}</li>`).join('')}
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h6>Synthetic Data Usage</h6>
                                    <ul class="small">
                                        ${Object.entries(data.synthetic_data_used).map(([key, value]) => 
                                            `<li><strong>${key.replace('_', ' ').toUpperCase()}:</strong> ${value}</li>`
                                        ).join('')}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
    }

    getMonthName(month) {
        const months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        return months[month - 1];
    }

    getYieldUnit(crop) {
        if (crop.includes('Onion') || crop.includes('Tomato')) {
            return 'kg';
        }
        return 'quintals';
    }

    getPriceUnit(crop) {
        if (crop.includes('Onion') || crop.includes('Tomato')) {
            return 'per kg';
        }
        return 'per quintal';
    }

    showLoading() {
        const container = document.getElementById('results-container');
        container.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        container.style.display = 'block';
    }

    showError(message) {
        const container = document.getElementById('results-container');
        container.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${message}
            </div>
        `;
        container.style.display = 'block';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CropForecastingApp();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
