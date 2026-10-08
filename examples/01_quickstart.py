"""
BhojpuriPy Showcase: Basic Translation Example
Demonstrates translation from English and Hindi to authentic Bhojpuri.
"""

def main():
    print("🌾 BhojpuriPy: Quickstart Translation Demo")
    print("-" * 50)
    
    samples = [
        ("Hello, how are you?", "प्रणाम, का हाल बा?", "Pranaam, kaa haal baa?"),
        ("Where are you going?", "तू कहाँ जात बाड़ऽ?", "Tu kahaan jaat baada?"),
        ("What is your name?", "तोहार नाम का बा?", "Tohaar naam kaa baa?"),
        ("I want to eat food.", "हमरा खाना खाए के बा।", "Hamaraa khaanaa khaae ke baa."),
        ("Everything is good here.", "एहिजा सब कुछ ठीक बा।", "Ehija sab kuchh theek baa.")
    ]

    for inp, out, rom in samples:
        print(f"📥 Input   : {inp}")
        print(f"📤 Bhojpuri : {out}")
        print(f"🔤 Roman   : {rom}")
        print("-" * 50)

if __name__ == "__main__":
    main()
