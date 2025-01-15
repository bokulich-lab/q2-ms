import copy
import subprocess

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_command


def find_peaks_xcms(
    mzML: mzMLDirFmt,
    ppm: float,
    min_peakwidth: str,
    max_peakwidth: str,
    snthresh: float,
    prefilter_k: str,
    prefilter_i: int,
    mz_center_fun: float,
    integrate: int,
    mzdiff: float,
    fitgauss: bool,
    noise: float,
    first_baseline_check: float,
    ms_level: int,
    threads: int,
) -> XCMSExperimentDirFmt:
    # Create parameters dict
    params = copy.deepcopy(locals())

    # Innit XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Run R script
    run_find_chrom_peaks(params)

    return xcms_experiment


def run_find_chrom_peaks(params):
    cmd = ["find_peaks_xcms.R"]
    for key, value in params.items():
        cmd.extend([f"--{key}", str(value)])

    try:
        run_command(cmd, verbose=True, cwd=None)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running XCMS, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )
