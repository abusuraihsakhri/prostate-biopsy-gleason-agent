import math
import pytest
from pydantic import ValidationError as PydanticValidationError
from agents.base import AuditTrail
from agents.models import SystemTaskPayload
from prostate_biopsy_gleason_agent.models import ClinicalCasePayload
from prostate_biopsy_gleason_agent.parsing import parse_csv_bool
from prostate_biopsy_gleason_agent.grading import grade_group

@pytest.mark.parametrize("primary,secondary,score,group", [
    (3,3,6,1),(3,4,7,2),(4,3,7,3),(4,4,8,4),(3,5,8,4),
    (5,3,8,4),(4,5,9,5),(5,4,9,5),(5,5,10,5),
])
def test_grade_groups(primary,secondary,score,group):
    result = grade_group(primary,secondary)
    assert (result.gleason_score,result.grade_group)==(score,group)

@pytest.mark.parametrize("a,b", [(1,3),(2,2),(6,3),("3",4),(3.5,4),(True,5)])
def test_invalid_grade_patterns(a,b):
    with pytest.raises(ValueError): grade_group(a,b)

@pytest.mark.parametrize("raw,value", [("False",False),(" TRUE ",True),("0",False),("1",True),("no",False),("yes",True),("",False)])
def test_csv_flags(raw,value):
    assert parse_csv_bool(raw) is value

def test_invalid_csv_flag():
    with pytest.raises(ValueError): parse_csv_bool("maybe")

def test_audit_detects_entry_and_signature_tampering():
    audit = AuditTrail(secret_key="tests-only")
    audit.log("tester","unit","created",{"status":"OK"})
    audit.log("tester","unit","updated",{"status":"OK"})
    assert audit.verify_integrity()
    audit.get_trail()[0]["actor"]="external edit"
    assert audit.verify_integrity()
    audit.logs[0]["actor"]="tampered"
    assert not audit.verify_integrity()
    audit.logs[0]["actor"]="tester"
    audit.logs[1]["current_hash"]="0"*64
    assert not audit.verify_integrity()

@pytest.mark.parametrize("bad", [math.nan,math.inf,-math.inf])
def test_nonfinite_rejected(bad):
    with pytest.raises(PydanticValidationError):
        SystemTaskPayload(task_id="T",target_identifier="S",primary_metric=bad)
    with pytest.raises(ValueError):
        ClinicalCasePayload("CASE","SYNTH",bad,2.0,"NORMAL")
