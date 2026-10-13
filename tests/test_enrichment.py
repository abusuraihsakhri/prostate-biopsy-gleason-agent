"""
Automated Pytest for prostate-biopsy-gleason-agent Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    OverviewEngine,
    Enrichment1GleasonGradeGroupGgg15ClassificationAgent,
    GradeGroupImplementationEngine,
    Enrichment2Gs7SubtypeDetection34Vs43Engine,
    Gs7SubtypeImplementationEngine,
    Enrichment3Who2019ProtocolComplianceCheckerEngine,
    WhoComplianceImplementationEngine,
    Enrichment4NumberOfCoresWithPattern4TrackingEngine,
    ProstatebiopsygleasonagentEnrichmentSuite,
    enrichment_suite,
)

def test_enrichment_suite_execution():
    suite = ProstatebiopsygleasonagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    # All 8 engines should produce results (no duplicate key overwrites)
    assert len(res) == 8
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = ProstatebiopsygleasonagentEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_enrichment_suite_unique_keys():
    """Verify all enrichment suite result keys are unique (no duplicate overwrites)."""
    suite = ProstatebiopsygleasonagentEnrichmentSuite()
    res = suite.execute_all(primary_val=1.5, secondary_val=0.5)
    expected_keys = {
        "Overview", "GradeGroupClassifier", "GradeGroupImplementation",
        "Gs7Subtype", "Gs7SubtypeImplementation",
        "WhoCompliance", "WhoComplianceImplementation",
        "Pattern4Tracker",
    }
    assert set(res.keys()) == expected_keys

@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
def test_enrichment_rejects_nonfinite_metrics(invalid):
    with pytest.raises(ValueError):
        enrichment_suite.execute_all(primary_val=invalid, secondary_val=0.2)
    with pytest.raises(ValueError):
        enrichment_suite.execute_all(primary_val=1.0, secondary_val=invalid)
