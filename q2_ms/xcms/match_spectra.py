# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import copy

from q2_ms.types import (
    MatchedSpectraDirFmt,
    MSPDirFmt,
    XCMSExperimentDirFmt,
    mzMLDirFmt,
)
from q2_ms.utils import run_r_script


def match_spectra(
    spectra: mzMLDirFmt,
    xcms_experiment: XCMSExperimentDirFmt,
    target_spectra: MSPDirFmt,
    map_fun: str = "join_peaks",
    tolerance: float = None,
    ppm: float = None,
    fun: str = "ndotproduct",
    fun_m: float = 0,
    fun_n: float = 0.5,
    fun_na_rm: bool = True,
    require_precursor: bool = True,
    require_precursor_peak: bool = False,
    thresh_fun: str = "function(x) which(x >= 0.7)",
    tolerance_rt: float = None,
    percent_rt: float = None,
    scale_peaks: bool = False,
    intensity_threshold: float = None,
    num_peaks_threshold: int = None,
    threads: int = 1,
) -> MatchedSpectraDirFmt:
    # Init MatchedSpectraDirFmt
    matched_spectra = MatchedSpectraDirFmt()

    # Create parameters dict
    params = copy.copy(locals())

    # Run R script
    run_r_script(params, "match_spectra", "MetaboAnnotation")

    return matched_spectra
