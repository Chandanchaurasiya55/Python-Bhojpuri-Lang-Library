"""Command-Line Interface (CLI) for BhojpuriPy."""

import argparse
import sys
import json

# Ensure UTF-8 output on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from bhojpuripy.client import BhojpuriTranslator
from bhojpuripy import __version__

def main():
    parser = argparse.ArgumentParser(
        description="BhojpuriPy CLI: Translate any language to Bhojpuri instantly."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text string to translate into Bhojpuri"
    )
    parser.add_argument(
        "-s", "--source",
        default="auto",
        help="Source language code (default: auto)"
    )
    parser.add_argument(
        "-e", "--engine",
        default="universal",
        choices=["universal", "rule_based", "gemini", "nllb"],
        help="Translation engine to use"
    )
    parser.add_argument(
        "-d", "--dialect",
        default="standard",
        choices=["standard", "western", "northern"],
        help="Bhojpuri regional dialect (standard, western, northern)"
    )
    parser.add_argument(
        "-r", "--roman-only",
        action="store_true",
        help="Output Romanized Bhojpuri only"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"BhojpuriPy {__version__}"
    )

    args = parser.parse_args()

    if not args.text:
        # Interactive mode
        print(f"=== BhojpuriPy CLI v{__version__} ===")
        print("Type text to translate into Bhojpuri (or 'exit' to quit):")
        translator = BhojpuriTranslator()
        while True:
            try:
                line = input("\n[Input] > ").strip()
                if not line or line.lower() in ["exit", "quit", "q"]:
                    break
                res = translator.translate(line, src=args.source, engine=args.engine, dialect=args.dialect)
                print(f"भोजपुरी : {res['bhojpuri']}")
                print(f"Roman   : {res['roman']}")
            except (KeyboardInterrupt, EOFError):
                break
        return

    translator = BhojpuriTranslator()
    res = translator.translate(
        args.text,
        src=args.source,
        engine=args.engine,
        dialect=args.dialect
    )

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.roman_only:
        print(res["roman"])
    else:
        print(f"भोजपुरी : {res['bhojpuri']}")
        print(f"Roman   : {res['roman']}")

if __name__ == "__main__":
    main()
