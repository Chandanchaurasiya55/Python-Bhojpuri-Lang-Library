"""Main BhojpuriTranslator client interface."""

import os
import json
from typing import Optional, Dict, Any, List

try:
    from .engines.rule_engine import RuleBasedEngine
    from .engines.universal_engine import UniversalEngine
    from .engines.llm_engine import LLMEngine
    from .engines.nllb_engine import NLLBEngine
    from .transliterate import devanagari_to_roman
    from .constants import SUPPORTED_LANGUAGES, DIALECTS, HONORIFICS
except (ImportError, ValueError):
    from bhojpuripy.engines.rule_engine import RuleBasedEngine
    from bhojpuripy.engines.universal_engine import UniversalEngine
    from bhojpuripy.engines.llm_engine import LLMEngine
    from bhojpuripy.engines.nllb_engine import NLLBEngine
    from bhojpuripy.transliterate import devanagari_to_roman
    from bhojpuripy.constants import SUPPORTED_LANGUAGES, DIALECTS, HONORIFICS

class BhojpuriTranslator:
    """
    High-level Bhojpuri translation client supporting multiple engines:
    - 'hybrid' / 'universal': Works from ANY language (English, Spanish, Hindi, etc.)
    - 'rule_based': Zero-latency offline engine for Hindi -> Bhojpuri
    - 'gemini': Cloud LLM for cultural nuance & idioms
    - 'nllb': Local offline Meta NLLB-200 neural network
    """

    def __init__(self, default_engine: str = "universal", api_key: Optional[str] = None):
        self.default_engine = default_engine
        self.api_key = api_key
        
        # Instantiate engines lazily or on-demand
        self._rule_engine = RuleBasedEngine()
        self._universal_engine = UniversalEngine()
        self._llm_engine = None
        self._nllb_engine = None

    def translate(
        self,
        text: str,
        src: str = "auto",
        engine: Optional[str] = None,
        dialect: str = "standard",
        honorific: str = "familiar",
        include_roman: bool = True
    ) -> Dict[str, Any]:
        """
        Translates text to Bhojpuri.

        Args:
            text: Text to translate.
            src: Source language code ('auto', 'en', 'hi', 'fr', etc.).
            engine: Engine to use ('universal', 'rule_based', 'gemini', 'nllb').
            dialect: 'standard' (Bhojpur), 'western' (Gorakhpur), 'northern' (Saran).
            honorific: 'informal' (तू), 'familiar' (तूँ), 'formal' (रउआ).
            include_roman: If True, provides Romanized/English phonetics alongside Devanagari.

        Returns:
            Dictionary with 'bhojpuri', 'roman', 'source_lang', 'detected_lang', 'engine'.
        """
        text = (text or "").strip()
        if not text:
            return {
                "bhojpuri": "",
                "roman": "",
                "source_text": "",
                "source_lang": src,
                "detected_lang": src,
                "engine": engine or self.default_engine,
                "dialect": dialect
            }

        eng_choice = (engine or self.default_engine).lower()

        # Engine Dispatch
        if eng_choice in ["rule_based", "rule"]:
            res = self._rule_engine.translate(text, src_lang=src, dialect=dialect, honorific=honorific)
        elif eng_choice in ["gemini", "llm"]:
            if self._llm_engine is None:
                self._llm_engine = LLMEngine(api_key=self.api_key)
            res = self._llm_engine.translate(text, src_lang=src, dialect=dialect, honorific=honorific)
        elif eng_choice in ["nllb", "neural"]:
            if self._nllb_engine is None:
                self._nllb_engine = NLLBEngine()
            res = self._nllb_engine.translate(text, src_lang=src, dialect=dialect, honorific=honorific)
        else:
            # Universal / Hybrid (Default)
            res = self._universal_engine.translate(text, src_lang=src, dialect=dialect, honorific=honorific)

        bhojpuri_text = res.get("translated_text", "")
        roman_text = devanagari_to_roman(bhojpuri_text) if include_roman else ""

        return {
            "bhojpuri": bhojpuri_text,
            "roman": roman_text,
            "source_text": text,
            "source_lang": src,
            "detected_lang": res.get("detected_lang", src),
            "engine": res.get("engine", eng_choice),
            "dialect": dialect,
            "intermediate_hindi": res.get("intermediate_hindi")
        }

    def to_roman(self, text: str) -> str:
        """Transliterate Devanagari Bhojpuri to Roman script."""
        return devanagari_to_roman(text)

    def get_idioms(self) -> List[Dict[str, Any]]:
        """Returns list of authentic Bhojpuri idioms and proverbs with meanings."""
        idioms_path = os.path.join(os.path.dirname(__file__), "data", "idioms.json")
        try:
            with open(idioms_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_languages(self) -> Dict[str, str]:
        """Returns dictionary of supported source languages."""
        return SUPPORTED_LANGUAGES

    def get_dialects(self) -> Dict[str, Any]:
        """Returns dictionary of available Bhojpuri dialects."""
        return DIALECTS
