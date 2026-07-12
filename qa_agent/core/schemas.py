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


class BugReport(BaseModel):
    """Structured bug report generated from a rough description."""

    title: str = Field(
        description="Concise, specific bug title suitable for a ticket (e.g. 'Login fails silently when password contains emoji')"
    )

    severity: str = Field(
        description="Severity: Critical, High, Medium, or Low"
    )

    steps_to_reproduce: list[str] = Field(
        description="Numbered, specific steps to reproduce the issue. Make reasonable inferences from the description; note any assumptions."
    )

    expected_result: str = Field(
        description="What should happen"
    )

    actual_result: str = Field(
        description="What actually happens, based on the description given"
    )

    environment_notes: list[str] = Field(
        description="Environment details that would be useful to capture (browser, OS, device, account type, etc.) — even if not specified, list what SHOULD be captured"
    )

    possible_root_cause: str = Field(
        description="A brief, informed guess at what might be causing this, useful context for the dev team. Say 'Unclear from description' if there isn't enough info."
    )


class PrioritizedTest(BaseModel):
    """A single test case with its assigned priority."""

    test_case: str = Field(description="The test case description")
    priority: str = Field(description="Priority: P0 (must run), P1 (should run), or P2 (nice to have)")
    reasoning: str = Field(description="Brief reason for this priority level")


class PrioritizationResult(BaseModel):
    """A ranked list of test cases by risk/importance."""

    prioritized_tests: list[PrioritizedTest] = Field(
        description="Test cases ranked from highest to lowest priority"
    )

    recommended_minimum: list[str] = Field(
        description="If time only allows a handful of tests, exactly which ones should run (by test_case text)"
    )


class CoverageGap(BaseModel):
    """Analysis comparing a requirement against existing test coverage."""

    already_covered: list[str] = Field(
        description="Aspects of the requirement that appear to already be tested by the existing test files"
    )

    coverage_gaps: list[str] = Field(
        description="Specific scenarios from the requirement that are NOT covered by existing tests"
    )

    suggested_new_tests: list[str] = Field(
        description="New test cases to write to close the identified gaps, described specifically enough to act on"
    )

    coverage_estimate: str = Field(
        description="Rough overall coverage assessment: e.g. 'Well covered', 'Partially covered', 'Largely untested'"
    )