import json
import re

import numpy
import pandas
import utils
from pandas import Series

MEASURE_FNAME_REGEX = re.compile(r"measure_(?P<id>\w+)\.csv")
DECILES = Series(numpy.arange(0.1, 1, 0.1), name="deciles")


def _get_denominator(measures_table):
    return measures_table.columns[-3]


def _get_group_by(measures_table):
    return list(measures_table.columns[:-4])


def get_measures_tables():
    for path in utils.OUTPUT_DIR.iterdir():
        measure_fname_match = re.match(MEASURE_FNAME_REGEX, path.name)
        if measure_fname_match is not None:
            # The `date` column is assigned by the measures framework.
            measures_table = pandas.read_csv(path, parse_dates=["date"])

            # We can reconstruct the parameters passed to `Measure` without
            # the study definition.
            measures_table.attrs["id"] = measure_fname_match.group("id")
            measures_table.attrs["denominator"] = _get_denominator(measures_table)
            measures_table.attrs["group_by"] = _get_group_by(measures_table)

            yield measures_table


def drop_rows(measures_table):
    return measures_table[measures_table[measures_table.attrs["denominator"]] > 0]


def get_deciles_table(measures_table):
    by = ["date"] + measures_table.attrs["group_by"][1:]
    deciles_table = measures_table.groupby(by)["value"].quantile(DECILES).reset_index()
    # `measures_table.attrs` isn't persisted.
    deciles_table.attrs = measures_table.attrs.copy()
    return deciles_table


def _to_records(deciles_table):
    _deciles_table = deciles_table.copy()
    _deciles_table["date"] = _deciles_table["date"].dt.strftime("%Y-%m-%dT00:00:00")
    return _deciles_table.to_dict("records")


def get_deciles_chart(deciles_table):
    chart = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "usermeta": deciles_table.attrs.copy(),
        "mark": "line",
        "encoding": {
            "x": {
                "type": "temporal",
                "field": "date",
            },
            "y": {
                "type": "quantitative",
                "field": "value",
            },
            "detail": {
                "type": "ordinal",
                "field": "deciles",
            },
        },
    }

    facets = deciles_table.columns[1:-2]
    if not facets.empty:
        assert len(facets) == 1, "We cannot facet by more than one column"  # FIXME
        chart["facet"] = {
            "row": {
                "field": f"{facets[0]}",
                "type": "nominal",
            },
        }

    chart["data"] = {
        "values": _to_records(deciles_table),
    }

    return chart


def write_deciles_chart(deciles_chart):
    id_ = deciles_chart["usermeta"]["id"]
    fname = f"deciles_chart_{id_}.vl.json"
    fpath = utils.OUTPUT_DIR / fname
    with open(fpath, "w", encoding="utf8") as f:
        json.dump(deciles_chart, f, indent=2)


def main():
    for measures_table in get_measures_tables():
        measures_table = drop_rows(measures_table)
        deciles_table = get_deciles_table(measures_table)
        deciles_chart = get_deciles_chart(deciles_table)
        write_deciles_chart(deciles_chart)


if __name__ == "__main__":
    main()
