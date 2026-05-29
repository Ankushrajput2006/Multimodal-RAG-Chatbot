"""Multilingual support module."""
import logging
from typing import Optional, Dict
from langdetect import detect, detect_langs
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


class MultilingualHandler:
    """Handle multilingual text processing."""

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "Chinese",
        "ja": "Japanese",
        "ar": "Arabic",
        "pt": "Portuguese",
        "ru": "Russian",
        "ko": "Korean"
    }

    def __init__(self, default_language: str = "en"):
        """Initialize multilingual handler.
        
        Args:
            default_language: Default language code
        """
        self.default_language = default_language

    def detect_language(self, text: str) -> Dict[str, any]:
        """Detect language of text.
        
        Args:
            text: Text to detect language
            
        Returns:
            Dictionary with language info
        """
        try:
            lang_code = detect(text)
            probabilities = detect_langs(text)
            
            return {
                "language_code": lang_code,
                "language_name": self.SUPPORTED_LANGUAGES.get(lang_code, "Unknown"),
                "confidence": max(p.prob for p in probabilities),
                "probabilities": {p.lang: p.prob for p in probabilities}
            }
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return {
                "language_code": self.default_language,
                "language_name": self.SUPPORTED_LANGUAGES.get(self.default_language),
                "confidence": 0.0
            }

    def translate(self, text: str, source_lang: Optional[str] = None, target_lang: str = "en") -> str:
        """Translate text to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (auto-detect if None)
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        try:
            if source_lang is None:
                detection = self.detect_language(text)
                source_lang = detection["language_code"]
            
            if source_lang == target_lang:
                return text
            
            # Map language codes if needed
            source_lang = self._map_language_code(source_lang)
            target_lang = self._map_language_code(target_lang)
            
            translator = GoogleTranslator(source_language=source_lang, target_language=target_lang)
            translated = translator.translate(text)
            
            logger.info(f"Translated text from {source_lang} to {target_lang}")
            return translated
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return text

    def _map_language_code(self, lang_code: str) -> str:
        """Map language code to translator compatible format.
        
        Args:
            lang_code: Language code
            
        Returns:
            Mapped language code
        """
        # Map some common codes
        mapping = {
            "zh": "zh-CN",  # Chinese simplified
            "pt": "pt-BR"   # Portuguese Brazilian
        }
        return mapping.get(lang_code, lang_code)

    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages.
        
        Returns:
            Dictionary of language codes and names
        """
        return self.SUPPORTED_LANGUAGES.copy()

    def process_multilingual_query(self, query: str, target_language: str = "en") -> Dict:
        """Process multilingual query.
        
        Args:
            query: Query in any language
            target_language: Target language for processing
            
        Returns:
            Dictionary with language info and translated query
        """
        detection = self.detect_language(query)
        translated_query = self.translate(query, source_lang=detection["language_code"], target_lang=target_language)
        
        return {
            "original_query": query,
            "original_language": detection,
            "translated_query": translated_query,
            "target_language": target_language
        }
