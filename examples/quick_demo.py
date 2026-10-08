"""
Quick demo example for BhojpuriPy Translation Library.
Shows how to translate text, select regional dialects, and get Roman script outputs.
"""

# Example translations demo
demo_data = [
    {
        "input": "Hello, how are you?",
        "dialect": "standard (भोजपुर/बक्सर/आरा)",
        "output": "प्रणाम, का हाल बा?",
        "roman": "Pranaam, kaa haal baa?"
    },
    {
        "input": "How are you?",
        "dialect": "western (गोरखपुर/बनारस/पूर्वांचल)",
        "output": "का हाल-चाल हवे?",
        "roman": "Kaa haal-chaal have?"
    },
    {
        "input": "Where are you going?",
        "dialect": "northern (सारण/सीवान/गोपालगंज)",
        "output": "तू कहाँ जात तारे?",
        "roman": "Tu kahaan jaat taare?"
    },
    {
        "input": "What is your name?",
        "dialect": "standard",
        "output": "तोहार नाम का बा?",
        "roman": "Tohaar naam kaa baa?"
    },
    {
        "input": "Everything is fine here.",
        "dialect": "standard",
        "output": "एहिजा सब कुछ ठीक बा।",
        "roman": "Ehija sab kuchh theek baa."
    }
]

def main():
    print("=" * 50)
    print("🌾 BhojpuriPy: Quick Demo Showcase")
    print("=" * 50)
    for item in demo_data:
        print(f"[Input]    : {item['input']}")
        print(f"[Dialect]  : {item['dialect']}")
        print(f"[Bhojpuri] : {item['output']}")
        print(f"[Roman]    : {item['roman']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
