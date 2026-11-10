import unittest
import numpy as np
from photo_gate import assess, near_duplicate
from voice_notes import parse_notes
from report import build


def flat():   return np.full((100, 100, 3), 120.0)
def sharp():
    img = np.zeros((100, 100, 3)); img[::2, ::2] = 200; return img


class TestPhotoGate(unittest.TestCase):
    def test_blurry_retake(self):
        v = assess("a.jpg", flat())
        self.assertFalse(v.usable)
        self.assertTrue(any("blurry" in i for i in v.issues))

    def test_sharp_ok(self):
        self.assertTrue(assess("b.jpg", sharp()).usable)

    def test_duplicate(self):
        self.assertTrue(near_duplicate(sharp(), sharp()))
        self.assertFalse(near_duplicate(sharp(), flat()))


class TestVoiceNotes(unittest.TestCase):
    def test_hinglish_extraction(self):
        fs = parse_notes("Front bumper pe halka scratch hai. Left door pe bada dent hai.")
        by_part = {f.part: f for f in fs}
        self.assertEqual(by_part["bumper"].condition, "scratch")
        self.assertEqual(by_part["bumper"].severity, "minor")
        self.assertEqual(by_part["door"].severity, "major")

    def test_ok_parts_recorded(self):
        fs = parse_notes("Bonnet theek hai.")
        self.assertEqual(fs[0].condition, "ok")

    def test_dedupe_keeps_worst(self):
        fs = parse_notes("Tyre worn hain. Front tyre ghis gaya hai major.")
        tyres = [f for f in fs if f.part == "tyre" and f.condition == "wear"]
        self.assertEqual(len(tyres), 1)
        self.assertEqual(tyres[0].severity, "major")

    def test_quotes_preserved(self):
        fs = parse_notes("Windshield pe chhota crack hai")
        self.assertIn("crack", fs[0].quote)


class TestReport(unittest.TestCase):
    def test_grade_and_estimate(self):
        fs = parse_notes("Left front door pe bada dent hai zyada. Bumper halka scratch.")
        r = build("Swift 2019", 60000, fs, [])
        self.assertEqual(r.status, "UNVERIFIED_INSPECTOR_NOTES")
        self.assertIn("major", r.summary_en)
        self.assertFalse(hasattr(r, "repair_estimate_inr"))



if __name__ == "__main__":
    unittest.main()
