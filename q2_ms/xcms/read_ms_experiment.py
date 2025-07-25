# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
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

    # Init XCMSExperimentDirFmt
    xcms_experiment = XCMSExperimentDirFmt()

    # Add output path to params
    params["output_path"] = str(xcms_experiment)

    with tempfile.TemporaryDirectory() as tmp_dir:
        if sample_metadata is not None:
            # Validate sample metadata IDs
            sample_metadata_table = sample_metadata.to_dataframe()
            _validate_metadata(sample_metadata_table, str(spectra))

            # Save sample metadata to tsv and add to params
            tsv_path = os.path.join(tmp_dir, "sample_metadata.tsv")
            sample_metadata_table.to_csv(tsv_path, sep="\t")
            params["sample_metadata"] = tsv_path

        # Run R script
        run_r_script("read_ms_experiment", params, "XCMS")

    return xcms_experiment


def _validate_metadata(metadata, spectra_path):
    """
    Validates that sample IDs in the metadata match the filenames in the spectra
    directory.

    This function compares the sample IDs from the metadata with the filenames
    of files in the given spectra directory. It checks for any discrepancies
    between the two sets of sample IDs and raises a ValueError if mismatches are found.

    Parameters:
        metadata (pd.DataFrame):
            Metadata DataFrame whose index represents sample IDs.
        spectra_path (str):
            Path to the directory containing spectra files.

    Raises:
        ValueError:
            If there are sample IDs present in one input (metadata or spectra)
            but missing in the other.
    """
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
