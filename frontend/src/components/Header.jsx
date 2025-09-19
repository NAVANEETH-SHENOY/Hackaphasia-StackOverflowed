import React from 'react'
import { Menu, Wheat } from 'lucide-react'

const Header = ({ onMenuClick }) => {
  return (
    <header className="bg-white/95 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Mobile menu button */}
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            aria-label="Open menu"
          >
            <Menu className="h-5 w-5 text-gray-600" />
          </button>

          {/* Logo and title */}
          <div className="flex-shrink-0 flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-tr from-primary-500 via-primary-400 to-secondary-500 rounded-xl shadow-glow-sm animate-pulse-subtle">
              <Wheat className="h-5 w-5 text-white transform -rotate-12" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold gradient-text tracking-tight">AgriTech</h1>
              <p className="text-xs font-medium text-gray-500">Smart Farming Solutions</p>
            </div>
          </div>

          {/* Desktop navigation */}
          <nav className="hidden lg:flex lg:items-center lg:space-x-8">
            {[
              ['Dashboard', '/'],
              ['Price Forecast', '/price-forecast'],
              ['Recommendations', '/crop-recommendations'],
              ['Analytics', '/market-analytics'],
            ].map(([name, href]) => (
              <a
                key={name}
                href={href}
                className="group relative px-3 py-2 text-sm font-medium text-gray-600 hover:text-primary-600 transition-colors"
              >
                {name}
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-primary-500 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
              </a>
            ))}
          </nav>

          {/* User actions */}
          <div className="flex items-center space-x-6">
            <div className="hidden sm:flex items-center space-x-2">
              <div className="flex space-x-1 items-center px-3 py-1.5 bg-success-50 text-success-600 rounded-full text-xs font-medium">
                <div className="w-1.5 h-1.5 bg-success-500 rounded-full animate-pulse"></div>
                <span>API Active</span>
              </div>
            </div>
            <button className="btn-primary text-sm group">
              Get Started
              <svg
                className="ml-2 -mr-1 w-4 h-4 transform transition-transform group-hover:translate-x-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
