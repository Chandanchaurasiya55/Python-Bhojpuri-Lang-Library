"""LLM-based translation engine supporting Google Gemini and OpenAI for authentic Bhojpuri."""

import os
import json
from typing import Dict, Any, Optional
try:
    from .base import BaseEngine
except (ImportError, ValueError):
    from bhojpuripy.engines.base import BaseEngine

class LLMEngine(BaseEngine):
    """
    LLM engine that translates text into natural Bhojpuri using Gemini or OpenAI.
    Ideal for nuanced slang, complex literature, and cultural idioms.
    """

    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider.lower()

    def translate(
        self,
        text: str,
        src_lang: str = "auto",
        dialect: str = "standard",
        honorific: str = "familiar",
        **kwargs
    ) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "translated_text": text,
                "error": "No API key found. Please set GEMINI_API_KEY or OPENAI_API_KEY environment variable.",
                "detected_lang": src_lang,
                "engine": f"llm_{self.provider}"
            }

        prompt = (
            f"You are a native Bhojpuri linguist from Bihar and Eastern UP. "
            f"Translate the following text into authentic, natural Bhojpuri (भोजपुरी).\n"
            f"Source language: {src_lang}\n"
            f"Dialect style: {dialect} (Bhojpur/Shahabad or Purvanchal)\n"
            f"Tone/Honorific: {honorific}\n\n"
            f"Input Text: \"{text}\"\n\n"
            f"Return ONLY the Bhojpuri translation in Devanagari script. Do not add explanations."
        )

        try:
            if self.provider == "gemini":
                import urllib.request
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    cand = data.get("candidates", [])[0]
                    content = cand.get("content", {}).get("parts", [])[0].get("text", "").strip()
                    return {
                        "translated_text": content,
                        "detected_lang": src_lang,
                        "engine": "gemini",
                        "dialect": dialect
                    }
        except Exception as e:
            return {
                "translated_text": text,
                "error": str(e),
                "detected_lang": src_lang,
                "engine": f"llm_{self.provider}"
            }

        return {
            "translated_text": text,
            "error": "Unsupported LLM provider.",
            "detected_lang": src_lang,
            "engine": self.provider
        }
