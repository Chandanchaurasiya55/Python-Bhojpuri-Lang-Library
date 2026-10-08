"""Unit tests for bhojpuripy library."""

import unittest
import bhojpuripy as bho

class TestBhojpuriPy(unittest.TestCase):

    def test_hindi_to_bhojpuri_greeting(self):
        res = bho.translate("नमस्ते, आप कैसे हैं?", src="hi")
        self.assertIn("प्रणाम", res["bhojpuri"])
        self.assertTrue(len(res["bhojpuri"]) > 0)
        self.assertTrue(len(res["roman"]) > 0)

    def test_english_to_bhojpuri(self):
        res = bho.translate("Where are you going?", src="en")
        self.assertIn("जात", res["bhojpuri"])
        self.assertEqual(res["detected_lang"], "en")

    def test_pronouns(self):
        res = bho.translate("मेरा नाम राम है।", src="hi")
        self.assertIn("हमार", res["bhojpuri"])
        self.assertIn("नाम", res["bhojpuri"])

    def test_dialects(self):
        # Western dialect (Gorakhpur) uses 'हवे' / 'हईं'
        res_standard = bho.translate("यह अच्छा है", src="hi", dialect="standard")
        res_western = bho.translate("यह अच्छा है", src="hi", dialect="western")
        self.assertIn("बा", res_standard["bhojpuri"])
        self.assertIn("हवे", res_western["bhojpuri"])

    def test_transliteration(self):
        roman = bho.to_roman("का हाल बा")
        self.assertTrue("haal" in roman.lower() or "kaa" in roman.lower())

    def test_idioms(self):
        idioms = bho.get_idioms()
        self.assertTrue(len(idioms) > 0)
        self.assertIn("bhojpuri", idioms[0])
        self.assertIn("meaning", idioms[0])

if __name__ == "__main__":
    unittest.main()
