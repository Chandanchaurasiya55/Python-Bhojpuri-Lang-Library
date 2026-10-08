"""FastAPI Backend Server for BhojpuriPy Translation API."""

import os
import sys
import time
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Ensure root workspace is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import bhojpuripy as bho
from bhojpuripy import __version__

app = FastAPI(
    title="BhojpuriPy API",
    description="High-performance Multilingual Translation API for Bhojpuri (भोजपुरी)",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = bho.BhojpuriTranslator()

# Pydantic Schemas
class TranslateRequest(BaseModel):
    text: str = Field(..., example="Where are you going?", description="Text to translate into Bhojpuri")
    source_lang: str = Field(default="auto", example="auto", description="Source language ISO code")
    engine: str = Field(default="universal", example="universal", description="Engine: universal, rule_based, gemini, nllb")
    dialect: str = Field(default="standard", example="standard", description="Bhojpuri dialect: standard, western, northern")
    honorific: str = Field(default="familiar", example="familiar", description="Tone: informal, familiar, formal")
    include_roman: bool = Field(default=True, description="Whether to include Romanized transliteration")

class TransliterateRequest(BaseModel):
    text: str = Field(..., example="का हाल बा?", description="Devanagari text to transliterate")

class TranslationResponse(BaseModel):
    bhojpuri: str
    roman: str
    source_text: str
    source_lang: str
    detected_lang: str
    engine: str
    dialect: str
    intermediate_hindi: Optional[str] = None
    execution_time_ms: float

# Routes
@app.post("/api/translate", response_model=TranslationResponse)
async def translate_text(req: TranslateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    start_time = time.time()
    try:
        res = translator.translate(
            text=req.text,
            src=req.source_lang,
            engine=req.engine,
            dialect=req.dialect,
            honorific=req.honorific,
            include_roman=req.include_roman
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

    latency_ms = round((time.time() - start_time) * 1000, 2)
    return TranslationResponse(
        bhojpuri=res.get("bhojpuri", ""),
        roman=res.get("roman", ""),
        source_text=res.get("source_text", req.text),
        source_lang=res.get("source_lang", req.source_lang),
        detected_lang=res.get("detected_lang", req.source_lang),
        engine=res.get("engine", req.engine),
        dialect=res.get("dialect", req.dialect),
        intermediate_hindi=res.get("intermediate_hindi"),
        execution_time_ms=latency_ms
    )

@app.post("/api/transliterate")
async def transliterate_text(req: TransliterateRequest):
    roman = bho.to_roman(req.text)
    return {
        "original": req.text,
        "roman": roman
    }

@app.get("/api/languages")
async def get_languages():
    return {
        "supported_languages": bho.get_languages()
    }

@app.get("/api/dialects")
async def get_dialects():
    return {
        "dialects": bho.get_dialects()
    }

@app.get("/api/idioms")
async def get_idioms():
    return {
        "idioms": bho.get_idioms()
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "BhojpuriPy Translation API",
        "version": __version__
    }

# Mount Frontend static files
frontend_dir = os.path.join(root_dir, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_frontend():
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": f"BhojpuriPy API v{__version__} is running. Visit /docs for Swagger UI."}
