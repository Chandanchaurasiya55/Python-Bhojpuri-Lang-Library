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

        # 1. Check exact phrase match
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
        res = text

        # Honorific adjustment (Elder/Formal vs Informal)
        if honorific == "formal":
            res = re.sub(r'(^|\s+)तू(?=$|\s|[।!?.,])', r'\1रउआ', res)
            res = re.sub(r'(^|\s+)तोहार(?=$|\s|[।!?.,])', r'\1राउर', res)
            res = re.sub(r'(^|\s+)तोहरा के(?=$|\s|[।!?.,])', r'\1रउरा के', res)
            res = re.sub(r'(^|\s+)बाड़ऽ(?=$|\s|[।!?.,])', r'\1बानी', res)
        elif honorific == "informal":
            res = re.sub(r'(^|\s+)रउआ(?=$|\s|[।!?.,])', r'\1तू', res)
            res = re.sub(r'(^|\s+)राउर(?=$|\s|[।!?.,])', r'\1तोहार', res)
            res = re.sub(r'(^|\s+)रउरा के(?=$|\s|[।!?.,])', r'\1तोहरा के', res)

        # Dialect transformations
        if dialect == "western":
            # Gorakhpur / Purvanchal / Banaras
            res = re.sub(r'(^|\s+)बानी(?=$|\s|[।!?.,])', r'\1हईं', res)
            res = re.sub(r'(^|\s+)बा(?=$|\s|[।!?.,])', r'\1हवे', res)
            res = re.sub(r'(^|\s+)खातिर(?=$|\s|[।!?.,])', r'\1बदे', res)
        elif dialect == "northern":
            # Saran / Siwan / Gopalganj
            res = re.sub(r'(^|\s+)बा(?=$|\s|[।!?.,])', r'\1बाटे', res)
            res = re.sub(r'(^|\s+)खातिर(?=$|\s|[।!?.,])', r'\1ला', res)

        return res
