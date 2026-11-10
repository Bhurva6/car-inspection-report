"""Offline prototype. See README.md for scope and limitations."""
import numpy as np
from photo_gate import assess, near_duplicate
from voice_notes import parse_notes
from report import build, to_json

rng = np.random.default_rng(7)


def synth_photo(kind: str) -> np.ndarray:
    if kind == "sharp":
        img = np.zeros((200, 300, 3))
        img[::4, :, :] = 180          # high-frequency texture = sharp
        img[:, ::5, :] += 60
        return img.clip(0, 255)
    if kind == "blurry":
        return np.full((200, 300, 3), 127.0)   # flat = no gradients
    if kind == "dark":
        return np.full((200, 300, 3), 18.0)
    raise ValueError(kind)


VOICE_NOTE = """
Front bumper pe halka scratch hai, minor. Bonnet theek hai.
Left front door pe bada dent hai, zyada major lag raha hai.
Windshield pe chhota crack hai driver side.
Tyre worn hain, front tyres ghis gaye hain major.
Engine se halki awaz aa rahi hai thoda, noise minor.
Interior saaf hai, seats theek. Roof ok.
"""


def main():
    photos = {"front_bumper.jpg": "sharp", "bonnet.jpg": "sharp",
              "left_door.jpg": "blurry", "odometer.jpg": "dark"}
    print("=== PHOTO GATE ===")
    issues = []
    for name, kind in photos.items():
        v = assess(name, synth_photo(kind))
        print(f"{'OK ' if v.usable else 'RETAKE'} {name}: " +
              ("usable" if v.usable else "; ".join(v.issues)))
        issues += [f"{name}: {i}" for i in v.issues]
    dup = near_duplicate(synth_photo("sharp"), synth_photo("sharp"))
    print(f"duplicate check (same photo twice): {'DUPLICATE' if dup else 'distinct'}")

    print("\n=== VOICE NOTE FINDINGS ===")
    findings = parse_notes(VOICE_NOTE)
    for f in findings:
        print(f"[{f.severity:5s}] {f.part:12s} {f.condition:10s} <- \"{f.quote}\"")

    print("\n=== REPORT ===")
    rep = build("Maruti Swift VXi 2019", 61240, findings, issues)
    print(to_json(rep))


if __name__ == "__main__":
    main()
