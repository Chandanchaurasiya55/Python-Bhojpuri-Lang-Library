"""Devanagari to Roman transliteration module for Bhojpuri text."""

import json
import os
from typing import Optional

def _load_phonetics():
    data_path = os.path.join(os.path.dirname(__file__), "data", "phonetics.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"vowels": {}, "matras": {}, "consonants": {}}

_PHONETICS = _load_phonetics()

def devanagari_to_roman(text: str) -> str:
    """
    Transliterates Bhojpuri text from Devanagari script to Roman script (Hinglish/English characters).
    Example: 'का हाल बा?' -> 'Kaa haal baa?'
    """
    if not text:
        return ""
        
    vowels = _PHONETICS.get("vowels", {})
    matras = _PHONETICS.get("matras", {})
    consonants = _PHONETICS.get("consonants", {})
    virama = "्"
    
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        char = text[i]
        
        # Check if punctuation or whitespace
        if not ('\u0900' <= char <= '\u097F'):
            result.append(char)
            i += 1
            continue
            
        # Vowels
        if char in vowels:
            result.append(vowels[char])
            i += 1
            continue
            
        # Consonants
        if char in consonants:
            roman_cons = consonants[char]
            
            # Lookahead for matra or virama
            if i + 1 < n:
                next_char = text[i + 1]
                if next_char == virama:
                    result.append(roman_cons)
                    i += 2
                    continue
                elif next_char in matras:
                    matra_roman = matras[next_char]
                    result.append(roman_cons + matra_roman)
                    i += 2
                    continue
                    
            # Default inherent vowel 'a' if not at the very end of word
            # In Bhojpuri/Hindi, word-final consonants usually drop schwa
            is_word_end = (i + 1 == n) or (text[i + 1] in ' \t\n.,!?।')
            if is_word_end:
                result.append(roman_cons)
            else:
                result.append(roman_cons + "a")
            i += 1
            continue
            
        # Matra standalone (uncommon)
        if char in matras:
            result.append(matras[char])
            i += 1
            continue
            
        result.append(char)
        i += 1
        
    res_str = "".join(result)
    # Capitalize first letter of sentences
    sentences = res_str.split(". ")
    capitalized = [s.strip().capitalize() if s else "" for s in sentences]
    return ". ".join(capitalized).replace("  ", " ").strip()
