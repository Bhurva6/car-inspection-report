"""Offline prototype. See README.md for scope and limitations."""
import numpy as np
from dataclasses import dataclass


@dataclass
class PhotoVerdict:
    path: str
    usable: bool
    blur_score: float
    brightness: float
    issues: list


def _gradient_var(gray: np.ndarray) -> float:
    gx = np.diff(gray.astype(float), axis=1)
    gy = np.diff(gray.astype(float), axis=0)
    return float(gx.var() + gy.var())


def assess(path: str, rgb: np.ndarray, blur_min: float = 50.0,
           dark_max: float = 40.0, bright_min: float = 220.0) -> PhotoVerdict:
    gray = rgb.mean(axis=2)
    blur = _gradient_var(gray)
    bright = float(gray.mean())
    issues = []
    if blur < blur_min:
        issues.append(f"too blurry (sharpness {blur:.0f} < {blur_min:.0f}); retake holding the phone steady")
    if bright < dark_max:
        issues.append(f"too dark (mean {bright:.0f}); retake in daylight or with flash")
    if bright > bright_min:
        issues.append("overexposed; avoid direct glare on the panel")
    return PhotoVerdict(path, not issues, blur, bright, issues)


def near_duplicate(a: np.ndarray, b: np.ndarray, thresh: float = 0.98) -> bool:
    """Histogram-correlation duplicate check for repeated uploads."""
    ha = np.histogram(a, bins=32, range=(0, 256))[0].astype(float)
    hb = np.histogram(b, bins=32, range=(0, 256))[0].astype(float)
    ha /= ha.sum() or 1
    hb /= hb.sum() or 1
    corr = float(np.corrcoef(ha, hb)[0, 1])
    return corr >= thresh
