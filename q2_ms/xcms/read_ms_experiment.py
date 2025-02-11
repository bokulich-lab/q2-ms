import copy
import os
import tempfile

from qiime2 import Metadata

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.utils import run_r_script


def read_ms_experiment(
    spectra: mzMLDirFmt,
    sample_metadata: Metadata = None,
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
        run_r_script(params, "read_ms_experiment", "XCMS")

    return xcms_experiment
