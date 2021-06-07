from cohortextractor import Measure, StudyDefinition, patients

from codelists import sbp_codelist

# We use these dates when we define the study population. Rather than type them
# "longhand" each time, we type them "shorthand", which reduces the risk of making
# a mistake.
EARLIEST = "index_date"
LATEST = "last_day_of_month(index_date)"
BETWEEN = [EARLIEST, LATEST]

# This is where we define the study population.
study = StudyDefinition(
    # Default characteristics of expected, or "dummy", data
    default_expectations={
        "date": {"earliest": EARLIEST, "latest": LATEST},
        "rate": "uniform",
        "incidence": 1,
    },
    # The study date
    index_date="2019-01-01",
    # The study population. Because `registered` and `died` are binary variables,
    # (see below) you can read this as "Include in the study population patients
    # who are registered and who haven't died."
    population=patients.satisfying("registered AND NOT died"),
    # Was the patient registered on the given date?
    registered=patients.registered_as_of(reference_date="index_date"),
    # Had the patient died on or before the given date?
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    # What was the patient's registered practice on the given date?
    practice=patients.registered_practice_as_of(
        date="index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}
        },
    ),
    # Did the patient experience a clinical event from the given codelist between
    # the given dates?
    had_sbp_event=patients.with_these_clinical_events(
        codelist=sbp_codelist,
        between=BETWEEN,
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    # What clinical event was it?
    sbp_event_code=patients.with_these_clinical_events(
        codelist=sbp_codelist,
        between=BETWEEN,
        returning="code",
        return_expectations={
            "category": {"ratios": {x: 1 / len(sbp_codelist) for x in sbp_codelist}},
            "incidence": 0.1,
        },
    ),
)

# This is where we define measures using the study population. A measure is
# the value of a numerator divided by a denominator for a given group of patients.
measures = [
    Measure(
        id="sbp_by_practice",
        numerator="had_sbp_event",
        denominator="population",
        group_by=["practice"],
    ),
]
