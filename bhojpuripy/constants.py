"""Constants, language codes, and dialect configurations for bhojpuripy."""

BHOJPURI_ISO = "bho"
BHOJPURI_NLLB_CODE = "bho_Deva"

SUPPORTED_LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "bn": "Bengali (বাংলা)",
    "ur": "Urdu (اردو)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "ne": "Nepali (नेपाली)",
    "ar": "Arabic (العربية)",
    "ru": "Russian (Русский)",
    "zh": "Chinese (中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "pt": "Portuguese (Português)",
    "it": "Italian (Italiano)",
    "tr": "Turkish (Türkçe)",
    "fa": "Persian (فارسی)",
    "id": "Indonesian (Bahasa Indonesia)"
}

DIALECTS = {
    "standard": {
        "id": "standard",
        "name": "Standard (Bhojpur / Shahabad / Buxar)",
        "desc": "छपरा-आरा-बक्सर क्षेत्र की मुख्य मानक बोली"
    },
    "western": {
        "id": "western",
        "name": "Western (Gorakhpur / Azamgarh / Banaras)",
        "desc": "पूर्वांचल, गोरखपुर और बनारस क्षेत्र की बोली"
    },
    "northern": {
        "id": "northern",
        "name": "Northern (Saran / Siwan / Gopalganj)",
        "desc": "सीवान, सारण और गोपालगंज की बोली"
    }
}

HONORIFICS = {
    "informal": "Informal / Peer (तू / तोहार)",
    "familiar": "Familiar (तूँ / बाड़ा)",
    "formal": "Respectful / Elder (रउआ / अपने)"
}
