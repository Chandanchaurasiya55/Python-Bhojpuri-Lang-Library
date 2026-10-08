# 🌾 BhojpuriPy Library (Standalone Package)

This is the standalone **`bhojpuripy`** library folder. You can copy this entire `bhojpuripy` folder into **any** of your Python projects (Django, Flask, FastAPI, CLI, Data Science, etc.) and immediately start translating!

## ⚡ 2-Minute Quickstart

Simply place this `bhojpuripy/` folder in your project root or directory, and:

```python
import bhojpuripy as bho

# 1. Translate from any language (English, Spanish, etc.)
res = bho.translate("Hello, how are you?")
print(res["bhojpuri"])  # प्रणाम, का हाल बा?
print(res["roman"])     # Pranaam, kaa haal baa?

# 2. Translate from Hindi (Zero Latency Offline)
res = bho.translate("मुझे बहुत भूख लगी है।", src="hi")
print(res["bhojpuri"])  # हमरा बहुते भूख लागल बा।

# 3. Regional Dialects
# Standard (Bhojpur / Arrah / Buxar)
print(bho.translate("यह अच्छा है", dialect="standard")["bhojpuri"]) # ई नीमन बा

# Western (Gorakhpur / Azamgarh / Banaras)
print(bho.translate("यह अच्छा है", dialect="western")["bhojpuri"])  # ई नीमन हवे

# Northern (Saran / Siwan / Gopalganj)
print(bho.translate("यह अच्छा है", dialect="northern")["bhojpuri"]) # ई नीमन बाटे

# 4. Formality / Tone
# Familiar (Default):
print(bho.translate("where are you going", honorific="familiar")["bhojpuri"]) # तू कहाँ जात बाड़ऽ?
# Respectful / Elder:
print(bho.translate("where are you going", honorific="formal")["bhojpuri"])   # रउआ कहाँ जात बानी?

# 5. Romanization (Devanagari -> Roman Script)
print(bho.to_roman("तोहार नाम का बा?"))  # Tohaar naam kaa baa?

# 6. Bhojpuri Proverbs & Idioms
idioms = bho.get_idioms()
print(idioms[0])  # {'bhojpuri': 'नाचे ना आवे त अँगने टेढ़', ...}
```

## 📦 Requirements
- Standard Python 3.8+
- `requests>=2.28.0` (for multilingual bridge)
- Standard library (`json`, `re`, `urllib`, `os`)

Enjoy authentic Bhojpuri NLP! ❤️
