"""
Automated Pytest for prostate_biopsy_gleason_agent package (clinical domain models & coordinator).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from prostate_biopsy_gleason_agent.models import (
    ClinicalCasePayload,
    AgentAlert,
    UrgencyLevel,
    ClinicalIntegrityStatus,
)
from prostate_biopsy_gleason_agent.agents import (
    CoreMeasurementAgent,
    GleasonPatternClassifierAgent,
    ISUPGradeGroupSynthesizerAgent,
    BiopsyCoordinator,
)
from prostate_biopsy_gleason_agent.engine import ClinicalDomainEngine
from prostate_biopsy_gleason_agent.cli import main


def test_clinical_case_payload_creation():
    case = ClinicalCasePayload(
        case_id="CASE-TEST-001",
        patient_synthetic_id="SYNTH-01",
        primary_metric=15.0,
        secondary_metric=5.0,
        status_flag="NORMAL",
    )
    assert case.case_id == "CASE-TEST-001"
    assert case.is_stat is False
    assert case.timestamp != ""


def test_core_measurement_agent():
    agent = CoreMeasurementAgent()
    case = ClinicalCasePayload(
        case_id="CASE-001",
        patient_synthetic_id="SYNTH-01",
        primary_metric=25.0,  # exceeds 20.0 threshold
        secondary_metric=5.0,
        status_flag="NORMAL",
    )
    alerts = agent.audit(case)
    assert len(alerts) == 1
    assert alerts[0].sub_agent == "CoreMeasurementAgent"
    assert alerts[0].urgency == UrgencyLevel.WARNING


def test_core_measurement_agent_normal():
    agent = CoreMeasurementAgent()
    case = ClinicalCasePayload(
        case_id="CASE-002",
        patient_synthetic_id="SYNTH-02",
        primary_metric=15.0,  # below 20.0 threshold
        secondary_metric=5.0,
        status_flag="NORMAL",
    )
    alerts = agent.audit(case)
    assert len(alerts) == 0


def test_gleason_pattern_agent_stat():
    agent = GleasonPatternClassifierAgent()
    case = ClinicalCasePayload(
        case_id="CASE-003",
        patient_synthetic_id="SYNTH-03",
        primary_metric=10.0,
        secondary_metric=5.0,
        status_flag="NORMAL",
        is_stat=True,
    )
    alerts = agent.audit(case)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.STAT_CRITICAL


def test_isup_grade_group_agent_discordant():
    agent = ISUPGradeGroupSynthesizerAgent()
    case = ClinicalCasePayload(
        case_id="CASE-004",
        patient_synthetic_id="SYNTH-04",
        primary_metric=10.0,
        secondary_metric=5.0,
        status_flag="DISCORDANT",
    )
    alerts = agent.audit(case)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.ADVISORY


def test_biopsy_coordinator_normal():
    coord = BiopsyCoordinator()
    case = ClinicalCasePayload(
        case_id="CASE-NORMAL-001",
        patient_synthetic_id="SYNTH-N01",
        primary_metric=10.0,
        secondary_metric=3.0,
        status_flag="NORMAL",
    )
    dossier = coord.process_case(case)
    assert dossier["overall_status"] == ClinicalIntegrityStatus.CONCORDANT_NORMAL.value
    assert dossier["total_alerts"] == 0


def test_biopsy_coordinator_critical():
    coord = BiopsyCoordinator()
    case = ClinicalCasePayload(
        case_id="CASE-CRIT-001",
        patient_synthetic_id="SYNTH-C01",
        primary_metric=25.0,
        secondary_metric=15.0,
        status_flag="DISCORDANT",
        is_stat=True,
    )
    dossier = coord.process_case(case)
    assert dossier["overall_status"] == ClinicalIntegrityStatus.CRITICAL_ACTION_REQUIRED.value
    assert dossier["stat_critical_alerts"] > 0


def test_coordinator_case_registry():
    coord = BiopsyCoordinator()
    case = ClinicalCasePayload(
        case_id="CASE-REG-001",
        patient_synthetic_id="SYNTH-R01",
        primary_metric=10.0,
        secondary_metric=3.0,
        status_flag="NORMAL",
    )
    coord.process_case(case)
    assert "CASE-REG-001" in coord.case_registry


def test_coordinator_chat_status():
    coord = BiopsyCoordinator()
    coord.case_registry["TEST"] = {}
    ans = coord.query_supervisory_chat("What is the status?")
    assert "tracking" in ans


def test_coordinator_chat_guidelines():
    coord = BiopsyCoordinator()
    ans = coord.query_supervisory_chat("What are the guidelines?")
    assert "CAP" in ans


def test_clinical_domain_engine_primary():
    res = ClinicalDomainEngine.evaluate_primary_index(25.0)
    assert res is not None
    assert "exceeds" in res["finding"]


def test_clinical_domain_engine_secondary_stat():
    res = ClinicalDomainEngine.evaluate_secondary_kinetics(5.0, is_stat=True)
    assert res is not None
    assert "STAT" in res["title"]


def test_clinical_domain_engine_biomarker_discordance():
    res = ClinicalDomainEngine.evaluate_biomarker_concordance("DISCORDANT", {})
    assert res is not None
    assert "discordance" in res["title"].lower() or "divergence" in res["finding"].lower()


def test_cli_audit():
    assert main(["audit", "--case-id", "CLI-PKG-01"]) == 0


def test_cli_chat():
    assert main(["chat", "What", "is", "the", "status?"]) == 0


def test_alert_to_dict():
    alert = AgentAlert(
        alert_id="TEST-001",
        sub_agent="TestAgent",
        urgency=UrgencyLevel.WARNING,
        title="Test",
        clinical_finding="Test finding",
        actionable_recommendation="Test recommendation",
    )
    d = alert.to_dict()
    assert d["alert_id"] == "TEST-001"
    assert d["urgency"] == "WARNING"
