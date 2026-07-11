from pydantic import BaseModel, Field


class QAAnalysis(BaseModel):
    """Structured QA analysis of a requirement or PR description."""

    summary: str = Field(description="One or two sentence summary of what this change does")

    what_to_verify: list[str] = Field(
        description="Specific things QA should manually verify or check"
    )

    apis_changed: list[str] = Field(
        description="APIs, endpoints, or services likely affected. Empty list if none identified."
    )

    regression_risk_areas: list[str] = Field(
        description="Existing features that could break due to this change"
    )

    smoke_tests: list[str] = Field(
        description="Minimal set of critical tests to run before any deeper testing"
    )

    risk_level: str = Field(
        description="Overall risk level: Low, Medium, or High"
    )


class AmbiguityCheck(BaseModel):
    """Structured analysis of ambiguity/gaps in a requirement."""

    clarity_score: str = Field(
        description="Overall clarity rating: Clear, Mostly Clear, or Ambiguous"
    )

    ambiguous_points: list[str] = Field(
        description="Specific phrases or statements that are vague, unclear, or open to interpretation"
    )

    missing_details: list[str] = Field(
        description="Important details that seem to be missing entirely (e.g. error handling, limits, permissions)"
    )

    clarifying_questions: list[str] = Field(
        description="Specific questions a QA engineer or BA should ask the requirement author before development starts"
    )

    assumptions_if_unclarified: list[str] = Field(
        description="Reasonable assumptions a developer might make if these ambiguities aren't resolved, which could lead to bugs"
    )