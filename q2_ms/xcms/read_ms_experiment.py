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

    if sample_metadata is not None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Validate sample metadata IDs
            sample_metadata_table = sample_metadata.to_dataframe()
            _validate_metadata(sample_metadata_table, str(spectra))

            # Save sample metadata to tsv
            tsv_path = os.path.join(tmp_dir, "sample_metadata.tsv")
            sample_metadata_table.to_csv(tsv_path, sep="\t")

            params["sample_metadata"] = tsv_path

            # Run R script
            run_r_script(params, "read_ms_experiment", "XCMS")
    else:
        run_r_script(params, "read_ms_experiment", "XCMS")

    return xcms_experiment


def _validate_metadata(metadata, spectra_path):
    metadata_set = set(metadata.index.astype(str))

    spectra_set = {
        os.path.splitext(f)[0]
        for f in os.listdir(spectra_path)
        if os.path.isfile(os.path.join(spectra_path, f))
    }

    missing_in_metadata = spectra_set - metadata_set
    missing_in_spectra = metadata_set - spectra_set

    if missing_in_metadata or missing_in_spectra:
        error_message = (
            "There is a mismatch of sample ids in the provided spectra "
            "and sample-metadata:\n"
        )
        if missing_in_metadata:
            error_message += (
                f"IDs in spectra but missing in sample-metadata: "
                f"{missing_in_metadata}\n"
            )
        if missing_in_spectra:
            error_message += (
                f"IDs in sample-metadata but missing in spectra: "
                f"{missing_in_spectra}\n"
            )

        raise ValueError(error_message.strip())
