import copy
import importlib
import os
import subprocess

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_command


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
    run_find_chrom_peaks(params)

    return xcms_experiment


def run_find_chrom_peaks(params):
    script_path = str(
        importlib.resources.files("q2_ms") / "assets/adjust_retention_time_obiwarp.R"
    )
    cmd = ["/usr/local/bin/Rscript", "--vanilla", script_path]

    for key, value in params.items():
        if value is not None:
            cmd.extend([f"--{key}", str(value)])

    env = os.environ.copy()  # Copy the current environment variables
    env["PATH"] = "/usr/local/bin:" + env["PATH"]

    # Unset Conda-related R variables to prevent it from overriding the system R library
    for var in ["R_LIBS", "R_LIBS_USER", "R_HOME", "CONDA_PREFIX"]:
        env.pop(var, None)

    try:
        run_command(cmd, verbose=True, cwd=None, env=env)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running XCMS, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )
