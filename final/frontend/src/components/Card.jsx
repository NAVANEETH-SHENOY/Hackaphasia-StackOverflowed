import React from 'react'
import { motion } from 'framer-motion'

const Card = ({ 
  children, 
  className = '', 
  hover = true, 
  padding = 'p-6',
  ...props 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`
        glass-card rounded-xl ${padding} ${className}
        ${hover ? 'hover:shadow-2xl hover:-translate-y-1' : ''}
        transition-all duration-300
      `}
      {...props}
    >
      {children}
    </motion.div>
  )
}

export default Card






