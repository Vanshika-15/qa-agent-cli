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