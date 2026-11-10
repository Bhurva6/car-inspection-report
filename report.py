"""Offline prototype. See README.md for scope and limitations."""
import json
from dataclasses import dataclass, asdict

@dataclass
class InspectionReport:
    vehicle: str
    odometer_km: int
    findings: list
    photo_issues: list
    summary_en: str
    status: str = "UNVERIFIED_INSPECTOR_NOTES"

def build(vehicle, odometer_km, findings, photo_issues):
    major = sum(f.severity == "major" for f in findings)
    minor = sum(f.severity == "minor" for f in findings)
    summary = (f"{vehicle}: {major} major and {minor} minor observations in supplied text. "
               "Severity is copied from the note, not independently assessed. "
               "Photos in this demo are synthetic arrays; no damage model is connected. "
               "No grade, roadworthiness judgment or repair estimate is available.")
    return InspectionReport(vehicle, odometer_km, [asdict(f) for f in findings], photo_issues, summary)

def to_json(r):
    return json.dumps(asdict(r), indent=2, ensure_ascii=False)
