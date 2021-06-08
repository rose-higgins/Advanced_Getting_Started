# Walk-through

## Getting started

Start a new Gitpod workspace:

* <https://gitpod.io/#https://github.com/opensafely/sro-measures-demo>

Generate expected, or "dummy", data:

* Expand the *output* directory; notice that it's empty
* Run:

```sh
opensafely run -f run_all
```

* Expand the *output* directory; notice that it's not empty any more!
* It contains three types of files:
  * input files (e.g. *output/input_2019-01-01.csv*)
  * measure files (e.g. *output/measure_sbp_by_practice.csv*)
  * a deciles chart file

Inspect *project.yaml*:

* It contains three actions; each action produces the types of files we saw above:
  * The `generate_cohort` action generates the input files from the study definition
  * The `generate_measures` action generates the measure files from the study definition
  * The `generate_deciles_charts` action generates the deciles chart file

Compare the columns in an input file to the study definition:

* It's easiest to do this side-by-side
* Notice that the columns are parameter names of the `StudyDefinition` instance
* Notice the `default_expectations` parameter

Compare the columns in a measure file to the study definition:

* It's easiest to do this side-by-side
* Notice that the columns are parameter values of the `Measure` instance
* Notice the additional `value` and `date` columns

Inspect the deciles chart file:

* TODO

## Adding a new covariate

Inspect a codelist on [OpenCodelists][]:

* <https://www.opencodelists.org/codelist/opensafely/cholesterol-tests/09896c09/>

Inspect *codelists/codelists.txt*:

* Add `opensafely/cholesterol-tests/09896c09`
* Run:

```sh
opensafely codelists update
```

Inspect *analysis/study_definition.py*:

* Copy `had_sbp_event` and `sbp_event_code`
* Rename them `had_cholesterol_event` and `cholesterol_event_code`
* Replace `sbp_codelist` with `cholesterol_codelist`

Regenerate expected, or "dummy", data:

* Run:

```sh
opensafely run -f run_all
```

Inspect an input file:

* Notice two new columns: `had_cholesterol_event` and `cholesterol_event_code`

## Adding a new measure

Inspect *analysis/study_definition.py*:

* Copy `Measure`
* Replace `sbp_by_practice` with `cholesterol_by_practice`
* Replace `had_sbp_event` with `had_cholesterol_event`

Regenerate expected, or "dummy", data:

* Run:

```sh
opensafely run -f run_all
```

* Notice that there are new measure files

Compare the columns in a new measure file to the study definition:

* It's easiest to do this side-by-side
* Notice that the columns are parameter values of the new `Measure` instance
* Notice the additional `value` and `date` columns

Inspect the deciles chart file:

* TODO

## TODO

* Data Preview is broken on Firefox - should we depend upon it?
* [Vega Viewer][] isn't in the marketplace - should we use Matplotlib rather than Vega Lite?

[OpenCodelists]: https://www.opencodelists.org/
[Vega Viewer]: https://marketplace.visualstudio.com/items?itemName=RandomFractalsInc.vscode-vega-viewer
