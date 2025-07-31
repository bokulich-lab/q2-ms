# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
import qiime2
from qiime2.metadata.base import is_id_header

from q2_ms.types import XCMSExperimentDirFmt


def create_spectral_metadata(
    xcms_experiment: XCMSExperimentDirFmt, ms_level: str = "1"
) -> qiime2.Metadata:
    # Read the backend data file while skipping the first line
    backend_df = pd.read_csv(
        os.path.join(str(xcms_experiment), "ms_backend_data.txt"),
        sep="\t",
        skiprows=1,
        index_col=0,
    )

    # Read the sample data file
    sample_df = pd.read_csv(
        os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt"), sep="\t"
    )
    sample_df.drop(columns=["spectraOrigin"], inplace=True)

    # Read the links file that maps sample indices to spectra indices.
    links_df = pd.read_csv(
        os.path.join(
            str(xcms_experiment), "ms_experiment_sample_data_links_spectra.txt"
        ),
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

    # Adds "_" to column name if it is a reserved metadata index name
    merged_df.columns = [
        col + "_" if is_id_header(col) else col for col in merged_df.columns
    ]

    # Filter data by MS level
    merged_df = merged_df.loc[merged_df["msLevel"] == int(ms_level)]

    if ms_level == "1":
        # Drop columns that only contain information about MS2 scans
        columns_to_drop = [
            "precScanNum",
            "precursorMz",
            "precursorIntensity",
            "precursorCharge",
            "collisionEnergy",
            "isolationWindowLowerMz",
            "isolationWindowTargetMz",
            "isolationWindowUpperMz",
        ]
        merged_df.drop(
            columns=[col for col in columns_to_drop if col in merged_df.columns]
        )

    return qiime2.Metadata(merged_df)
