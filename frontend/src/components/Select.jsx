import React from 'react'

const Select = ({ 
  label, 
  error, 
  helperText,
  icon: Icon,
  loading = false,
  disabled = false,
  required = false, 
  options = [],
  placeholder = 'Select an option',
  size = 'md',
  className = '',
  ...props 
}) => {
  const sizeClasses = {
    sm: 'py-1.5 text-sm',
    md: 'py-2.5 text-base',
    lg: 'py-3 text-lg'
  }

  return (
    <div className="space-y-1.5">
      {label && (
        <div className="flex items-center justify-between">
          <label className="block text-sm font-medium text-gray-700">
            {label}
            {required && <span className="ml-1 text-red-500">*</span>}
          </label>
          {loading && (
            <div className="flex items-center text-gray-400">
              <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"></div>
              <span className="text-xs">Loading...</span>
            </div>
          )}
        </div>
      )}
      <div className="relative">
        {Icon && (
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <Icon className="h-5 w-5 text-gray-400" />
          </div>
        )}
        <select
          className={`
            block w-full rounded-lg border border-gray-300 bg-white px-4
            ${sizeClasses[size]} ${Icon ? 'pl-10' : ''}
            ${error ? 'border-red-500 focus:ring-red-500' : 'focus:ring-primary-500'}
            ${disabled ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : ''}
            shadow-sm
            transition-all duration-200
            placeholder-gray-400
            focus:border-transparent focus:outline-none focus:ring-2
            disabled:opacity-75
            ${className}
          `}
          disabled={disabled || loading}
          {...props}
        >
          <option value="" disabled>
            {placeholder}
          </option>
          {options.map((option) => (
            <option 
              key={option.value} 
              value={option.value}
              disabled={option.disabled}
            >
              {option.label}
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
          <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
      {/* Error and Helper Text */}
      <div className="min-h-[20px]">
        {error ? (
          <p className="flex items-center text-sm text-red-600">
            <svg className="mr-1.5 h-4 w-4 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            {error}
          </p>
        ) : helperText ? (
          <p className="text-sm text-gray-500">{helperText}</p>
        ) : null}
      </div>
    </div>
  )
}

export default Select






