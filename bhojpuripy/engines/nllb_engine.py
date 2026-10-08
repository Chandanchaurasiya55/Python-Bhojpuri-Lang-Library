"""Meta NLLB-200 (No Language Left Behind) local AI engine for offline Bhojpuri neural translation."""

from typing import Dict, Any, Optional
try:
    from .base import BaseEngine
except (ImportError, ValueError):
    from bhojpuripy.engines.base import BaseEngine

class NLLBEngine(BaseEngine):
    """
    Offline Neural Machine Translation using Meta NLLB-200 (facebook/nllb-200-distilled-600M).
    Directly supports bho_Deva (Bhojpuri in Devanagari script).
    """

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device
        self.tokenizer = None
        self.model = None
        self._is_ready = False

    def _load_model(self):
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            import torch
            
            if self.device is None:
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
            self._is_ready = True
        except ImportError:
            raise ImportError(
                "NLLB engine requires 'transformers' and 'torch'. "
                "Install them using: pip install torch transformers sentencepiece"
            )

    def translate(
        self,
        text: str,
        src_lang: str = "eng_Latn",
        dialect: str = "standard",
        honorific: str = "familiar",
        **kwargs
    ) -> Dict[str, Any]:
        if not self._is_ready:
            try:
                self._load_model()
            except Exception as e:
                return {
                    "translated_text": text,
                    "error": str(e),
                    "detected_lang": src_lang,
                    "engine": "nllb"
                }

        # NLLB Target code for Bhojpuri
        target_lang = "bho_Deva"

        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.lang_code_to_id.get(target_lang),
            max_length=256
        )
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

        return {
            "translated_text": translated_text,
            "detected_lang": src_lang,
            "engine": "nllb-200",
            "dialect": dialect
        }
