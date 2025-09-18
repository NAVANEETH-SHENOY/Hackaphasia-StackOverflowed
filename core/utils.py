"""
Utility functions for Karnataka Crop Demand Forecasting Platform
"""

def translate_to_kannada(text: str) -> str:
    """Translate common agricultural terms to Kannada"""
    translations = {
        "sowing": "ಬಿತ್ತನೆ",
        "harvest": "ಕೊಯ್ಲು",
        "profit": "ಲಾಭ",
        "loss": "ನಷ್ಟ",
        "acre": "ಎಕರೆ",
        "hectare": "ಹೆಕ್ಟೇರ್",
        "quintal": "ಕ್ವಿಂಟಾಲ್",
        "kg": "ಕೆಜಿ",
        "price": "ಬೆಲೆ",
        "yield": "ಉತ್ಪಾದನೆ",
        "cost": "ವೆಚ್ಚ",
        "season": "ಋತು",
        "kharif": "ಖರೀಫ್",
        "rabi": "ರಬಿ",
        "summer": "ಬೇಸಿಗೆ"
    }
    
    for english, kannada in translations.items():
        text = text.replace(english, f"{english} ({kannada})")
    
    return text

def format_currency(amount: float) -> str:
    """Format currency in Indian Rupees"""
    return f"₹{amount:,.0f}"

def calculate_season(month: int) -> str:
    """Calculate season based on month"""
    if month in [6, 7, 8, 9, 10]:
        return "kharif"
    elif month in [11, 12, 1, 2, 3]:
        return "rabi"
    else:
        return "summer"

def get_month_name(month: int) -> str:
    """Get month name"""
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[month - 1] if 1 <= month <= 12 else "Invalid"

def get_kannada_month_name(month: int) -> str:
    """Get Kannada month name"""
    kannada_months = [
        "ಜನವರಿ", "ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್", "ಏಪ್ರಿಲ್", "ಮೇ", "ಜೂನ್",
        "ಜುಲೈ", "ಆಗಸ್ಟ್", "ಸೆಪ್ಟೆಂಬರ್", "ಅಕ್ಟೋಬರ್", "ನವೆಂಬರ್", "ಡಿಸೆಂಬರ್"
    ]
    return kannada_months[month - 1] if 1 <= month <= 12 else "ಅಮಾನ್ಯ"
