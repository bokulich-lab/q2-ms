import os

import pandas as pd


def create_fake_mzml_files(xcms_experiment_path, tmp_dir):
    """
    Create empty mzML files filenames in a temp directory that are present in the
    'ms_experiment_sample_data.txt' file of an exported xcms experiment. This is
    needed to import an xcms experiment object without providing the original mzML
    files.

       Args:
        xcms_experiment_path (str): Path to the XCMSExperiment.
        tmp_dir (str): Path to the temp directory.
    """
    sample_data_path = os.path.join(
        xcms_experiment_path, "ms_experiment_sample_data.txt"
    )
    file_paths = pd.read_csv(
        sample_data_path, sep="\t", index_col=0, usecols=["spectraOrigin"]
    ).squeeze()
    for path in file_paths:
        with open(os.path.join(tmp_dir, os.path.basename(path)), "w"):
            pass
