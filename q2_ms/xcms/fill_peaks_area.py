import copy

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_r_script


def fill_peaks_area(
    spectra: mzMLDirFmt,
    xcms_experiment: XCMSExperimentDirFmt,
    mz_min: str = "function(z) quantile(z, probs = 0.25)",
    mz_max: str = "function(z) quantile(z, probs = 0.75)",
    rt_min: str = "function(z) quantile(z, probs = 0.25)",
    rt_max: str = "function(z) quantile(z, probs = 0.75)",
    threads: int = 1,
    ms_level: int = 1,
) -> XCMSExperimentDirFmt:
    # Create parameters dict
    params = copy.copy(locals())

    # Innit XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Add output path to params
    params["output_path"] = str(xcms_experiment)

    # Run R script
    run_r_script(params, "fill_peaks_area", "XCMS")

    return xcms_experiment
