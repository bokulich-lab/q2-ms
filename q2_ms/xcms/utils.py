import csv
import os
from pathlib import Path

import pandas as pd


def change_data_paths(dir_path, new_directory):
    for filename in ["ms_backend_data.txt", "ms_experiment_sample_data.txt"]:
        # Read in dataframe
        file_path = os.path.join(dir_path, filename)
        if filename == "ms_backend_data.txt":
            df = pd.read_csv(
                file_path, sep="\t", header=1, index_col=0, quoting=csv.QUOTE_NONE
            )
        else:
            df = pd.read_csv(file_path, sep="\t", index_col=0, quoting=csv.QUOTE_NONE)

        # Update the paths while keeping the original filenames
        for column in ['"dataOrigin"', '"dataStorage"', '"spectraOrigin"']:
            try:
                df[column] = df[column].apply(
                    lambda x: '"' + str(Path(new_directory) / Path(x).name)
                )
            except KeyError:
                pass

        # Write dataframe back to file
        with open(file_path, "w") as f:
            if filename == "ms_backend_data.txt":
                f.write("# MsBackendMzR\n")
            f.write("\t".join(list(df.columns)) + "\n")
            df.to_csv(f, sep="\t", index=True, header=False, quoting=csv.QUOTE_NONE)


def create_fake_mzml_files(xcms_experiment_path):
    """
    Create empty mzML files for paths that are present in the
    'ms_experiment_sample_data.txt' file of an exported xcms experiment. This is
    needed to import an xcms experiment object without providing the original mzML
    files.
    """
    sample_data_path = os.path.join(
        xcms_experiment_path, "ms_experiment_sample_data.txt"
    )
    sample_data = pd.read_csv(
        sample_data_path, sep="\t", index_col=0, usecols=["spectraOrigin"]
    ).squeeze()
    for path in sample_data:
        os.makedirs(Path(path).parent, exist_ok=True)
        with open(path, "w"):
            pass
