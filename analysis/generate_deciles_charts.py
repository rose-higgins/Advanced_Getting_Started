import re

import numpy
import pandas
import utils
from ebmdatalab import charts
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


def write_deciles_chart(measures_table):
    facets = measures_table.attrs["group_by"][1:]
    assert not facets, "Faceted deciles charts are not supported"  # FIXME

    plt = charts.deciles_chart(
        measures_table,
        "date",
        "value",
        show_outer_percentiles=False,
    )
    id_ = measures_table.attrs["id"]
    fname = f"deciles_chart_{id_}.png"
    fpath = utils.OUTPUT_DIR / fname
    plt.savefig(fpath, dpi=300, bbox_inches="tight")


def main():
    for measures_table in get_measures_tables():
        measures_table = drop_rows(measures_table)
        write_deciles_chart(measures_table)


if __name__ == "__main__":
    main()
