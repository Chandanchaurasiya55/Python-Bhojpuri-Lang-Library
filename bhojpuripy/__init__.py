"""
BhojpuriPy: The Open-Source Multilingual Translation Library for Bhojpuri.
Translate any language (English, Hindi, Spanish, French, etc.) into Bhojpuri.
"""

from bhojpuripy.client import BhojpuriTranslator
from bhojpuripy.transliterate import devanagari_to_roman
from bhojpuripy.constants import SUPPORTED_LANGUAGES, DIALECTS, HONORIFICS

__version__ = "1.0.0"
__author__ = "Open Source Community"

_default_client = BhojpuriTranslator()

def translate(
    text: str,
    src: str = "auto",
    engine: str = "universal",
    dialect: str = "standard",
    honorific: str = "familiar",
    include_roman: bool = True
):
    """
    Convenience function to translate text directly into Bhojpuri.
    
    Example:
        >>> import bhojpuripy as bho
        >>> bho.translate("Where are you going?")
        {'bhojpuri': 'कहाँ जात बाड़ऽ?', 'roman': 'Kahaan jaat baad?'}
    """
    return _default_client.translate(
        text=text,
        src=src,
        engine=engine,
        dialect=dialect,
        honorific=honorific,
        include_roman=include_roman
    )

def to_roman(text: str) -> str:
    """Convert Bhojpuri Devanagari text to Roman English phonetics."""
    return devanagari_to_roman(text)

def get_idioms():
    """Retrieve list of Bhojpuri idioms and sayings."""
    return _default_client.get_idioms()

def get_languages():
    """List all supported source languages."""
    return SUPPORTED_LANGUAGES

def get_dialects():
    """List available Bhojpuri dialect styles."""
    return DIALECTS

__all__ = [
    "translate",
    "to_roman",
    "get_idioms",
    "get_languages",
    "get_dialects",
    "BhojpuriTranslator",
    "__version__"
]
