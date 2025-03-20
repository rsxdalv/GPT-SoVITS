import json
import os
from typing import List, Dict, Any, Optional
from ...src.common_config_manager import app_config

# Default locale path
default_locale_path = "i18n/locale"

class I18nAuto:
    """
    I18nAuto class for handling internationalization
    """
    def __init__(self, language: str = "auto", locale_path: str = default_locale_path):
        """
        Initialize I18nAuto

        Args:
            language (str): Language code (e.g., "en", "zh", "auto")
            locale_path (str): Path to locale files
        """
        self.language = language
        self.locale_path = locale_path
        self.locale_dict = {}
        
        # If language is auto, try to get from app_config
        if language == "auto":
            self.language = app_config.locale
        
        # Load locale file
        self.load_locale()
        
    def load_locale(self):
        """
        Load locale file based on language
        """
        # Get absolute path
        abs_locale_path = os.path.join(os.getcwd(), self.locale_path)
        
        # Get locale file path
        locale_file = os.path.join(abs_locale_path, f"{self.language}.json")
        
        # Check if locale file exists
        if not os.path.exists(locale_file):
            # If not exists, try to find similar locale file
            similar_locale_file = self.find_similar_locale_file(abs_locale_path)
            if similar_locale_file is not None:
                locale_file = similar_locale_file
            else:
                # If no similar locale file found, use English
                locale_file = os.path.join(abs_locale_path, "en_US.json")
        
        # Load locale file
        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                self.locale_dict = json.load(f)
        except:
            print(f"Failed to load locale file: {locale_file}")
            self.locale_dict = {}
            
    def find_similar_locale_file(self, locale_path: str) -> Optional[str]:
        """
        Find similar locale file

        Args:
            locale_path (str): Path to locale files

        Returns:
            Optional[str]: Path to similar locale file
        """
        # Get language code (e.g., "en" from "en-US")
        lang_code = self.language.split("_")[0].lower()
        
        # List all locale files
        locale_files = os.listdir(locale_path)
        
        # Find similar locale file
        for locale_file in locale_files:
            if locale_file.lower().startswith(lang_code):
                return os.path.join(locale_path, locale_file)
        
        return None
    
    def __call__(self, text: str) -> str:
        """
        Get localized text

        Args:
            text (str): Text to be localized

        Returns:
            str: Localized text
        """
        # Try to get localized text from locale file
        localized_text = self.locale_dict.get(text)
        
        # If not found, return original text
        if localized_text is None:
            return text
        
        return localized_text
