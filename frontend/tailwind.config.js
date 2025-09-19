/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eefcf4',
          100: '#d8f7e6',
          200: '#b4ecd1',
          300: '#84dcb5',
          400: '#4fc393',
          500: '#38a677',
          600: '#2c8861',
          700: '#266d4f',
          800: '#235742',
          900: '#1f4838',
        },
        secondary: {
          50: '#f7f7ff',
          100: '#eeeeff',
          200: '#deddff',
          300: '#c3c1ff',
          400: '#a19dff',
          500: '#7e78ff',
          600: '#5b54ff',
          700: '#4037f5',
          800: '#352dd3',
          900: '#2d28a8',
        },
        accent: {
          50: '#fff8f1',
          100: '#feecdc',
          200: '#fcd9b7',
          300: '#fbbc86',
          400: '#fa9454',
          500: '#f76b2f',
          600: '#e4471a',
          700: '#be3515',
          800: '#982c18',
          900: '#7c2617',
        },
        success: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
        error: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
        'scale-in': 'scaleIn 0.2s ease-out',
        'rotate-360': 'rotate360 1s linear infinite',
        'pulse-subtle': 'pulseSubtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        },
        rotate360: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' }
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.85' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        }
      },
      boxShadow: {
        'glow-sm': '0 2px 8px -1px rgba(56, 166, 119, 0.15)',
        'glow-md': '0 4px 16px -2px rgba(56, 166, 119, 0.2)',
        'glow-lg': '0 8px 24px -4px rgba(56, 166, 119, 0.25)',
        'glow-xl': '0 12px 32px -6px rgba(56, 166, 119, 0.3)',
        'card': '0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.08)'
      },
      backdropBlur: {
        'xs': '2px'
      }
      }
    },
  
  plugins: [],
}






