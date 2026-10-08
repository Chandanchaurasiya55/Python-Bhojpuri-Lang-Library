"""Rule-based Morpho-Syntactic Translation Engine for Hindi -> Bhojpuri."""

import os
import json
import re
from typing import Dict, Any, Optional
from bhojpuripy.engines.base import BaseEngine

class RuleBasedEngine(BaseEngine):
    """
    Offline zero-dependency Morphological Engine for Hindi to Bhojpuri translation.
    Applies grammatical inflection rules, lexicon replacement, and dialect transformations.
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.vocab = self._load_json("vocabulary.json")
        self.grammar = self._load_json("grammar_patterns.json")
        
        # Flatten dictionary for quick word lookup
        self.word_map = {}
        for category in ["pronouns", "interrogatives", "auxiliaries", "verbs", "common_nouns", "adjectives_adverbs", "greetings_and_phrases"]:
            if category in self.vocab:
                self.word_map.update(self.vocab[category])

        self.exact_phrases = self.grammar.get("exact_phrases", {})
        self.postpositions = self.grammar.get("postpositions", {})
        self.verb_transformations = self.grammar.get("verb_transformations", [])
        self.dialects_info = self.grammar.get("dialects", {})

    def _load_json(self, filename: str) -> dict:
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def translate(
        self,
        text: str,
        src_lang: str = "hi",
        dialect: str = "standard",
        honorific: str = "familiar",
        **kwargs
    ) -> Dict[str, Any]:
        """Translates Hindi text to Bhojpuri using rule-based grammar and vocabulary."""
        text = text.strip()
        if not text:
            return {
                "translated_text": "",
                "detected_lang": src_lang,
                "engine": "rule_based",
                "dialect": dialect
            }

        cleaned = text.strip().rstrip("।!?., ")

        # 1. Check exact phrase match first
        if cleaned in self.exact_phrases:
            result = self.exact_phrases[cleaned]
            result = self._apply_dialect_and_honorific(result, dialect, honorific)
            return {
                "translated_text": result,
                "detected_lang": "hi",
                "engine": "rule_based_exact",
                "dialect": dialect
            }

        # 2. Check phrase substrings in exact phrases
        output = text
        for phrase, bho_phrase in self.exact_phrases.items():
            if phrase in output:
                output = output.replace(phrase, bho_phrase)

        # 3. Apply postposition rules (e.g. "के लिए" -> "खातिर")
        for hindi_post, bho_post in self.postpositions.items():
            output = re.sub(re.escape(hindi_post) + r'(?=\s|$|[।!?.,])', bho_post, output)

        # 4. Apply verb transformations (e.g., "कर रहा हूँ" -> "करत बानी")
        for rule in self.verb_transformations:
            pat = rule.get("pattern")
            rep = rule.get("replacement")
            if pat and rep:
                output = re.sub(pat, rep, output)

        # 5. Tokenize and map remaining words (pronouns, question words, auxiliaries)
        tokens = re.split(r'(\s+|[।!?.,:;"\'\(\)\[\]])', output)
        translated_tokens = []

        for token in tokens:
            if not token:
                continue
            token_clean = token.strip()
            if token_clean in self.word_map:
                translated_tokens.append(self.word_map[token_clean])
            else:
                translated_tokens.append(token)

        output = "".join(translated_tokens)

        # 6. Apply dialect and honorific fine-tuning
        output = self._apply_dialect_and_honorific(output, dialect, honorific)

        return {
            "translated_text": output,
            "detected_lang": "hi",
            "engine": "rule_based",
            "dialect": dialect
        }

    def _apply_dialect_and_honorific(self, text: str, dialect: str, honorific: str) -> str:
        res = text.strip()

        # Handle greetings / general "how are you" culturally based on honorific
        has_pranam = "प्रणाम" in res or "नमस्ते" in text or "नमस्कार" in text
        if "कइसे बानी" in res or "क्या हाल" in res or "का हाल" in res or "कैसे हैं" in res or "कैसे हो" in res:
            if honorific == "formal":
                greeting_q = "रउआ कइसे हईं?" if dialect == "western" else "रउआ कइसे बानी?"
            else: # familiar or informal
                if dialect == "western":
                    greeting_q = "का हाल-चाल हवे?"
                elif dialect == "northern":
                    greeting_q = "का हाल बाटे?"
                else:
                    greeting_q = "का हाल बा?"
            
            if has_pranam:
                res = f"प्रणाम, {greeting_q}"
            else:
                res = greeting_q
            return res

        # General Honorific Adjustment (Informal / Familiar vs Formal)
        if honorific == "formal":
            res = re.sub(r'(^|\s+)तू(?=$|\s|[।!?.,])', r'\1रउआ', res)
            res = re.sub(r'(^|\s+)तोहार(?=$|\s|[।!?.,])', r'\1राउर', res)
            res = re.sub(r'(^|\s+)तोहरा के(?=$|\s|[।!?.,])', r'\1रउरा के', res)
            res = re.sub(r'(^|\s+)तोहरा(?=$|\s|[।!?.,])', r'\1रउरा', res)
            res = re.sub(r'(^|\s+)बाड़ऽ(?=$|\s|[।!?.,])', r'\1बानी', res)
            res = re.sub(r'(^|\s+)बाड़ा(?=$|\s|[।!?.,])', r'\1बानी', res)
            res = re.sub(r'(^|\s+)बाड़न(?=[?।!]|\s|$)', r'\1बानी', res)
            res = re.sub(r'(^|\s+)हवा(?=$|\s|[।!?.,])', r'\1हईं', res)
            res = re.sub(r'(^|\s+)तारे(?=$|\s|[।!?.,])', r'\1बानी', res)
        elif honorific in ["informal", "familiar"]:
            # If text had formal markers, downscale to familiar/informal
            res = re.sub(r'(^|\s+)रउआ(?=$|\s|[।!?.,])', r'\1तू', res)
            res = re.sub(r'(^|\s+)राउर(?=$|\s|[।!?.,])', r'\1तोहार', res)
            res = re.sub(r'(^|\s+)रउरा के(?=$|\s|[।!?.,])', r'\1तोहरा के', res)
            res = re.sub(r'(^|\s+)रउरा(?=$|\s|[।!?.,])', r'\1तोहार', res)
            # Question endings when addressed to 'तू'
            if "तू" in res:
                if dialect == "western":
                    res = re.sub(r'(^|\s+)बानी(?=[?।!]|\s|$)', r'\1हवा', res)
                    res = re.sub(r'(^|\s+)बाड़न(?=[?।!]|\s|$)', r'\1हवा', res)
                elif dialect == "northern":
                    res = re.sub(r'(^|\s+)बानी(?=[?।!]|\s|$)', r'\1तारे', res)
                    res = re.sub(r'(^|\s+)बाड़न(?=[?।!]|\s|$)', r'\1तारे', res)
                else: # standard
                    res = re.sub(r'(^|\s+)बानी(?=[?।!]|\s|$)', r'\1बाड़ऽ', res)
                    res = re.sub(r'(^|\s+)बाड़न(?=[?।!]|\s|$)', r'\1बाड़ऽ', res)

        # Regional Dialect Specializations
        if dialect == "western":
            # Gorakhpur / Purvanchal / Azamgarh / Banaras
            # Auxiliaries
            res = re.sub(r'(^|\s+)बा(?=$|\s|[।!?.,])', r'\1हवे', res)
            res = re.sub(r'(^|\s+)बानी(?=$|\s|[।!?.,])', r'\1हईं', res)
            res = re.sub(r'(^|\s+)बाड़ऽ(?=$|\s|[।!?.,])', r'\1हवा', res)
            res = re.sub(r'(^|\s+)बाड़ा(?=$|\s|[।!?.,])', r'\1हवा', res)
            res = re.sub(r'(^|\s+)बाड़न(?=$|\s|[।!?.,])', r'\1हवें', res)
            # Postpositions & Spatial
            res = re.sub(r'(^|\s+)खातिर(?=$|\s|[।!?.,])', r'\1बदे', res)
            res = re.sub(r'(^|\s+)एहिजा(?=$|\s|[।!?.,])', r'\1इहाँ', res)
            res = re.sub(r'(^|\s+)ओहिजा(?=$|\s|[।!?.,])', r'\1उहाँ', res)
            # Common phrases
            res = re.sub(r'का हाल बा\??', 'का हाल-चाल हवे?', res)
            res = re.sub(r'का बात बा', 'का बात हवे', res)

        elif dialect == "northern":
            # Saran / Siwan / Gopalganj / Champaran
            # Auxiliaries
            res = re.sub(r'(^|\s+)बा(?=$|\s|[।!?.,])', r'\1बाटे', res)
            # Continuous / informal
            if honorific != "formal":
                res = re.sub(r'(^|\s+)बाड़ऽ(?=$|\s|[।!?.,])', r'\1तारे', res)
                res = re.sub(r'(^|\s+)बाड़ा(?=$|\s|[।!?.,])', r'\1तारे', res)
            # Postpositions & Spatial
            res = re.sub(r'(^|\s+)खातिर(?=$|\s|[।!?.,])', r'\1ला', res)
            res = re.sub(r'(^|\s+)एहिजा(?=$|\s|[।!?.,])', r'\1एने', res)
            res = re.sub(r'(^|\s+)ओहिजा(?=$|\s|[।!?.,])', r'\1ओने', res)
            res = re.sub(r'का हाल बा\??', 'का हाल बाटे?', res)

        # Standard Bhojpuri (Arrah / Buxar / Bhojpur)
        else:
            # Clean up any leftover artifacts
            res = re.sub(r'का हाल-चाल हवे\??', 'का हाल बा?', res)

        # Natural word order & punctuation cleanups
        res = re.sub(r'(तोहार|राउर)\s+का\s+नाम', r'\1 नाम का', res)
        res = re.sub(r'(^|\s+)कहां(?=$|\s|[।!?.,])', r'\1कहाँ', res)
        if any(q in res for q in ["नाम का", "कहाँ", "का करत", "कइसे", "का भइल", "के हवे", "का हवे", "का बा", "का बाटे"]) and not res.endswith(('?', '।', '!')):
            res = res + "?"

        return res
