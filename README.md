# Used-car inspection-notes prototype

An offline prototype that turns **written Hinglish notes** into structured
observations with exact quotes. A separate NumPy photo-quality heuristic
checks sharpness, brightness and histogram similarity on synthetic arrays.
No speech recognition, vision model or automated damage detection is wired.

## Run

Python 3.10+, NumPy:

```sh
python3 -m pip install -r requirements.txt
python3 inspect_cli.py
python3 -m unittest discover -s . -v
```

8 unit tests exercise the demo heuristics. The inputs are invented written
notes and generated pixel arrays, not a real inspection or vehicle photo set.
The CLI does not yet ingest real image or audio files. No API key needed.

## What the report means

Part, condition and severity are extracted by small keyword lists, not
independently assessed. Unrecognised wording may be missed; ambiguous
negation is skipped for review. This is not a roadworthiness judgment,
vehicle certification, mechanical diagnosis or repair quotation. It does
not assign a quality grade or estimate cost. A histogram match can falsely
call two different photos duplicates; blur/exposure thresholds are not
calibrated against a real inspection dataset.

Next: actual image/audio file inputs, a speech adapter, evaluated visual
findings and a human-reviewed evidence workflow. No models trained or
fine-tuned. No customer or real inspection data used.
