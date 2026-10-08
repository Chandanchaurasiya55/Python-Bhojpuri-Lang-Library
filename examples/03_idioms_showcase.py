"""
BhojpuriPy Showcase: Authentic Folk Idioms & Sayings (कहावतें)
"""

def main():
    print("🌾 BhojpuriPy: Curated Bhojpuri Idioms (कहावतें)")
    print("=" * 60)
    
    idioms = [
        ("नाचे ना आवे त अँगने टेढ़", "Naache naa aave ta angane tedh", "A bad workman blames his tools"),
        ("जेकर लाठी ओकर भँइस", "Jekar laathi okar bhains", "Might is right"),
        ("अपने हाथे जगन्नाथ", "Apne haathe Jagannath", "Self-help is the best help"),
        ("का बरखा जब खेत सुखाइल", "Kaa barkha jab khet sukhayal", "What use is rain when the crops are dead"),
        ("बोवल बबूल त आम कहाँ से पाई", "Boval babool ta aam kahaan se paayi", "You reap what you sow")
    ]

    for bhoj, rom, eng in idioms:
        print(f"📜 {bhoj}")
        print(f"   🔤 Roman   : {rom}")
        print(f"   💡 English : {eng}\n")

if __name__ == "__main__":
    main()
