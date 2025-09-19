import React from 'react'
import { motion } from 'framer-motion'

const MetricCard = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend, 
  color = 'primary',
  loading = false,
  className = '' 
}) => {
  const colorClasses = {
    primary: 'from-primary-500 to-primary-600',
    secondary: 'from-secondary-500 to-secondary-600',
    accent: 'from-accent-500 to-accent-600',
    success: 'from-success-500 to-success-600',
    warning: 'from-warning-500 to-warning-600',
    error: 'from-error-500 to-error-600'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        duration: 0.5,
        ease: [0.4, 0, 0.2, 1]
      }}
      className={`metric-card group ${loading ? 'animate-pulse' : ''} ${className}`}
      whileHover={{ y: -4 }}
    >
      <div className="flex items-start justify-between mb-4">
        {Icon && (
          <div className={`p-3 rounded-lg bg-gradient-to-r ${colorClasses[color]} text-white
            transition-transform duration-300 group-hover:scale-110`}>
            <Icon className="h-6 w-6" />
          </div>
        )}
        {trend !== undefined && (
          <div className={`flex items-center space-x-1 text-sm font-medium ${
            trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-600' : 'text-gray-600'
          }`}>
            <span>
              {trend > 0 ? '↑' : trend < 0 ? '↓' : '●'} {Math.abs(trend)}%
            </span>
          </div>
        )}
      </div>
      
      <div className="space-y-1">
        {loading ? (
          <>
            <div className="h-8 w-2/3 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-4 w-1/2 bg-gray-100 rounded animate-pulse"></div>
          </>
        ) : (
          <>
            <h3 className="text-2xl font-bold text-gray-900 tracking-tight">
              {value}
            </h3>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            {subtitle && (
              <p className="text-xs text-gray-500">{subtitle}</p>
            )}
          </>
        )}
      </div>
      
      {/* Hover effect decoration */}
      <div className="absolute inset-0 rounded-2xl transition-opacity duration-300 opacity-0 group-hover:opacity-100">
        <div className="absolute inset-x-0 h-px bottom-0 bg-gradient-to-r from-transparent via-primary-500 to-transparent"></div>
      </div>
    </motion.div>
  )
}

export default MetricCard






