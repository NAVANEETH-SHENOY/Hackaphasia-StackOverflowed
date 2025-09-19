import React from 'react'
import { motion } from 'framer-motion'
import { 
  Target, 
  BarChart3, 
  Users, 
  Heart,
  Wheat,
  TrendingUp,
  Sprout,
  Globe,
  Shield,
  Smartphone,
  Award,
  CheckCircle
} from 'lucide-react'
import Card from '../components/Card'

const About = () => {
  const features = [
    {
      icon: TrendingUp,
      title: 'AI-Powered Price Forecasting',
      description: '15-day price predictions using advanced XGBoost models with 85%+ accuracy',
      color: 'primary'
    },
    {
      icon: Sprout,
      title: 'Smart Crop Recommendations',
      description: 'Location and season-based crop suggestions using comprehensive data analysis',
      color: 'secondary'
    },
    {
      icon: BarChart3,
      title: 'Market Analytics',
      description: 'Comprehensive market trends and insights for informed decision making',
      color: 'accent'
    },
    {
      icon: Users,
      title: 'User-Friendly Interface',
      description: 'Intuitive design accessible to farmers of all technical backgrounds',
      color: 'green'
    }
  ]

  const techStack = [
    { name: 'Machine Learning', items: ['XGBoost', 'scikit-learn', 'Pandas', 'NumPy'] },
    { name: 'Backend', items: ['Flask', 'REST API', 'CORS', 'Joblib'] },
    { name: 'Frontend', items: ['React', 'Tailwind CSS', 'Recharts', 'Framer Motion'] },
    { name: 'Data Sources', items: ['Agmarknet', 'Agricultural datasets', 'Weather APIs', 'Market data'] }
  ]

  const stats = [
    { label: 'Supported Crops', value: '10+', icon: Wheat },
    { label: 'Indian States', value: '8+', icon: Globe },
    { label: 'API Accuracy', value: '85%+', icon: Award },
    { label: 'Active Users', value: '1,250+', icon: Users }
  ]

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <h1 className="text-5xl font-bold gradient-text mb-6">
          About AgriTech
        </h1>
        <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
          AgriTech is designed to empower farmers with cutting-edge AI technology for making 
          informed decisions about crop pricing and cultivation strategies. We bridge the gap 
          between traditional farming and modern data analytics.
        </p>
      </motion.div>

      {/* Mission */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <div className="text-center">
            <Target className="h-16 w-16 text-primary-600 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              To democratize access to agricultural intelligence and help farmers make 
              data-driven decisions that improve yields, reduce risks, and increase profitability. 
              We believe every farmer deserves access to the same level of technology that 
              large agricultural corporations use.
            </p>
          </div>
        </Card>
      </motion.div>

      {/* Features */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
            >
              <Card className="h-full">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${
                    feature.color === 'primary' ? 'from-primary-500 to-primary-600' :
                    feature.color === 'secondary' ? 'from-secondary-500 to-secondary-600' :
                    feature.color === 'accent' ? 'from-accent-500 to-accent-600' :
                    'from-green-500 to-green-600'
                  } text-white`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">By the Numbers</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
            >
              <Card className="text-center">
                <stat.icon className="h-12 w-12 text-primary-600 mx-auto mb-4" />
                <div className="text-3xl font-bold text-gray-900 mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-600 font-medium">
                  {stat.label}
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Technology Stack */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {techStack.map((category, index) => (
            <motion.div
              key={category.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.7 + index * 0.1 }}
            >
              <Card>
                <h3 className="text-lg font-bold text-gray-900 mb-4 text-center">
                  {category.name}
                </h3>
                <ul className="space-y-2">
                  {category.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-center space-x-2 text-sm">
                      <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                      <span className="text-gray-700">{item}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* How to Use */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
      >
        <Card>
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">How to Use AgriTech</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Price Forecasting</h3>
              <p className="text-gray-600">
                Select your crop and get 15-day price predictions to optimize your selling strategy.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-secondary-500 to-secondary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Crop Recommendations</h3>
              <p className="text-gray-600">
                Enter your location and get personalized crop suggestions based on season and market conditions.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-accent-500 to-accent-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Market Analytics</h3>
              <p className="text-gray-600">
                Explore market trends and insights to make informed decisions about your farming business.
              </p>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Data Sources */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.9 }}
      >
        <Card>
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Data Sources</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Primary Sources</h3>
              <ul className="space-y-3">
                <li className="flex items-center space-x-3">
                  <Shield className="h-5 w-5 text-primary-600" />
                  <span className="text-gray-700">Agmarknet Price Data - Ministry of Agriculture</span>
                </li>
                <li className="flex items-center space-x-3">
                  <Shield className="h-5 w-5 text-primary-600" />
                  <span className="text-gray-700">Crop Yield Statistics - Government datasets</span>
                </li>
                <li className="flex items-center space-x-3">
                  <Shield className="h-5 w-5 text-primary-600" />
                  <span className="text-gray-700">Weather and Rainfall Data - IMD</span>
                </li>
                <li className="flex items-center space-x-3">
                  <Shield className="h-5 w-5 text-primary-600" />
                  <span className="text-gray-700">Market Demand Indicators - Industry reports</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Quality Assurance</h3>
              <ul className="space-y-3">
                <li className="flex items-center space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-gray-700">Real-time data validation</span>
                </li>
                <li className="flex items-center space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-gray-700">Automated quality checks</span>
                </li>
                <li className="flex items-center space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-gray-700">Regular data updates</span>
                </li>
                <li className="flex items-center space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-gray-700">Cross-validation with multiple sources</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Support */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.0 }}
      >
        <Card>
          <div className="text-center">
            <Heart className="h-16 w-16 text-red-500 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Support & Community</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto mb-8">
              We&apos;re committed to supporting farmers with comprehensive resources, 
              technical assistance, and a growing community of agricultural innovators.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <Smartphone className="h-12 w-12 text-primary-600 mx-auto mb-3" />
                <h3 className="font-bold text-gray-900 mb-2">Mobile Support</h3>
                <p className="text-sm text-gray-600">
                  Access AgriTech on any device with our responsive design
                </p>
              </div>
              <div className="text-center">
                <Users className="h-12 w-12 text-secondary-600 mx-auto mb-3" />
                <h3 className="font-bold text-gray-900 mb-2">Community</h3>
                <p className="text-sm text-gray-600">
                  Join our growing community of farmers and agricultural experts
                </p>
              </div>
              <div className="text-center">
                <Award className="h-12 w-12 text-accent-600 mx-auto mb-3" />
                <h3 className="font-bold text-gray-900 mb-2">Recognition</h3>
                <p className="text-sm text-gray-600">
                  Built for AgriTech Hackathon 2024 - Award-winning solution
                </p>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.1 }}
        className="text-center py-8"
      >
        <div className="flex items-center justify-center space-x-2 mb-4">
          <Wheat className="h-8 w-8 text-primary-600" />
          <span className="text-2xl font-bold gradient-text">AgriTech</span>
        </div>
        <p className="text-gray-600 mb-4">
          Empowering Agriculture Through Artificial Intelligence
        </p>
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
          <span>Made with</span>
          <Heart className="h-4 w-4 text-red-500" />
          <span>for Indian Farmers</span>
        </div>
      </motion.div>
    </div>
  )
}

export default About
