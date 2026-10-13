"""
Clinical Algorithmic Engine & Guideline Rules for ProstateBiopsy Gleason Sentinel: Autonomous Multi-Core ISUP Grade Grouping & Perineural Tracker.
Domain: Digital Pathology
Standard: CAP Cancer Protocols & ASCO/CAP 2023
"""
from typing import Dict, Any, List, Optional
from .models import ClinicalCasePayload, AgentAlert, UrgencyLevel, ClinicalIntegrityStatus


class ClinicalDomainEngine:
    GUIDELINE = "Unvalidated demonstration thresholds"
    PRIMARY_BASELINE_LIMIT = 20.0
    SECONDARY_ALERT_LIMIT = 10.0

    @classmethod
    def evaluate_primary_index(cls, value: float) -> Optional[Dict[str, Any]]:
        if value > cls.PRIMARY_BASELINE_LIMIT:
            return {
                "title": "Primary Metric Threshold Exceeded",
                "finding": f"Observed value ({value:.2f}) exceeds configured demonstration threshold ({cls.PRIMARY_BASELINE_LIMIT:.1f}).",
                "recommendation": "Review the recorded metric and demonstration threshold.",
            }
        return None

    @classmethod
    def evaluate_secondary_kinetics(cls, value: float, is_stat: bool) -> Optional[Dict[str, Any]]:
        if value > cls.SECONDARY_ALERT_LIMIT or is_stat:
            return {
                "title": "STAT Kinetic Escalation Triggered",
                "finding": f"Kinetic parameter ({value:.2f}) with STAT={is_stat} requires prioritized supervision.",
                "recommendation": "Review this demonstration alert manually. No clinical notification is performed.",
            }
        return None

    @classmethod
    def evaluate_biomarker_concordance(cls, status_flag: str, biomarkers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        status_upper = str(status_flag).upper()
        if "DISCORDANT" in status_upper or "EQUIVOCAL" in status_upper or "MUTANT" in status_upper:
            return {
                "title": "Phenotypic / Biomarker Discordance Identified",
                "finding": f"Status flag '{status_flag}' indicates divergence from standard diagnostic concordance.",
                "recommendation": f"Review the status descriptor; do not infer a testing recommendation from this flag.",
            }
        return None
