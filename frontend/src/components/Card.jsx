import React from 'react'
import { motion } from 'framer-motion'

const Card = ({ 
  children, 
  className = '', 
  variant = 'default',
  hover = true, 
  loading = false,
  padding = 'p-6',
  title,
  subtitle,
  action,
  ...props 
}) => {
  const variants = {
    default: 'bg-white border border-gray-100',
    glass: 'glass-card',
    colored: 'bg-gradient-to-br from-primary-500/5 to-secondary-500/5 border border-primary-100',
    outline: 'border-2 border-gray-200 bg-white/50'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        duration: 0.5,
        ease: [0.4, 0, 0.2, 1]
      }}
      className={`
        rounded-2xl ${variants[variant]} ${padding} ${className}
        ${hover ? 'transform-gpu transition-all duration-300 hover:shadow-lg hover:-translate-y-1 hover:ring-4 hover:ring-primary-500/10' : ''}
        ${loading ? 'animate-pulse' : ''}
        relative overflow-hidden
      `}
      {...props}
    >
      {loading ? (
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
            <div className="h-3 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      ) : (
        <>
          {(title || subtitle || action) && (
            <div className="flex items-start justify-between mb-4">
              <div className="space-y-1">
                {title && (
                  <h3 className="text-lg font-semibold text-gray-900">
                    {title}
                  </h3>
                )}
                {subtitle && (
                  <p className="text-sm text-gray-500">
                    {subtitle}
                  </p>
                )}
              </div>
              {action && (
                <div className="ml-4">
                  {action}
                </div>
              )}
            </div>
          )}
          {children}
        </>
      )}
      
      {/* Decorative corner gradients */}
      {variant === 'default' && (
        <>
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-primary-500/5 to-transparent transform rotate-12 -translate-y-16 translate-x-16"></div>
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-gradient-to-tr from-secondary-500/5 to-transparent transform -rotate-12 translate-y-16 -translate-x-16"></div>
        </>
      )}
    </motion.div>
  )
}

export default Card






