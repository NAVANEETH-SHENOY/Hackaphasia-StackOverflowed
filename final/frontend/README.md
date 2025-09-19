# 🌾 AgriTech React Frontend

A modern, responsive React frontend for the AgriTech Smart Farming Solutions platform. Built with React, Tailwind CSS, and modern web technologies to provide an intuitive interface for farmers.

## ✨ Features

- **🎨 Modern UI/UX**: Beautiful, responsive design with smooth animations
- **📱 Mobile-First**: Optimized for all device sizes
- **📊 Interactive Charts**: Real-time data visualization with Recharts
- **🚀 Fast Performance**: Built with Vite for lightning-fast development and builds
- **♿ Accessible**: WCAG 2.1 AA compliant design
- **🌐 Multi-Device**: Works seamlessly on desktop, tablet, and mobile

## 🛠️ Technology Stack

- **Frontend Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Routing**: React Router DOM

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Running AgriTech Flask backend (port 5000)

### Installation

1. **Clone and navigate to the frontend directory**
   ```bash
   cd react-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 📁 Project Structure

```
react-frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Header.jsx
│   │   ├── Input.jsx
│   │   ├── MetricCard.jsx
│   │   ├── Select.jsx
│   │   └── Sidebar.jsx
│   ├── pages/             # Page components
│   │   ├── About.jsx
│   │   ├── CropRecommendations.jsx
│   │   ├── Dashboard.jsx
│   │   ├── MarketAnalytics.jsx
│   │   └── PriceForecast.jsx
│   ├── services/          # API services
│   │   └── api.js
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # App entry point
│   └── index.css          # Global styles
├── package.json
├── tailwind.config.js     # Tailwind configuration
├── vite.config.js         # Vite configuration
└── README.md
```

## 🎨 Design System

### Color Palette
- **Primary**: Deep Blue (#667eea) - Trust and reliability
- **Secondary**: Purple (#764ba2) - Innovation and technology  
- **Accent**: Orange (#ff6b6b) - Energy and optimism
- **Neutral**: Light Gray (#f8f9fa) - Clean and modern

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800

### Components
- **Cards**: Glass-morphism design with subtle shadows
- **Buttons**: Gradient backgrounds with hover effects
- **Charts**: Interactive visualizations with tooltips
- **Forms**: Clean inputs with validation states

## 📱 Pages

### Dashboard
- Welcome screen with quick actions
- API status indicator
- Key metrics overview
- Feature highlights

### Price Forecasting
- Crop selection and forecast period
- Interactive price charts
- Summary metrics and trends
- Smart recommendations

### Crop Recommendations
- Location-based recommendations
- Crop analysis mode
- Suitability scores and charts
- Detailed crop information

### Market Analytics
- Price trend analysis
- Crop distribution charts
- State performance metrics
- Market insights and alerts

### About
- Mission and features
- Technology stack
- Usage instructions
- Support information

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
VITE_API_URL=http://localhost:5000

# Development Settings
VITE_APP_TITLE=AgriTech - Smart Farming Solutions
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

### Tailwind Configuration

The project uses a custom Tailwind configuration with:
- Extended color palette
- Custom animations
- Component classes
- Responsive breakpoints

## 🚀 Deployment

### Build for Production

```bash
npm run build
# or
yarn build
```

### Preview Production Build

```bash
npm run preview
# or
yarn preview
```

### Deploy to Vercel

1. Install Vercel CLI
   ```bash
   npm i -g vercel
   ```

2. Deploy
   ```bash
   vercel
   ```

### Deploy to Netlify

1. Build the project
   ```bash
   npm run build
   ```

2. Deploy the `dist` folder to Netlify

## 🔌 API Integration

The frontend integrates with the AgriTech Flask backend through:

- **Health Check**: `GET /health`
- **Price Forecasting**: `POST /forecast-price`
- **Crop Recommendations**: `POST /recommend-crop`

### API Service

The `services/api.js` file handles all API communication with:
- Axios configuration
- Request/response interceptors
- Error handling
- TypeScript support

## 🎯 Key Features

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Touch-friendly interface
- Optimized for all screen sizes

### Performance
- Vite for fast builds
- Code splitting
- Lazy loading
- Optimized images
- Minimal bundle size

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- High contrast ratios
- Focus indicators

### User Experience
- Smooth animations
- Loading states
- Error handling
- Toast notifications
- Intuitive navigation

## 🧪 Development

### Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Dependencies
npm install          # Install dependencies
npm update           # Update dependencies
```

### Code Style

- ESLint configuration
- Prettier formatting
- Component-based architecture
- Custom hooks for state management
- TypeScript support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for AgriTech Hackathon 2024
- Designed for Indian farmers
- Powered by modern web technologies
- Inspired by agricultural innovation

---

**Made with ❤️ for Indian Farmers**






