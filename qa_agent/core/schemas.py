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

class APITestCase(BaseModel):
    """A single API test case."""

    endpoint: str = Field(description="The endpoint and method, e.g. 'POST /users/login'")
    scenario: str = Field(description="What this test verifies")
    expected_status: str = Field(description="Expected HTTP status code, e.g. '200', '400', '401'")
    notes: str = Field(description="Any important details: required headers, payload shape, auth needs, etc.")


class APITestSuite(BaseModel):
    """A set of API test cases generated from a spec."""

    test_cases: list[APITestCase] = Field(
        description="API test cases covering positive, negative, auth, and validation scenarios"
    )

    untested_risk_areas: list[str] = Field(
        description="Notable risk areas in the spec that deserve extra attention (e.g. endpoints handling sensitive data, missing rate limiting, etc.)"
    )

class RegressionImpact(BaseModel):
    """Analysis of downstream regression impact from code changes."""

    summary: str = Field(description="One or two sentence summary of the change's overall impact")

    directly_changed_areas: list[str] = Field(
        description="Features/functionality directly affected by the changed files themselves"
    )

    downstream_impact: list[str] = Field(
        description="Features/functionality that could break due to dependent files, even though not directly edited"
    )

    regression_test_scope: list[str] = Field(
        description="Specific test cases/areas that should be run to catch regressions from this change, prioritized by risk"
    )

    risk_level: str = Field(description="Overall regression risk: Low, Medium, or High")
    

class RootCauseAnalysis(BaseModel):
    """Analysis of the likely root cause of a bug, error, or test failure."""

    likely_causes: list[str] = Field(
        description="Most probable root causes, ranked from most to least likely, grounded in the actual code where possible"
    )

    affected_code_areas: list[str] = Field(
        description="Specific functions, files, or lines that are likely involved"
    )

    debugging_steps: list[str] = Field(
        description="Concrete next steps to confirm the root cause (e.g. what to log, what to check, what to reproduce)"
    )

    confidence: str = Field(
        description="Confidence in this diagnosis: High, Medium, or Low — Low if the error text/code alone isn't enough to be sure"
    )

    related_test_gaps: list[str] = Field(
        description="If this bug reveals a testing gap, what test(s) would have caught it earlier"
    )