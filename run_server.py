"""
Server Launcher script for BhojpuriPy Translator.
Runs the FastAPI Backend and serves the Frontend at http://localhost:8000.
"""

import sys
import os

# Ensure UTF-8 output on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uvicorn

def main():
    print("=" * 60)
    print("   [+] BhojpuriPy Multilingual AI Translator Server")
    print("   [*] Web UI & API running at: http://localhost:8000")
    print("   [*] Swagger API Docs at:      http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
