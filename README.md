# 🌾 BhojpuriPy (भोजपुरीपाई)

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)
![NLP](https://img.shields.io/badge/Indic%20NLP-Bhojpuri%20(bho)-orange?style=for-the-badge)
![Build Status](https://img.shields.io/badge/tests-passing-brightgreen?style=for-the-badge)

**The Universal Open-Source Multilingual Translation Library and Ecosystem for Bhojpuri (भोजपुरी).**

*Translate any language (English, Hindi, Spanish, French, Bengali, etc.) into authentic, idiomatic Bhojpuri with regional dialects, Roman phonetics, and AI neural support.*

[Features](#-key-features) • [Installation](#-installation) • [Quickstart](#-quickstart-python) • [CLI](#-command-line-interface-cli) • [Architecture](#-architecture) • [API & Web UI](#-web-ui--rest-api)

</div>

---

## 📖 Overview

**Bhojpuri** (ISO 639-3: `bho`) is spoken by over 50+ million people across Bihar, Eastern Uttar Pradesh (Purvanchal), Jharkhand, Nepal, and the diaspora in Mauritius, Fiji, and the Caribbean. Despite its cultural richness, high-quality, developer-friendly open-source NLP libraries for Bhojpuri have historically been scarce.

**BhojpuriPy** solves this by providing:
1. **Core Python Package (`bhojpuripy`)**: Simple 2-line import for Python developers.
2. **Hybrid Engine Pipeline**: Combines an ultra-fast zero-latency offline Morphological Rule Engine, an open Multilingual Translation Bridge, Meta's NLLB-200 Neural model, and Gemini AI.
3. **Dialect Customization**: Choose between Standard (Bhojpur/Arrah/Buxar), Western (Gorakhpur/Banaras), and Northern (Saran/Siwan/Gopalganj) dialects.
4. **Devanagari + Roman Script**: Instant phonetic transliteration (e.g. *का हाल बा* $\rightarrow$ *Kaa haal baa*).
5. **Interactive Full-Stack Web App**: Built with FastAPI and a modern Indic Glassmorphic UI featuring Audio Pronunciation (TTS).

---

## 🌟 Key Features

- 🌐 **Translate From Any Language**: Supports 50+ source languages including English, Hindi, Spanish, French, German, Bengali, Urdu, Russian, and Japanese.
- ⚡ **Zero-Latency Offline Mode**: Built-in morpho-syntactic engine transforms Hindi/Indic languages to Bhojpuri locally in milliseconds without network calls.
- 🏛️ **Bhojpuri Dialect Support**:
  - **Standard**: Bhojpur, Buxar, Rohtas, Arrah (`बा`, `बानी`, `खातिर`)
  - **Western**: Gorakhpur, Azamgarh, Banaras, Deoria (`हवे`, `हईं`, `बदे`)
  - **Northern**: Saran, Siwan, Gopalganj (`बाटे`, `ला`)
- 👥 **Tone & Honorifics**: Flexible formality levels (Informal: `तू/बाड़ऽ`, Familiar: `तूँ/बाड़ा`, Formal/Elder: `रउआ/बानी`).
- 🔤 **Automatic Romanization**: Generates readable English-letter phonetics for subtitles, chats, or non-Devanagari readers.
- 📜 **Bhojpuri Idioms (कहावतें)**: Curated database of authentic folk idioms and proverbs with Hindi & English meanings.
- 💻 **CLI Tool Included**: Translate directly in your terminal with `bhojpuri "Where are you going?"`.
- 🚀 **Production-Ready REST API**: Complete FastAPI server with automatic Swagger documentation (`/docs`).

---

## 🏗️ Architecture

```
                               ┌────────────────────────┐
                               │   Source Text (Any)    │
                               └───────────┬────────────┘
                                           │
                                           ▼
                     ┌───────────────────────────────────────────┐
                     │          Translation Router               │
                     └─────────────────────┬─────────────────────┘
                                           │
         ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
         │                   │                           │                   │
         ▼                   ▼                           ▼                   ▼
┌──────────────────┐ ┌────────────────┐ ┌──────────────────────────┐ ┌──────────────┐
│ Universal Bridge │ │  Rule Engine   │ │     Meta NLLB-200        │ │  Gemini AI   │
│ Any Lang -> Deva │ │ Zero-Latency   │ │  facebook/nllb-200-600M  │ │ Nuance/Slang │
└────────┬─────────┘ └───────┬────────┘ └────────────┬─────────────┘ └──────┬───────┘
         │                   │                       │                      │
         └─────────────┬─────┴───────────────────────┴──────────────────────┘
                       │
                       ▼
         ┌───────────────────────────┐
         │ Dialect & Honorific Tuner │
         │  Standard / West / North  │
         └─────────────┬─────────────┘
                       │
                       ▼
         ┌───────────────────────────┐
         │   Transliteration Core    │
         │   Devanagari -> Roman     │
         └─────────────┬─────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌───────────────────┐       ┌─────────────────┐
│ Devanagari Output │       │  Roman Output   │
│ (कहाँ जात बाड़ऽ?) │       │ (Kahaan jaat?)  │
└───────────────────┘       └─────────────────┘
```

---

## 📦 Installation

### Option 1: Install via Git / Local (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/bhojpuripy.git
cd "Python library Bhojpuri"

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
.venv\Scripts\activate     # On Windows PowerShell

# 3. Install dependencies and the package
pip install -r requirements.txt
pip install -e .
```

### Option 2: Install via PyPI (Once Published)

```bash
pip install bhojpuripy
```

---

## 🚀 Quickstart (Python)

### 1. Basic Translation (Auto Detect)

```python
import bhojpuripy as bho

# Translate from English
res = bho.translate("Hello, how are you?")
print(res["bhojpuri"])  # Output: प्रणाम, रउआ कइसे बानी?
print(res["roman"])     # Output: Pranaam, rauaa kaise baanee?

# Translate from Hindi (Offline Rule Engine)
res = bho.translate("मुझे बहुत भूख लगी है।", src="hi")
print(res["bhojpuri"])  # Output: हमरा बहुते भूख लागल बा।
print(res["roman"])     # Output: Hamaraa bahute bhookh laagal baa।
```

### 2. Multi-Language Support

```python
import bhojpuripy as bho

# Spanish -> Bhojpuri
res = bho.translate("Hola, ¿cómo estás?", src="es")
print(res["bhojpuri"])  # Output: प्रणाम, रउआ कइसे बानी?

# French -> Bhojpuri
res = bho.translate("Je veux manger", src="fr")
print(res["bhojpuri"])  # Output: हम खाना खाएल चाहत बानी
```

### 3. Choosing Regional Dialects & Formality

```python
import bhojpuripy as bho

# Standard Bhojpuri (Bhojpur / Shahabad)
res1 = bho.translate("यह अच्छा है", dialect="standard")
print(res1["bhojpuri"])  # ई नीमन बा

# Western Bhojpuri (Gorakhpur / Purvanchal / Banaras)
res2 = bho.translate("यह अच्छा है", dialect="western")
print(res2["bhojpuri"])  # ई नीमन हवे

# Northern Bhojpuri (Saran / Siwan)
res3 = bho.translate("यह अच्छा है", dialect="northern")
print(res3["bhojpuri"])  # ई नीमन बाटे

# Respectful / Elder tone (Formal)
res_formal = bho.translate("तुम कहाँ जा रहे हो?", honorific="formal")
print(res_formal["bhojpuri"])  # रउआ कहाँ जात बानी?
```

### 4. Romanization & Transliteration

```python
import bhojpuripy as bho

roman = bho.to_roman("तोहार नाम का बा?")
print(roman)  # Output: Tohaar naam kaa baa?
```

### 5. Accessing Authentic Bhojpuri Idioms (कहावतें)

```python
import bhojpuripy as bho

idioms = bho.get_idioms()
for item in idioms[:3]:
    print(f"Bhojpuri: {item['bhojpuri']}")
    print(f"Hindi   : {item['hindi']}")
    print(f"English : {item['english']}\n")
```

---

## 💻 Command-Line Interface (CLI)

BhojpuriPy comes with a terminal utility:

```bash
# Simple translation
bhojpuri "Where are you going?"

# Specify dialect
bhojpuri "Everything is good here." --dialect western

# Get Roman output only
bhojpuri "Good morning" --roman-only

# JSON output
bhojpuri "What is your name?" --json

# Interactive REPL mode
bhojpuri
```

---

## 🌐 Web UI & REST API

BhojpuriPy includes a full-stack interactive web application and REST API server:

### Launching the Server

```bash
python run_server.py
```

- **Interactive Web App**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### API Endpoints

#### `POST /api/translate`
Request:
```json
{
  "text": "Where are you going?",
  "source_lang": "auto",
  "engine": "universal",
  "dialect": "standard",
  "honorific": "familiar",
  "include_roman": true
}
```

Response:
```json
{
  "bhojpuri": "रउआ कहां जात बाड़न?",
  "roman": "Rauaa kahaan jaat baada़n?",
  "source_text": "Where are you going?",
  "source_lang": "auto",
  "detected_lang": "en",
  "engine": "universal_pipeline",
  "dialect": "standard",
  "execution_time_ms": 32.4
}
```

#### `GET /api/languages`
Lists all 50+ supported source languages.

#### `GET /api/idioms`
Fetches the complete dataset of Bhojpuri proverbs and idioms.

#### `POST /api/transliterate`
Converts Devanagari script to Roman phonetics.

---

## 📂 Project Directory Structure

```text
Python library Bhojpuri/
│
├── bhojpuripy/                     # Core Python Library
│   ├── __init__.py                 # Top-level API exports
│   ├── client.py                   # BhojpuriTranslator class
│   ├── constants.py                # Language codes & dialects
│   ├── transliterate.py            # Devanagari -> Roman converter
│   ├── cli.py                      # Terminal CLI tool
│   ├── __main__.py                 # python -m bhojpuripy support
│   ├── engines/
│   │   ├── base.py                 # Abstract Engine interface
│   │   ├── rule_engine.py          # Zero-latency Morpho-Syntactic engine
│   │   ├── universal_engine.py     # Multilingual 50+ language bridge
│   │   ├── llm_engine.py           # Gemini/OpenAI cloud engine
│   │   └── nllb_engine.py          # Meta NLLB-200 local neural engine
│   └── data/
│       ├── vocabulary.json         # Bhojpuri-Hindi-English lexicon
│       ├── grammar_patterns.json   # Verb conjugations & dialect rules
│       ├── idioms.json             # Bhojpuri idioms (कहावतें)
│       └── phonetics.json          # Transliteration mappings
│
├── backend/                        # FastAPI REST Server
│   ├── main.py                     # API routes & static mounting
│   └── requirements.txt            # Server dependencies
│
├── frontend/                       # Modern Glassmorphic Web App
│   ├── index.html                  # Responsive UI layout
│   ├── style.css                   # Indic gradient aesthetic (Vanilla CSS)
│   └── app.js                      # Client logic, TTS, & code generation
│
├── tests/                          # Automated Unit Tests
│   └── test_translation.py         # Test suite
│
├── run_server.py                   # One-click server launcher
├── setup.py                        # Setuptools packaging configuration
├── pyproject.toml                  # Modern PEP 621 build specification
├── requirements.txt                # Pinned dependencies
└── README.md                       # Comprehensive documentation
```

---

## 🧪 Running Tests

To run the automated test suite:

```bash
python -m unittest discover tests
```

---

## 🤝 Contributing

Contributions are warmly welcomed! You can help by:
1. Adding more words to `bhojpuripy/data/vocabulary.json`.
2. Expanding regional dialect rules in `bhojpuripy/data/grammar_patterns.json`.
3. Adding folk idioms to `bhojpuripy/data/idioms.json`.
4. Improving transliteration rules for complex conjuncts.

### Steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-words`)
3. Commit your changes (`git commit -m 'Add Siwan regional verbs'`)
4. Push to the branch (`git push origin feature/new-words`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

<div align="center">
  <sub>बनावल गइल बा भोजपुरी समाज आ ओपेन सोर्स कम्युनिटी खातिर ❤️</sub>
</div>
#   P y t h o n - B h o j p u r i - L a n g - L i b r a r y  
 