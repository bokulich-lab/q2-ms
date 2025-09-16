# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import json
import os
import tempfile
import warnings

import numpy as np
import pandas as pd

from q2_ms.types import XCMSExperimentDirFmt
from q2_ms.utils import run_r_script
from q2_ms.xcms.utils import create_fake_spectra_files


def partition_xcms_experiment(
    xcms_experiment: XCMSExperimentDirFmt,
    num_partitions: int | None = None,
) -> XCMSExperimentDirFmt:
    # Get sample names
    sample_data_fp = os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt")
    sample_data = pd.read_csv(sample_data_fp, sep="\t")
    sample_names = (
        sample_data["spectraOrigin"]
        .apply(lambda x: os.path.splitext(os.path.basename(x))[0])
        .tolist()
    )
    num_samples = len(sample_names)

    # Validate num_partitions
    if num_partitions is None:
        num_partitions = num_samples
    elif num_partitions > num_samples:
        warnings.warn(
            f"You have requested a number of partitions '{num_partitions}' that is "
            f"greater than your number of samples '{num_samples}.' Your data will be "
            f"partitioned by sample into '{num_samples}' partitions."
        )
        num_partitions = num_samples

    index_partitions = [
        list(g) for g in np.array_split(list(range(num_samples)), num_partitions)
    ]

    # Create a dictionary to hold the partitions
    partitioned_experiments = {}
    all_paths = []
    for i, indices in enumerate(index_partitions, 1):
        fmt = XCMSExperimentDirFmt()
        all_paths.append(str(fmt))
        key = i if num_partitions != num_samples else sample_names[indices[0]]
        partitioned_experiments[key] = fmt

    # Run the R file
    with tempfile.TemporaryDirectory() as fake_spectra:
        create_fake_spectra_files(str(xcms_experiment), fake_spectra)

        params = {
            "xcms_experiment": str(xcms_experiment),
            "output_paths": json.dumps(all_paths),
            "partition_indices": json.dumps(
                [list(map(int, group)) for group in index_partitions]
            ),
            "fake_spectra": str(fake_spectra),
        }

        run_r_script(
            params=params, script_name="partition_xcms_experiment", package_name="XCMS"
        )

    return partitioned_experiments
