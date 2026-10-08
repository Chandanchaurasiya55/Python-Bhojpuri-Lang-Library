"""
BhojpuriPy Showcase: Regional Dialect Comparison
Compares Standard (Bhojpur), Western (Gorakhpur), and Northern (Saran) dialects.
"""

def main():
    print("🌾 BhojpuriPy: Regional Dialect Comparison Showcase")
    print("=" * 60)
    
    dialects = [
        ("how are you", {
            "Standard (Bhojpur/Arrah)": "का हाल बा?",
            "Western (Gorakhpur/Banaras)": "का हाल-चाल हवे?",
            "Northern (Saran/Siwan)": "का हाल बाटे?"
        }),
        ("Where are you going?", {
            "Standard (Bhojpur/Arrah)": "तू कहाँ जात बाड़ऽ?",
            "Western (Gorakhpur/Banaras)": "तू कहाँ जात हवा?",
            "Northern (Saran/Siwan)": "तू कहाँ जात तारे?"
        }),
        ("What is your name?", {
            "Standard (Bhojpur/Arrah)": "तोहार नाम का बा?",
            "Western (Gorakhpur/Banaras)": "तोहार नाम का हवे?",
            "Northern (Saran/Siwan)": "तोहार नाम का बाटे?"
        }),
        ("This is good.", {
            "Standard (Bhojpur/Arrah)": "ई नीमन बा",
            "Western (Gorakhpur/Banaras)": "ई नीमन हवे",
            "Northern (Saran/Siwan)": "ई नीमन बाटे"
        })
    ]

    for phrase, res in dialects:
        print(f"\n[Phrase]: \"{phrase}\"")
        for dial, val in res.items():
            print(f"  • {dial:<30} -> {val}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
