import copy

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_r_script


def group_peaks_density(
    spectra: mzMLDirFmt,
    xcms_experiment: XCMSExperimentDirFmt,
    bw: float = 30,
    min_fraction: float = 0.5,
    min_samples: float = 1,
    bin_size: float = 0.25,
    max_features: float = 50,
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
    run_r_script(params, "group_peaks_density", "XCMS")

    return xcms_experiment
