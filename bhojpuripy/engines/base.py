"""Base engine interface for Bhojpuri translators."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseEngine(ABC):
    """Abstract base class that all translation engines must implement."""

    @abstractmethod
    def translate(
        self,
        text: str,
        src_lang: str = "auto",
        dialect: str = "standard",
        honorific: str = "familiar",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Translates text to Bhojpuri.

        Args:
            text: Input string.
            src_lang: Source language code (e.g., 'en', 'hi', 'es').
            dialect: Bhojpuri dialect ('standard', 'western', 'northern').
            honorific: Tone level ('informal', 'familiar', 'formal').

        Returns:
            Dict containing 'translated_text', 'detected_lang', 'engine', etc.
        """
        pass
