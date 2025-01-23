import copy
import importlib
import os
import subprocess
import tempfile

from qiime2 import Metadata

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_command


def find_peaks_centwave(
    spectra: mzMLDirFmt,
    sample_metadata: Metadata,
    ppm: float = 25,
    min_peakwidth: float = 20,
    max_peakwidth: float = 50,
    snthresh: float = 10,
    prefilter_k: float = 3,
    prefilter_i: float = 100,
    mz_center_fun: str = "wMean",
    integrate: int = 1,
    mzdiff: float = -0.001,
    fitgauss: bool = False,
    noise: float = 0,
    first_baseline_check: bool = True,
    ms_level: int = 1,
    threads: int = 1,
) -> XCMSExperimentDirFmt:
    # Create parameters dict
    params = copy.copy(locals())

    # Innit XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Add output path to params
    params["output_path"] = str(xcms_experiment)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tsv_path = os.path.join(tmp_dir, "sample_metadata.tsv")
        sample_metadata.to_dataframe().to_csv(tsv_path, sep="\t")
        params["sample_metadata"] = tsv_path

        # Run R script
        run_find_chrom_peaks(params)

    return xcms_experiment


def run_find_chrom_peaks(params):
    script_path = str(
        importlib.resources.files("q2_ms") / "assets/find_peaks_centwave.R"
    )
    cmd = ["/usr/local/bin/Rscript", "--vanilla", script_path]

    for key, value in params.items():
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
