import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  DollarSign,
  Calendar,
  Globe
} from 'lucide-react'
import Card from '../components/Card'
import MetricCard from '../components/MetricCard'
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts'
import PageTransition from '../components/PageTransition'

const MarketAnalytics = () => {
  const [timeRange, setTimeRange] = useState('6months')
  const [selectedCrop, setSelectedCrop] = useState('Rice')

  // Sample data - in real app, this would come from API
  const priceTrendsData = [
    { month: 'Jan', Rice: 2200, Wheat: 1950, Maize: 1650 },
    { month: 'Feb', Rice: 2250, Wheat: 2000, Maize: 1700 },
    { month: 'Mar', Rice: 2300, Wheat: 2050, Maize: 1750 },
    { month: 'Apr', Rice: 2350, Wheat: 2100, Maize: 1800 },
    { month: 'May', Rice: 2400, Wheat: 2150, Maize: 1850 },
    { month: 'Jun', Rice: 2450, Wheat: 2200, Maize: 1900 },
    { month: 'Jul', Rice: 2500, Wheat: 2250, Maize: 1950 },
    { month: 'Aug', Rice: 2550, Wheat: 2300, Maize: 2000 },
    { month: 'Sep', Rice: 2600, Wheat: 2350, Maize: 2050 }
  ]

  const cropDistributionData = [
    { name: 'Rice', value: 25, color: '#667eea' },
    { name: 'Wheat', value: 22, color: '#764ba2' },
    { name: 'Maize', value: 18, color: '#ff6b6b' },
    { name: 'Cotton', value: 15, color: '#4ecdc4' },
    { name: 'Others', value: 20, color: '#45b7d1' }
  ]

  const statePerformanceData = [
    { state: 'Maharashtra', yield: 4.2, price: 2400, trend: 5.2 },
    { state: 'Karnataka', yield: 3.8, price: 2350, trend: 3.8 },
    { state: 'Andhra Pradesh', yield: 4.5, price: 2500, trend: 6.1 },
    { state: 'Tamil Nadu', yield: 4.0, price: 2450, trend: 4.5 },
    { state: 'Gujarat', yield: 3.6, price: 2300, trend: 2.9 },
    { state: 'Rajasthan', yield: 3.2, price: 2200, trend: 1.8 }
  ]

  const marketInsights = [
    {
      type: 'hot',
      title: 'Hot Markets',
      icon: TrendingUp,
      color: 'green',
      items: [
        'Cotton prices rising 15%',
        'Onion demand increasing',
        'Export opportunities for Rice'
      ]
    },
    {
      type: 'alert',
      title: 'Market Alerts',
      icon: AlertTriangle,
      color: 'yellow',
      items: [
        'Monsoon affecting Wheat',
        'Storage issues with Potato',
        'Transportation costs up 8%'
      ]
    },
    {
      type: 'event',
      title: 'Upcoming Events',
      icon: Calendar,
      color: 'blue',
      items: [
        'Harvest season begins Oct',
        'New MSP announcement',
        'Agricultural expo next month'
      ]
    }
  ]

  const crops = [
    { value: 'Rice', label: 'Rice' },
    { value: 'Wheat', label: 'Wheat' },
    { value: 'Maize', label: 'Maize' },
    { value: 'Cotton', label: 'Cotton' },
    { value: 'Sugarcane', label: 'Sugarcane' }
  ]

  const timeRanges = [
    { value: '3months', label: '3 Months' },
    { value: '6months', label: '6 Months' },
    { value: '1year', label: '1 Year' },
    { value: '2years', label: '2 Years' }
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
          Market Analytics
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          Comprehensive market insights and trends analysis to help you make informed decisions.
        </p>
      </motion.div>

      {/* Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Crop
              </label>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="select-field"
              >
                {crops.map(crop => (
                  <option key={crop.value} value={crop.value}>
                    {crop.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Time Range
              </label>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="select-field"
              >
                {timeRanges.map(range => (
                  <option key={range.value} value={range.value}>
                    {range.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-6"
      >
        <MetricCard
          title="Average Price"
          value="₹2,450"
          subtitle="Per quintal"
          icon={DollarSign}
          color="primary"
          trend={5.2}
        />
        <MetricCard
          title="Market Growth"
          value="+12.5%"
          subtitle="This quarter"
          icon={TrendingUp}
          color="green"
          trend={12.5}
        />
        <MetricCard
          title="Active Markets"
          value="47"
          subtitle="Across India"
          icon={Globe}
          color="secondary"
        />
        <MetricCard
          title="Price Volatility"
          value="8.3%"
          subtitle="Current level"
          icon={BarChart3}
          color="accent"
        />
      </motion.div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Price Trends */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Price Trends</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceTrendsData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} tickFormatter={(value) => `₹${value}`} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                    formatter={(value, name) => [`₹${value}`, name]}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="Rice" stroke="#667eea" strokeWidth={3} />
                  <Line type="monotone" dataKey="Wheat" stroke="#764ba2" strokeWidth={3} />
                  <Line type="monotone" dataKey="Maize" stroke="#ff6b6b" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </motion.div>

        {/* Crop Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Crop Area Distribution</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={cropDistributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={120}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {cropDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                    formatter={(value, name) => [`${value}%`, name]}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </motion.div>
      </div>

      {/* State Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        <Card>
          <h3 className="text-xl font-bold text-gray-900 mb-4">State Performance</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={statePerformanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="state" stroke="#666" fontSize={12} />
                <YAxis stroke="#666" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'white',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Legend />
                <Bar dataKey="yield" fill="#667eea" name="Yield (T/Ha)" />
                <Bar dataKey="trend" fill="#764ba2" name="Growth %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </motion.div>

      {/* Market Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Market Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {marketInsights.map((insight, index) => (
            <motion.div
              key={insight.type}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.7 + index * 0.1 }}
            >
              <Card>
                <div className="flex items-center space-x-3 mb-4">
                  <div className={`p-2 rounded-lg ${
                    insight.color === 'green' ? 'bg-green-100' :
                    insight.color === 'yellow' ? 'bg-yellow-100' :
                    'bg-blue-100'
                  }`}>
                    <insight.icon className={`h-6 w-6 ${
                      insight.color === 'green' ? 'text-green-600' :
                      insight.color === 'yellow' ? 'text-yellow-600' :
                      'text-blue-600'
                    }`} />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {insight.title}
                  </h3>
                </div>
                <ul className="space-y-2">
                  {insight.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-start space-x-2 text-sm">
                      <div className={`w-2 h-2 rounded-full mt-2 ${
                        insight.color === 'green' ? 'bg-green-500' :
                        insight.color === 'yellow' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`}></div>
                      <span className="text-gray-700">{item}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Market Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
      >
        <Card>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Market Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Positive Indicators</h4>
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-green-700">
                  <CheckCircle className="h-4 w-4" />
                  <span className="text-sm">Strong demand for staple crops</span>
                </div>
                <div className="flex items-center space-x-2 text-green-700">
                  <CheckCircle className="h-4 w-4" />
                  <span className="text-sm">Export opportunities increasing</span>
                </div>
                <div className="flex items-center space-x-2 text-green-700">
                  <CheckCircle className="h-4 w-4" />
                  <span className="text-sm">Government support programs active</span>
                </div>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Areas of Concern</h4>
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-yellow-700">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="text-sm">Weather variability affecting yields</span>
                </div>
                <div className="flex items-center space-x-2 text-yellow-700">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="text-sm">Transportation costs rising</span>
                </div>
                <div className="flex items-center space-x-2 text-yellow-700">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="text-sm">Storage infrastructure needs improvement</span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
      </div>
    </PageTransition>
  )
}

export default MarketAnalytics