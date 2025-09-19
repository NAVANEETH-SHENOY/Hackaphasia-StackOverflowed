import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Sprout, 
  MapPin, 
  Calendar, 
  Target,
  CheckCircle,
  AlertCircle,
  Droplets,
  Sun,
  Thermometer
} from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import Select from '../components/Select'
import { agriTechAPI } from '../services/api'
import toast from 'react-hot-toast'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const CropRecommendations = () => {
  const [mode, setMode] = useState('location') // 'location' or 'crop'
  const [loading, setLoading] = useState(false)
  const [recommendations, setRecommendations] = useState(null)
  const [formData, setFormData] = useState({
    state: 'Maharashtra',
    month: new Date().getMonth() + 1,
    district: '',
    crop: 'Rice'
  })

  const states = [
    { value: 'Maharashtra', label: 'Maharashtra' },
    { value: 'Karnataka', label: 'Karnataka' },
    { value: 'Andhra Pradesh', label: 'Andhra Pradesh' },
    { value: 'Tamil Nadu', label: 'Tamil Nadu' },
    { value: 'Gujarat', label: 'Gujarat' },
    { value: 'Rajasthan', label: 'Rajasthan' },
    { value: 'Madhya Pradesh', label: 'Madhya Pradesh' },
    { value: 'Uttar Pradesh', label: 'Uttar Pradesh' }
  ]

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

  const months = [
    { value: 1, label: 'January' },
    { value: 2, label: 'February' },
    { value: 3, label: 'March' },
    { value: 4, label: 'April' },
    { value: 5, label: 'May' },
    { value: 6, label: 'June' },
    { value: 7, label: 'July' },
    { value: 8, label: 'August' },
    { value: 9, label: 'September' },
    { value: 10, label: 'October' },
    { value: 11, label: 'November' },
    { value: 12, label: 'December' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      let data
      if (mode === 'location') {
        data = await agriTechAPI.getLocationBasedRecommendations(
          formData.state, 
          formData.month, 
          formData.district || null
        )
      } else {
        data = await agriTechAPI.analyzeCrop(formData.crop, formData.state || null)
      }
      setRecommendations(data)
      toast.success('Recommendations generated successfully!')
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  const getSeasonIcon = (season) => {
    switch (season) {
      case 'Monsoon': return <Droplets className="h-5 w-5 text-blue-500" />
      case 'Summer': return <Sun className="h-5 w-5 text-yellow-500" />
      case 'Winter': return <Thermometer className="h-5 w-5 text-blue-300" />
      default: return <Calendar className="h-5 w-5 text-gray-500" />
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const formatChartData = (recommendations) => {
    return recommendations.map(rec => ({
      crop: rec.crop,
      score: rec.suitability_score
    }))
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold gradient-text mb-4">
          Crop Recommendations
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          Discover the best crops to grow based on your location, season, and market conditions.
        </p>
      </motion.div>

      {/* Mode Selection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => setMode('location')}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${
                mode === 'location'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <MapPin className="h-4 w-4 inline mr-2" />
              Location-Based
            </button>
            <button
              onClick={() => setMode('crop')}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${
                mode === 'crop'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Target className="h-4 w-4 inline mr-2" />
              Crop Analysis
            </button>
          </div>
        </Card>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Input Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {mode === 'location' ? 'Location Parameters' : 'Crop Analysis'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <AnimatePresence mode="wait">
                {mode === 'location' ? (
                  <motion.div
                    key="location"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-4"
                  >
                    <Select
                      label="Select State"
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                      options={states}
                      helperText="Choose your state"
                    />

                    <Select
                      label="Select Month"
                      value={formData.month}
                      onChange={(e) => setFormData({ ...formData, month: parseInt(e.target.value) })}
                      options={months}
                      helperText="Choose planting month"
                    />

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        District (Optional)
                      </label>
                      <input
                        type="text"
                        value={formData.district}
                        onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                        placeholder="Enter your district name"
                        className="input-field"
                      />
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="crop"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-4"
                  >
                    <Select
                      label="Select Crop to Analyze"
                      value={formData.crop}
                      onChange={(e) => setFormData({ ...formData, crop: e.target.value })}
                      options={crops}
                      helperText="Choose crop for detailed analysis"
                    />

                    <Select
                      label="Select State (Optional)"
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                      options={[{ value: '', label: 'General' }, ...states]}
                      helperText="Choose your state for region-specific analysis"
                    />
                  </motion.div>
                )}
              </AnimatePresence>

              <Button
                type="submit"
                loading={loading}
                className="w-full"
                disabled={loading}
              >
                {loading ? 'Analyzing...' : 'Get Recommendations'}
              </Button>
            </form>

            {/* Tips */}
            <div className="mt-8 p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold text-green-900 mb-2">💡 Farming Tips</h3>
              <ul className="text-sm text-green-800 space-y-1">
                <li>• Consider soil type and water availability</li>
                <li>• Check local market demand and prices</li>
                <li>• Plan crop rotation for soil health</li>
                <li>• Monitor weather forecasts regularly</li>
              </ul>
            </div>
          </Card>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="lg:col-span-2"
        >
          {recommendations ? (
            <div className="space-y-6">
              {recommendations.mode === 'location_based' ? (
                <>
                  {/* Location Info */}
                  <Card>
                    <div className="flex items-center space-x-4 mb-4">
                      <MapPin className="h-6 w-6 text-primary-600" />
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">
                          {recommendations.state}
                        </h3>
                        <p className="text-gray-600">
                          {recommendations.month_name} • {recommendations.season}
                        </p>
                      </div>
                      {getSeasonIcon(recommendations.season)}
                    </div>
                  </Card>

                  {/* Recommendations Chart */}
                  <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4">
                      Crop Suitability Scores
                    </h3>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={formatChartData(recommendations.recommendations)}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                          <XAxis 
                            dataKey="crop" 
                            stroke="#666"
                            fontSize={12}
                          />
                          <YAxis 
                            stroke="#666"
                            fontSize={12}
                            domain={[0, 100]}
                          />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'white',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                        formatter={(value) => [`${value}%`, 'Suitability Score']}
                      />
                          <Bar 
                            dataKey="score" 
                            fill="#667eea"
                            radius={[4, 4, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </Card>

                  {/* Recommendation Cards */}
                  <div className="space-y-4">
                    {recommendations.recommendations.map((rec, index) => (
                      <motion.div
                        key={rec.crop}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <Card className="hover:shadow-lg transition-all duration-300">
                          <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center space-x-3">
                              <div className="text-2xl font-bold text-gray-900">
                                #{index + 1}
                              </div>
                              <div>
                                <h4 className="text-xl font-bold text-gray-900">
                                  {rec.crop}
                                </h4>
                                <p className="text-gray-600">
                                  Expected Yield: {rec.estimated_yield} T/Ha
                                </p>
                              </div>
                            </div>
                            <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(rec.suitability_score)}`}>
                              {rec.suitability_score}/100
                            </div>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div className="flex items-center space-x-2">
                              {rec.season_match ? (
                                <CheckCircle className="h-5 w-5 text-green-600" />
                              ) : (
                                <AlertCircle className="h-5 w-5 text-yellow-600" />
                              )}
                              <span className="text-sm">
                                Season Match: {rec.season_match ? 'Yes' : 'Moderate'}
                              </span>
                            </div>
                            <div className="flex items-center space-x-2">
                              {rec.region_suitable ? (
                                <CheckCircle className="h-5 w-5 text-green-600" />
                              ) : (
                                <AlertCircle className="h-5 w-5 text-yellow-600" />
                              )}
                              <span className="text-sm">
                                Region Suitable: {rec.region_suitable ? 'Yes' : 'Moderate'}
                              </span>
                            </div>
                          </div>

                          <div className="p-3 bg-blue-50 rounded-lg">
                            <p className="text-sm text-blue-800">
                              <strong>💡 Recommendation:</strong> {rec.recommendation_reason}
                            </p>
                          </div>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                </>
              ) : (
                /* Crop Analysis Mode */
                <div className="space-y-6">
                  <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4">
                      {recommendations.crop} Analysis
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-primary-600">
                          {recommendations.analysis.suitability_score}/100
                        </div>
                        <div className="text-sm text-gray-600">Suitability Score</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-secondary-600">
                          {recommendations.analysis.estimated_yield} T/Ha
                        </div>
                        <div className="text-sm text-gray-600">Expected Yield</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-accent-600">
                          {recommendations.state}
                        </div>
                        <div className="text-sm text-gray-600">Region</div>
                      </div>
                    </div>
                  </Card>

                  <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4">Analysis Details</h3>
                    <div className="space-y-4">
                      <div className="p-4 bg-blue-50 rounded-lg">
                        <p className="text-blue-800">
                          <strong>💡 Analysis:</strong> {recommendations.analysis.recommendation_reason}
                        </p>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Market Outlook</h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="p-3 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Demand</div>
                            <div className="font-semibold capitalize">
                              {recommendations.market_outlook.demand}
                            </div>
                          </div>
                          <div className="p-3 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Price Stability</div>
                            <div className="font-semibold capitalize">
                              {recommendations.market_outlook.price_stability}
                            </div>
                          </div>
                          <div className="p-3 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Competition</div>
                            <div className="font-semibold capitalize">
                              {recommendations.market_outlook.competition}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Card>
                </div>
              )}
            </div>
          ) : (
            <Card className="text-center py-12">
              <Sprout className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No Recommendations Yet
              </h3>
              <p className="text-gray-600">
                Select your parameters and generate recommendations to see detailed crop analysis.
              </p>
            </Card>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default CropRecommendations
