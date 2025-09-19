import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const agriTechAPI = {
  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw new Error('API is not available')
    }
  },

  // Price forecasting
  async forecastPrice(crop, days = 15) {
    try {
      const response = await api.post('/forecast-price', {
        crop,
        days
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get price forecast')
    }
  },

  // Crop recommendations
  async recommendCrops(data) {
    try {
      const response = await api.post('/recommend-crop', data)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get crop recommendations')
    }
  },

  // Location-based recommendations
  async getLocationBasedRecommendations(state, month, district = null) {
    return this.recommendCrops({
      state,
      month,
      district
    })
  },

  // Crop analysis
  async analyzeCrop(crop, state = null) {
    return this.recommendCrops({
      crop,
      state
    })
  }
}

export default api
