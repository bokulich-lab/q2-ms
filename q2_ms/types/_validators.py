# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
from qiime2.core.exceptions import ValidationError
from qiime2.core.type import Properties

from q2_ms.plugin_setup import plugin
from q2_ms.types import XCMSExperiment, XCMSExperimentDirFmt


@plugin.register_validator(XCMSExperiment % Properties("MS2"))
def validate_xcms_experiment_ms2(data: XCMSExperimentDirFmt, level):
    """
    Validates that the XCMSExperiment contains MS2-level spectra. Checks for any "2"
    values in the "msLevel" column in the file "ms_backend_data.txt".
    """
    df = pd.read_csv(
        os.path.join(data.path, "ms_backend_data.txt"),
        sep="\t",
        usecols=["msLevel"],
        skiprows=1,
        index_col=0,
    )
    if not (df["msLevel"] == 2).any():
        raise ValidationError(
            "The property 'MS2' requires MS2-level spectra to be present in the "
            "XCMSExperiment."
        )


@plugin.register_validator(XCMSExperiment % Properties("peaks"))
def validate_xcms_experiment_peaks(data: XCMSExperimentDirFmt, level):
    """
    Validates that required chromatographic peak files exist in the XCMSExperiment.
    """
    files = ["xcms_experiment_chrom_peaks.txt", "xcms_experiment_chrom_peak_data.txt"]
    if not any(os.path.exists(os.path.join(data.path, f)) for f in files):
        raise ValidationError(
            "The property 'peaks' requires the two files "
            "'xcms_experiment_chrom_peaks.txt' and "
            "'xcms_experiment_chrom_peak_data.txt' to be present in the "
            "XCMSExperiment. To identify chromatographic peaks use the action "
            "'find-chrom-peaks-centwave'."
        )


@plugin.register_validator(XCMSExperiment % Properties("features"))
def validate_xcms_experiment_features(data: XCMSExperimentDirFmt, level):
    """
    Validates that required feature grouping files exist in the XCMSExperiment.
    """
    files = [
        "xcms_experiment_feature_definitions.txt",
        "xcms_experiment_feature_peak_index.txt",
    ]
    if not any(os.path.exists(os.path.join(data.path, f)) for f in files):
        raise ValidationError(
            "The property 'features' requires the two files "
            "'xcms_experiment_feature_definitions.txt' and "
            "'xcms_experiment_feature_peak_index.txt' to be present in the "
            "XCMSExperiment. To group peaks into features use the action "
            "'group-chrom-peaks-density'."
        )
