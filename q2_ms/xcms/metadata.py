# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
from qiime2 import Metadata

from q2_ms.types import XCMSExperimentDirFmt


def chromatogram(
    ctx,
    xcms_experiment,
    x_measure,
    y_measure=None,
    replicate_method="none",
    group_by=None,
    title=None,
):
    lineplot = ctx.get_action("vizard", "lineplot")

    df = create_metadata(str(xcms_experiment.view(XCMSExperimentDirFmt)))

    vis = lineplot(
        Metadata(df), x_measure, y_measure, replicate_method, group_by, title
    )

    return tuple(vis)


def create_metadata(dir_fmt_path):
    # Read the backend data file while skipping the first line
    backend_df = pd.read_csv(
        os.path.join(dir_fmt_path, "ms_backend_data.txt"),
        sep="\t",
        skiprows=1,
        index_col=0,
    )

    # Read the sample data file
    sample_df = pd.read_csv(
        os.path.join(dir_fmt_path, "ms_experiment_sample_data.txt"), sep="\t"
    )
    sample_df.drop(columns=["spectraOrigin"], inplace=True)

    # Read the links file that maps sample indices to spectra indices.
    links_df = pd.read_csv(
        os.path.join(dir_fmt_path, "ms_experiment_sample_data_links_spectra.txt"),
        sep="\t",
        header=None,
        names=["sample_id", "spectra_index"],
    )

    # Merge the backend data with the links data using the spectra_index.
    merged_df = backend_df.join(links_df.set_index("spectra_index"), how="left")

    # Merge the merged_df with the sample_df using the sample_id.
    merged_df = merged_df.join(sample_df, on="sample_id")

    # Create new column that shows the difference between rtime and the adjusted rtime
    if "rtime_adjusted" in merged_df.columns:
        merged_df["rtime_adjusted-rtime"] = (
            merged_df["rtime_adjusted"] - merged_df["rtime"]
        )

    # Set index to str
    merged_df.index.name = "id"
    merged_df.index = merged_df.index.astype(str)

    # Set column centroided to str
    if "centroided" in merged_df.columns:
        merged_df["centroided"] = merged_df["centroided"].astype(str)

    return merged_df
