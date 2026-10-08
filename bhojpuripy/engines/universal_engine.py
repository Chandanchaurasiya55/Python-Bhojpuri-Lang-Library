"""Universal translation engine supporting any language to Bhojpuri."""

import json
import urllib.parse
import urllib.request
import re
from typing import Dict, Any, Optional
from bhojpuripy.engines.base import BaseEngine
from bhojpuripy.engines.rule_engine import RuleBasedEngine

class UniversalEngine(BaseEngine):
    """
    Universal Multilingual Engine.
    Converts text from ANY language (English, Spanish, French, Bengali, etc.)
    into Bhojpuri via a two-stage pipeline:
    1. Source Lang -> Intermediate Hindi / Indic semantic representation
    2. Hindi -> Bhojpuri Morphological Rule & Dialect Engine
    """

    def __init__(self):
        self.rule_engine = RuleBasedEngine()

    def _is_devanagari(self, text: str) -> bool:
        devanagari_count = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        total_letters = sum(1 for c in text if c.isalpha())
        if total_letters == 0:
            return False
        return (devanagari_count / total_letters) > 0.4

    def _bridge_translate_to_hindi(self, text: str, src_lang: str = "auto") -> tuple[str, str]:
        """
        Translates foreign text to Hindi using lightweight HTTP web bridge.
        Returns: (hindi_text, detected_lang)
        """
        # Endpoint 1: Google public web translate endpoint
        try:
            sl = "auto" if src_lang == "auto" else src_lang
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl=hi&dt=t&q={urllib.parse.quote(text)}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                translated_segments = []
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    for segment in data[0]:
                        if isinstance(segment, list) and len(segment) > 0:
                            translated_segments.append(segment[0])
                detected = data[2] if len(data) > 2 and isinstance(data[2], str) else src_lang
                hindi_res = "".join(translated_segments)
                if hindi_res.strip():
                    return hindi_res, detected
        except Exception:
            pass

        # Endpoint 2: MyMemory API Fallback
        try:
            sl = "en" if src_lang == "auto" else src_lang
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={sl}|hi"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "BhojpuriPyTranslator/1.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "responseData" in res_data and "translatedText" in res_data["responseData"]:
                    return res_data["responseData"]["translatedText"], sl
        except Exception:
            pass

        # If both network calls fail or offline: return original text
        return text, src_lang

    def translate(
        self,
        text: str,
        src_lang: str = "auto",
        dialect: str = "standard",
        honorific: str = "familiar",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Translates text from any language into Bhojpuri.
        """
        text = text.strip()
        if not text:
            return {
                "translated_text": "",
                "detected_lang": src_lang,
                "engine": "universal",
                "intermediate_hindi": "",
                "dialect": dialect
            }

        detected_lang = src_lang

        # If the input is already in Devanagari script (Hindi/Bhojpuri/Maithili)
        if self._is_devanagari(text) or src_lang == "hi":
            detected_lang = "hi"
            bhojpuri_res = self.rule_engine.translate(
                text=text,
                src_lang="hi",
                dialect=dialect,
                honorific=honorific
            )
            return {
                "translated_text": bhojpuri_res["translated_text"],
                "detected_lang": "hi",
                "engine": "universal_direct",
                "intermediate_hindi": text,
                "dialect": dialect
            }

        # Otherwise: translate to Hindi first, then to Bhojpuri
        hindi_text, detected_lang = self._bridge_translate_to_hindi(text, src_lang)

        # Convert Hindi to Bhojpuri
        bhojpuri_res = self.rule_engine.translate(
            text=hindi_text,
            src_lang="hi",
            dialect=dialect,
            honorific=honorific
        )

        return {
            "translated_text": bhojpuri_res["translated_text"],
            "detected_lang": detected_lang,
            "engine": "universal_pipeline",
            "intermediate_hindi": hindi_text,
            "dialect": dialect
        }
