import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  DollarSign, 
  AlertTriangle,
  CheckCircle
} from 'lucide-react'
import Card from '../components/Card'
import MetricCard from '../components/MetricCard'
import Button from '../components/Button'
import Select from '../components/Select'
import { agriTechAPI } from '../services/api'
import toast from 'react-hot-toast'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import PageTransition from '../components/PageTransition'

const PriceForecast = () => {
  const [formData, setFormData] = useState({
    crop: 'Rice',
    days: 15
  })
  const [loading, setLoading] = useState(false)
  const [forecastData, setForecastData] = useState(null)

  const crops = [
    { value: 'Rice', label: 'Rice' },
    { value: 'Wheat', label: 'Wheat' },
    { value: 'Maize', label: 'Maize' },
    { value: 'Cotton', label: 'Cotton' },
    { value: 'Sugarcane', label: 'Sugarcane' },
    { value: 'Onion', label: 'Onion' },
    { value: 'Potato', label: 'Potato' },
    { value: 'Tomato', label: 'Tomato' },
    { value: 'Soybean', label: 'Soybean' },
    { value: 'Groundnut', label: 'Groundnut' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const data = await agriTechAPI.forecastPrice(formData.crop, formData.days)
      setForecastData(data)
      toast.success('Price forecast generated successfully!')
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  const formatChartData = (predictions) => {
    return predictions.map(pred => ({
      date: new Date(pred.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      price: pred.price,
      fullDate: pred.date
    }))
  }


  return (
    <PageTransition>
      <div className="space-y-8">
        {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold gradient-text mb-4">
          Price Forecasting
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          Get AI-powered price predictions for the next 15 days to optimize your selling strategy.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Input Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Forecast Parameters</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <Select
                label="Select Crop"
                value={formData.crop}
                onChange={(e) => setFormData({ ...formData, crop: e.target.value })}
                options={crops}
                helperText="Choose the crop for price forecasting"
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Forecast Period: {formData.days} days
                </label>
                <input
                  type="range"
                  min="5"
                  max="30"
                  value={formData.days}
                  onChange={(e) => setFormData({ ...formData, days: parseInt(e.target.value) })}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>5 days</span>
                  <span>30 days</span>
                </div>
              </div>

              <Button
                type="submit"
                loading={loading}
                className="w-full"
                disabled={loading}
              >
                {loading ? 'Generating Forecast...' : 'Generate Forecast'}
              </Button>
            </form>

            {/* Tips */}
            <div className="mt-8 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-2">💡 Pro Tips</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Check forecasts regularly for updates</li>
                <li>• Consider seasonal patterns in your decisions</li>
                <li>• Monitor market volatility indicators</li>
                <li>• Combine with local market knowledge</li>
              </ul>
            </div>
          </Card>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-2"
        >
          {forecastData ? (
            <div className="space-y-6">
              {/* Summary Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <MetricCard
                  title="Average Price"
                  value={`₹${forecastData.summary.average_price}`}
                  subtitle="Per quintal"
                  icon={DollarSign}
                  color="primary"
                />
                <MetricCard
                  title="Price Trend"
                  value={forecastData.summary.price_trend}
                  subtitle="Direction"
                  icon={TrendingUp}
                  color={forecastData.summary.price_trend === 'increasing' ? 'green' : 'red'}
                />
                <MetricCard
                  title="Volatility"
                  value={`₹${forecastData.summary.volatility}`}
                  subtitle="Price variation"
                  icon={AlertTriangle}
                  color="accent"
                />
              </div>

              {/* Price Chart */}
              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {forecastData.crop} Price Forecast ({forecastData.forecast_days} days)
                </h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={formatChartData(forecastData.predictions)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis 
                        dataKey="date" 
                        stroke="#666"
                        fontSize={12}
                      />
                      <YAxis 
                        stroke="#666"
                        fontSize={12}
                        tickFormatter={(value) => `₹${value}`}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'white',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                        formatter={(value) => [`₹${value}`, 'Price']}
                        labelFormatter={(label) => `Date: ${label}`}
                      />
                      <Line
                        type="monotone"
                        dataKey="price"
                        stroke="#667eea"
                        strokeWidth={3}
                        dot={{ fill: '#764ba2', strokeWidth: 2, r: 4 }}
                        activeDot={{ r: 6, stroke: '#667eea', strokeWidth: 2 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </Card>

              {/* Recommendations */}
              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Recommendations</h3>
                <div className="space-y-4">
                  {forecastData.summary.price_trend === 'increasing' ? (
                    <div className="flex items-start space-x-3 p-4 bg-green-50 rounded-lg border border-green-200">
                      <CheckCircle className="h-6 w-6 text-green-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-green-900">Positive Trend Detected</h4>
                        <p className="text-green-800 text-sm mt-1">
                          Prices are trending upward. Consider holding your harvest for better returns. 
                          Monitor the market closely for optimal selling opportunities.
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-start space-x-3 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <AlertTriangle className="h-6 w-6 text-yellow-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-yellow-900">Declining Trend Detected</h4>
                        <p className="text-yellow-800 text-sm mt-1">
                          Prices are declining. Consider selling soon to avoid further losses. 
                          Look for local market opportunities or storage options.
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <strong>Min Price:</strong> ₹{forecastData.summary.min_price}
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <strong>Max Price:</strong> ₹{forecastData.summary.max_price}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          ) : (
            <Card className="text-center py-12">
              <TrendingUp className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No Forecast Data
              </h3>
              <p className="text-gray-600">
                Select a crop and generate a price forecast to see detailed predictions and recommendations.
              </p>
            </Card>
          )}
        </motion.div>
      </div>
      </div>
    </PageTransition>
  )
}

export default PriceForecast