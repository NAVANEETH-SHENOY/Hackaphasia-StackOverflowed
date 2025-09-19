import React from 'react'
import { Menu, Wheat } from 'lucide-react'

const Header = ({ onMenuClick }) => {
  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Mobile menu button */}
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <Menu className="h-6 w-6 text-gray-600" />
          </button>

          {/* Logo and title */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl">
              <Wheat className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">AgriTech</h1>
              <p className="text-sm text-gray-600">Smart Farming Solutions</p>
            </div>
          </div>

          {/* Desktop navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <a href="/" className="text-gray-600 hover:text-primary-600 transition-colors">
              Dashboard
            </a>
            <a href="/price-forecast" className="text-gray-600 hover:text-primary-600 transition-colors">
              Price Forecast
            </a>
            <a href="/crop-recommendations" className="text-gray-600 hover:text-primary-600 transition-colors">
              Recommendations
            </a>
            <a href="/market-analytics" className="text-gray-600 hover:text-primary-600 transition-colors">
              Analytics
            </a>
          </nav>

          {/* User actions */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>API Connected</span>
            </div>
            <button className="btn-primary text-sm">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
