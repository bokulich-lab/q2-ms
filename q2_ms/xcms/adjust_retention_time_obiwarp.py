import copy

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_r_script


def adjust_retention_time_obiwarp(
    spectra: mzMLDirFmt,
    chromatographic_peaks: XCMSExperimentDirFmt,
    bin_size: float = 25,
    center_sample: int = None,
    response: float = 1,
    dist_fun: str = "cor_opt",
    gap_init: float = None,
    gap_extend: float = None,
    factor_diag: float = 2,
    factor_gap: float = 1,
    local_alignment: bool = False,
    init_penalty: float = 0,
    subset: int = None,
    subset_adjust: str = None,
    rtime_difference_threshold: float = 5,
    chunk_size: int = 1,
    threads: int = 1,
) -> XCMSExperimentDirFmt:
    # Create parameters dict
    params = copy.copy(locals())

    # Innit XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Add output path to params
    params["output_path"] = str(xcms_experiment)

    # Run R script
    run_r_script(params, "adjust_retention_time_obiwarp", "XCMS")

    return xcms_experiment
