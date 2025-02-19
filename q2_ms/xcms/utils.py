import csv
import os

import pandas as pd


def change_spectra_paths(xcms_experiment_path, spectra_path):
    """Changes the paths to the spectra files in XCMSExperiment files.

    The paths to the spectra files is recorded in multiple files in the
    XCMSExperiment artifact. This function updates the paths to the spectra files
    in the XCMSExperiment files with the specified spectra_path while keeping the
    filenames unchanged.

    Args:
        xcms_experiment_path (str): Path to the XCMSExperiment.
        spectra_path (str): Path to the directory where the spectra files are
        located.

    """
    for filename in ["ms_backend_data.txt", "ms_experiment_sample_data.txt"]:
        # Read in dataframe
        file_path = os.path.join(xcms_experiment_path, filename)
        header = 1 if filename == "ms_backend_data.txt" else 0
        df = pd.read_csv(
            file_path, sep="\t", header=header, index_col=0, quoting=csv.QUOTE_NONE
        )

        # Update the paths while keeping the original filenames
        for column in set(df.columns) & {
            '"dataOrigin"',
            '"dataStorage"',
            '"spectraOrigin"',
        }:
            df[column] = df[column].apply(
                lambda x: '"' + os.path.join(spectra_path, os.path.basename(x))
            )

        # Write dataframe back to file
        with open(file_path, "w") as f:
            if filename == "ms_backend_data.txt":
                f.write("# MsBackendMzR\n")
            f.write("\t".join(list(df.columns)) + "\n")
            df.to_csv(f, sep="\t", index=True, header=False, quoting=csv.QUOTE_NONE)
