"""ISUP Grade Group mapping for already assigned biopsy Gleason patterns.

This lookup does not interpret images, estimate patterns, or provide diagnoses.
"""
from dataclasses import dataclass

_GROUPS = {
    (3, 3): 1, (3, 4): 2, (4, 3): 3,
    (4, 4): 4, (3, 5): 4, (5, 3): 4,
    (4, 5): 5, (5, 4): 5, (5, 5): 5,
}


@dataclass(frozen=True)
class GleasonResult:
    primary_pattern: int
    secondary_pattern: int
    gleason_score: int
    grade_group: int


def grade_group(primary: int, secondary: int) -> GleasonResult:
    """Map assigned patterns 3-5 to ISUP Grade Group 1-5."""
    if type(primary) is not int or type(secondary) is not int:
        raise ValueError("Gleason patterns must be integers in {3, 4, 5}")
    try:
        group = _GROUPS[(primary, secondary)]
    except KeyError as exc:
        raise ValueError("Gleason patterns must be integers in {3, 4, 5}") from exc
    return GleasonResult(primary, secondary, primary + secondary, group)
