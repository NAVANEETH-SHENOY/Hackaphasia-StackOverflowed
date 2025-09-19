import React from 'react'
import { motion } from 'framer-motion'

const Loader = ({ 
  size = 'md', 
  variant = 'primary',
  center = false,
  text,
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12'
  }

  const variantClasses = {
    primary: 'text-primary-500',
    secondary: 'text-secondary-500',
    white: 'text-white',
    gray: 'text-gray-400'
  }

  const containerClasses = center ? 'flex flex-col items-center justify-center' : 'inline-flex items-center'

  return (
    <div className={`${containerClasses} ${className}`}>
      <motion.div
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
        className={`${sizeClasses[size]} ${variantClasses[variant]}`}
      >
        <svg
          className="w-full h-full"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 6C8.68629 6 6 8.68629 6 12C6 15.3137 8.68629 18 12 18C15.3137 18 18 15.3137 18 12">
            <animateTransform
              attributeName="transform"
              attributeType="XML"
              type="rotate"
              dur="1s"
              from="0 12 12"
              to="360 12 12"
              repeatCount="indefinite"
            />
          </path>
        </svg>
      </motion.div>
      {text && (
        <span className={`ml-3 text-sm font-medium ${variantClasses[variant]}`}>
          {text}
        </span>
      )}
    </div>
  )
}

export default Loader