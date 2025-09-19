from typing import Dict, Optional, Any
import requests
import json
import os
from pathlib import Path

class TranslationService:
    def __init__(self):
        self.supported_languages = {
            'hi': 'hindi',
            'kn': 'kannada',
            'en': 'english'
        }
        self.cache = {}  # Cache for common translations
        
        # Load common translations from JSON if available
        self.load_common_translations()
        
    def load_common_translations(self):
        """
        Load common translations from JSON file
        """
        try:
            translation_file = os.path.join(os.path.dirname(__file__), 'common_translations.json')
            if os.path.exists(translation_file):
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations_cache = json.load(f)
        except Exception as e:
            print(f"Error loading translations: {str(e)}")
            
    def translate(self, text: str, target_lang: str) -> str:
        """
        Translate text to target language using common translations
        """
        if not target_lang or target_lang == 'en' or target_lang not in self.supported_languages:
            return text

        if not isinstance(text, str):
            return str(text)

        # Normalize text for lookup
        text_key = text.strip()
        
        # Check common translations
        if text_key in COMMON_TRANSLATIONS and target_lang in COMMON_TRANSLATIONS[text_key]:
            return COMMON_TRANSLATIONS[text_key][target_lang]
        
        # Return original text if no translation found
        return text
            
    def translate_response(self, response_data: Any, target_lang: str) -> Any:
        """
        Translate API response data recursively
        Args:
            response_data: Data to translate (dict, list, or primitive)
            target_lang (str): Target language code
        Returns:
            Translated data in same structure
        """
        try:
            if isinstance(response_data, dict):
                translated_data = {}
                for key, value in response_data.items():
                    # Don't translate certain fields
                    if key in ['date', 'generated_at', 'price', 'confidence_lower', 'confidence_upper', 
                              'temperature', 'humidity', 'ph', 'rainfall', 'volatility']:
                        translated_data[key] = value
                    elif isinstance(value, str):
                        translated_data[key] = self.translate(value, target_lang)
                    elif isinstance(value, (list, dict)):
                        translated_data[key] = self.translate_response(value, target_lang)
                    else:
                        translated_data[key] = value
                return translated_data
            elif isinstance(response_data, list):
                return [self.translate_response(item, target_lang) for item in response_data]
            else:
                return response_data

        except Exception as e:
            print(f"Response translation error: {e}")
            return response_data
            
    def save_translations(self):
        """
        Save cached translations to file
        """
        try:
            translation_file = os.path.join(os.path.dirname(__file__), 'common_translations.json')
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving translations: {str(e)}")
            
# Common agricultural terms translations (for faster access)
COMMON_TRANSLATIONS = {
    "Rice": {
        "hi": "चावल",
        "kn": "ಅಕ್ಕಿ"
    },
    "Wheat": {
        "hi": "गेहूं",
        "kn": "ಗೋಧಿ"
    },
    "Maize": {
        "hi": "मक्का",
        "kn": "ಮೆಕ್ಕೆಜೋಳ"
    },
    "Cotton": {
        "hi": "कपास",
        "kn": "ಹತ್ತಿ"
    },
    "Sugarcane": {
        "hi": "गन्ना",
        "kn": "ಕಬ್ಬು"
    },
    "recommendations": {
        "hi": "सिफारिशें",
        "kn": "ಶಿಫಾರಸುಗಳು"
    },
    "weather": {
        "hi": "मौसम",
        "kn": "ಹವಾಮಾನ"
    },
    "temperature": {
        "hi": "तापमान",
        "kn": "ತಾಪಮಾನ"
    },
    "humidity": {
        "hi": "आर्द्रता",
        "kn": "ಆರ್ದ್ರತೆ"
    },
    "rainfall": {
        "hi": "वर्षा",
        "kn": "ಮಳೆ"
    },
    "market_outlook": {
        "hi": "बाजार का दृष्टिकोण",
        "kn": "ಮಾರುಕಟ್ಟೆ ನೋಟ"
    },
    "price_forecast": {
        "hi": "मूल्य पूर्वानुमान",
        "kn": "ಬೆಲೆ ಮುನ್ಸೂಚನೆ"
    },
    "seasonal_pattern": {
        "hi": "मौसमी पैटर्न",
        "kn": "ಋತುಮಾನ ಮಾದರಿ"
    },
    "confidence_score": {
        "hi": "विश्वास स्कोर",
        "kn": "ವಿಶ್ವಾಸ ಅಂಕ"
    }
}