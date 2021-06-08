from cohortextractor import codelist_from_csv

sbp_codelist = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)

cholesterol_codelist = codelist_from_csv(
    "codelists/opensafely-cholesterol-tests.csv",
    system="snomed",
    column="code",
)
