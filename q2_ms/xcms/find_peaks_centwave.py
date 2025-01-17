import copy
import importlib
import subprocess

from qiime2 import Metadata

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_command


def find_peaks_centwave(
    mzml: mzMLDirFmt,
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

    # Convert metadata to json string
    params["sample_metadata"] = (
        params["sample_metadata"].to_dataframe().reset_index().to_json(orient="records")
    )

    # Innit XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Add output path to params
    params["output_path"] = str(xcms_experiment)

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

    try:
        run_command(cmd, verbose=True, cwd=None)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running XCMS, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )
