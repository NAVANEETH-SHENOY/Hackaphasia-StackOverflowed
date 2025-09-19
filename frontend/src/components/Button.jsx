import React from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  disabled = false,
  icon: Icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  ...props 
}) => {
  const baseClasses = `
    inline-flex items-center justify-center font-medium rounded-lg
    transition-all duration-200 transform-gpu
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none
    active:scale-95
  `
  
  const variants = {
    primary: `
      bg-primary-500 hover:bg-primary-600 text-white 
      focus:ring-primary-500 shadow-sm hover:shadow-md
      hover:-translate-y-0.5
    `,
    secondary: `
      bg-secondary-500 hover:bg-secondary-600 text-white 
      focus:ring-secondary-500 shadow-sm hover:shadow-md
      hover:-translate-y-0.5
    `,
    success: `
      bg-success-500 hover:bg-success-600 text-white 
      focus:ring-success-500 shadow-sm hover:shadow-md
      hover:-translate-y-0.5
    `,
    warning: `
      bg-warning-500 hover:bg-warning-600 text-white 
      focus:ring-warning-500 shadow-sm hover:shadow-md
      hover:-translate-y-0.5
    `,
    soft: `
      bg-primary-50 hover:bg-primary-100 text-primary-700
      focus:ring-primary-500 hover:-translate-y-0.5
    `,
    outline: `
      border-2 border-gray-300 hover:border-primary-500 
      text-gray-700 hover:text-primary-600 bg-white
      hover:bg-primary-50 focus:ring-primary-500
      hover:-translate-y-0.5
    `,
    ghost: `
      text-gray-600 hover:text-gray-900 hover:bg-gray-100 
      focus:ring-gray-500 hover:-translate-y-0.5
    `,
    link: `
      text-primary-600 hover:text-primary-700 underline-offset-4
      hover:underline focus:ring-primary-500
    `,
  }
  
  const sizes = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-4 text-lg',
  }

  return (
    <motion.button
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.95 }}
      className={`
        ${baseClasses} 
        ${variants[variant]} 
        ${sizes[size]} 
        ${fullWidth ? 'w-full' : ''} 
        ${className}
      `}
      disabled={disabled || loading}
      {...props}
    >
      {/* Loading State */}
      {loading && (
        <>
          <Loader2 className={`
            h-4 w-4 animate-spin
            ${children ? 'mr-2' : ''}
          `} />
          {children && <span className="animate-pulse">{children}</span>}
        </>
      )}
      
      {/* Normal State */}
      {!loading && (
        <>
          {Icon && iconPosition === 'left' && (
            <Icon className={`h-4 w-4 ${children ? 'mr-2' : ''}`} />
          )}
          {children}
          {Icon && iconPosition === 'right' && (
            <Icon className={`h-4 w-4 ${children ? 'ml-2' : ''}`} />
          )}
        </>
      )}
      
      {/* Interactive gradient background effect */}
      {variant === 'primary' && (
        <div className="absolute inset-0 rounded-lg overflow-hidden pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-r from-primary-400/0 via-primary-400/10 to-primary-400/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        </div>
      )}
    </motion.button>
  )
}

export default Button






