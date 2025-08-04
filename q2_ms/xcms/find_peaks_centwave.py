# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import copy

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_r_script


def find_peaks_centwave(
    spectra: mzMLDirFmt,
    xcms_experiment: XCMSExperimentDirFmt,
    ppm: float = 25,
    min_peak_width: float = 20,
    max_peak_width: float = 50,
    sn_thresh: float = 10,
    prefilter_k: float = 3,
    prefilter_i: float = 100,
    mz_center_fun: str = "wMean",
    integrate: int = 1,
    mz_diff: float = -0.001,
    fit_gauss: bool = False,
    noise: float = 0,
    first_baseline_check: bool = True,
    ms_level: int = 1,
    extend_length_msw: bool = False,
    verbose_columns: bool = False,
    verbose_beta_columns: bool = False,
    threads: int = 1,
) -> XCMSExperimentDirFmt:
    # Init XCMSExperimentDirFmt
    xcms_experiment_peaks = XCMSExperimentDirFmt()

    # Create parameters dict
    params = copy.copy(locals())

    # Run R script
    run_r_script("find_peaks_centwave", params, "XCMS")

    return xcms_experiment_peaks
