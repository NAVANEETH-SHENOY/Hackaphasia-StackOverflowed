import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Sprout, 
  BarChart3, 
  ArrowRight,
  Wheat,
  DollarSign,
  Target,
  Users
} from 'lucide-react'
import Card from '../components/Card'
import MetricCard from '../components/MetricCard'
import Button from '../components/Button'
import { agriTechAPI } from '../services/api'
import toast from 'react-hot-toast'
import PageTransition from '../components/PageTransition'

const Dashboard = () => {
  const [apiStatus, setApiStatus] = useState('checking')
  const [stats] = useState({
    totalCrops: 10,
    activeForecasts: 0,
    recommendations: 0,
    farmersHelped: 1250
  })

  useEffect(() => {
    checkAPIStatus()
  }, [])

  const checkAPIStatus = async () => {
    try {
      await agriTechAPI.healthCheck()
      setApiStatus('connected')
      toast.success('API Connected Successfully!')
    } catch (error) {
      setApiStatus('disconnected')
      toast.error('API Connection Failed')
    }
  }

  const quickActions = [
    {
      title: 'Price Forecast',
      description: 'Get 15-day price predictions for your crops',
      icon: TrendingUp,
      href: '/price-forecast',
      color: 'primary'
    },
    {
      title: 'Crop Recommendations',
      description: 'Find the best crops for your location and season',
      icon: Sprout,
      href: '/crop-recommendations',
      color: 'secondary'
    },
    {
      title: 'Market Analytics',
      description: 'Analyze market trends and insights',
      icon: BarChart3,
      href: '/market-analytics',
      color: 'accent'
    }
  ]

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
          Welcome to AgriTech
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          Empowering farmers with AI-driven crop price forecasts and intelligent recommendations. 
          Make data-driven decisions for better yields and profits.
        </p>
      </motion.div>

      {/* API Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${
              apiStatus === 'connected' ? 'bg-green-500 animate-pulse' : 
              apiStatus === 'disconnected' ? 'bg-red-500' : 'bg-yellow-500'
            }`}></div>
            <span className="font-medium">
              {apiStatus === 'connected' ? 'API Connected' : 
               apiStatus === 'disconnected' ? 'API Disconnected' : 'Checking Connection...'}
            </span>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={checkAPIStatus}
            loading={apiStatus === 'checking'}
          >
            {apiStatus === 'checking' ? 'Checking...' : 'Refresh'}
          </Button>
        </Card>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <MetricCard
          title="Supported Crops"
          value={stats.totalCrops}
          subtitle="Different crop types"
          icon={Wheat}
          color="primary"
        />
        <MetricCard
          title="Active Forecasts"
          value={stats.activeForecasts}
          subtitle="Price predictions"
          icon={DollarSign}
          color="secondary"
        />
        <MetricCard
          title="Recommendations"
          value={stats.recommendations}
          subtitle="Crop suggestions"
          icon={Target}
          color="accent"
        />
        <MetricCard
          title="Farmers Helped"
          value={stats.farmersHelped.toLocaleString()}
          subtitle="Active users"
          icon={Users}
          color="green"
        />
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
            >
              <Card className="group cursor-pointer hover:shadow-2xl transition-all duration-300">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${
                    action.color === 'primary' ? 'from-primary-500 to-primary-600' :
                    action.color === 'secondary' ? 'from-secondary-500 to-secondary-600' :
                    'from-accent-500 to-accent-600'
                  } text-white group-hover:scale-110 transition-transform duration-300`}>
                    <action.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {action.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {action.description}
                    </p>
                    <div className="flex items-center text-primary-600 font-medium group-hover:text-primary-700">
                      <span>Get Started</span>
                      <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform duration-200" />
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Features Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Why Choose AgriTech?</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered Predictions</h3>
              <p className="text-gray-600">
                Advanced machine learning models provide accurate 15-day price forecasts with 85%+ accuracy.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-secondary-500 to-secondary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sprout className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Recommendations</h3>
              <p className="text-gray-600">
                Get personalized crop suggestions based on your location, season, and market conditions.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-accent-500 to-accent-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Market Insights</h3>
              <p className="text-gray-600">
                Comprehensive market analytics and trends to help you make informed decisions.
              </p>
            </div>
          </div>
        </Card>
      </motion.div>
      </div>
    </PageTransition>
  )
}

export default Dashboard