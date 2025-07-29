import os
import shutil

import pandas as pd

from q2_ms.types import XCMSExperimentDirFmt


def _verify_and_copy_file(xcms_experiments, file_name, output_path):
    """
    Verifies that all files with the given name in xcms_experiments paths
    have identical content. If so, copies one to the output path.

    Parameters:
        xcms_experiments (list): List of xcms_experiments containing the target files.
        file_name (str): The name of the file to check in each directory.
        output_path (str): File path where the verified file should be copied.

    Raises:
        ValueError: If any file content differs from the others.
    """
    contents = []
    file_paths = []

    for xcms_experiment in xcms_experiments:
        file_path = os.path.join(str(xcms_experiment), file_name)
        file_paths.append(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            contents.append(f.read())

    reference = contents[0]
    for _id, content in enumerate(contents[1:], start=1):
        if content != reference:
            raise ValueError(
                f"Mismatching content found in {file_name}: {file_paths[_id]}\n"
                f"Only artifacts with identical content in {file_name} can be collated."
            )

    # All files are identical; copy the first one to output_path
    shutil.copyfile(file_paths[0], os.path.join(output_path, file_name))


def _read_table_and_index(file_path: str, header_lines: int, index_prefix="", offset=0):
    """
    Reads a tab-separated file with a fixed number of header lines and reindexes
    the resulting DataFrame rows using a custom prefix and offset.

    Parameters:
        file_path (str):
            The full path to the input tab-separated text file to read.

        header_lines (int):
            The number of header lines to preserve from the top of the file.

        index_prefix (str, optional):
            A string prefix to add to each row index. Default is an empty string.

        offset (int, optional):
            A numeric offset to apply to the index. The first row will have index
            '<index_prefix><offset + 1>'. Default is 0.

    Returns:
        header (str):
            The preserved header lines as a single string.
        df (pd.DataFrame or None):
            A DataFrame containing the parsed table with reindexed rows or None if
            df is empty.
    """
    # Read the header lines from the file
    with open(file_path) as f:
        header = "".join([f.readline() for _ in range(header_lines)])

    df = pd.read_csv(
        file_path,
        sep="\t",
        skiprows=header_lines - 1,
        index_col=0,
        dtype=str,
        quoting=3,
    )
    # Return only header and None if the DataFrame is empty
    if df.empty:
        return header, None

    # Reindex the DataFrame rows with the specified prefix and offset
    df.index = [f'"{index_prefix}{i}"' for i in range(offset + 1, offset + 1 + len(df))]
    return header, df


def _write_with_preserved_header(
    output_path: str, header: str, df: pd.DataFrame | None
):
    with open(output_path, "w") as f:
        f.write(header)
        if df is not None:
            df.to_csv(f, sep="\t", index=True, header=False, quoting=3)


def _check_headers(dfs, file_name):
    """
    Verifies that all DataFrames in the list have the same column names.

    Parameters:
        dfs (list of pd.DataFrame): List of DataFrames to compare.

    Raises:
        ValueError: If any DataFrame has columns that differ from the first one.
                    The error message will show the mismatched columns.
    """
    for i, df in enumerate(dfs[1:], start=1):
        if not df.columns.equals(dfs[0].columns):
            raise ValueError(
                f"There is a column mismatch in one of the files called: {file_name}\n"
                f"Columns of DataFrame at index {0}:\n"
                f"{','.join(dfs[0].columns.tolist())}\n"
                f"Columns of DataFrame at index {i}:\n"
                f"{','.join(df.columns.tolist())}\n"
            )


def collate_xcms_experiments(
    xcms_experiments: XCMSExperimentDirFmt,
) -> XCMSExperimentDirFmt:
    collated_xcms_experiment = XCMSExperimentDirFmt()
    output_dir = collated_xcms_experiment.path

    ms_backend_all = []
    sample_data_all = []
    spectra_links_all = []
    chrom_peaks_all = []
    chrom_peak_data_all = []

    spectrum_index_offset = 0
    sample_index_offset = 0
    chrom_peaks_offset = 0
    chrom_peaks_data_offset = 0

    for file_name in [
        "spectra_slots.txt",
        "xcms_experiment_process_history.json",
        "ms_experiment_link_mcols.txt",
        "spectra_processing_queue.json",
    ]:
        _verify_and_copy_file(xcms_experiments, file_name, output_dir)

    for xcms_experiment in xcms_experiments:
        dir_path = xcms_experiment.path

        # spectra_links
        links = pd.read_csv(
            os.path.join(dir_path, "ms_experiment_sample_data_links_spectra.txt"),
            sep="\t",
            header=None,
        )
        links[0] += sample_index_offset
        links[1] += spectrum_index_offset
        spectra_links_all.append(links)

        # ms_backend
        header_ms_backend, ms_backend = _read_table_and_index(
            os.path.join(dir_path, "ms_backend_data.txt"),
            header_lines=2,
            offset=spectrum_index_offset,
        )
        ms_backend_all.append(ms_backend)
        spectrum_index_offset += len(ms_backend)

        # chrom_peaks
        header_chrom_peaks, chrom_peaks = _read_table_and_index(
            os.path.join(dir_path, "xcms_experiment_chrom_peaks.txt"),
            header_lines=1,
            offset=chrom_peaks_offset,
            index_prefix="CP",
        )
        if chrom_peaks is not None:
            chrom_peaks['"sample"'] = (
                chrom_peaks['"sample"'].astype(int) + sample_index_offset
            )
            chrom_peaks_all.append(chrom_peaks)
            chrom_peaks_offset += len(chrom_peaks)

        # sample_data
        header_sample_data, sample_data = _read_table_and_index(
            os.path.join(dir_path, "ms_experiment_sample_data.txt"),
            header_lines=1,
            offset=sample_index_offset,
        )
        sample_data_all.append(sample_data)
        sample_index_offset += len(sample_data)

        # chrom_peak_data
        header_chrom_peak_data, chrom_peak_data = _read_table_and_index(
            os.path.join(dir_path, "xcms_experiment_chrom_peak_data.txt"),
            header_lines=1,
            offset=chrom_peaks_data_offset,
            index_prefix="CP",
        )
        if chrom_peak_data is not None:
            chrom_peak_data_all.append(chrom_peak_data)
            chrom_peaks_data_offset += len(chrom_peak_data)

    # Check if headers are consistent
    _check_headers(ms_backend_all, "ms_backend_data.txt")
    _check_headers(sample_data_all, "ms_experiment_sample_data.txt")
    _check_headers(chrom_peaks_all, "xcms_experiment_chrom_peaks.txt")
    _check_headers(chrom_peak_data_all, "xcms_experiment_chrom_peak_data.txt")

    # Concat dfs and Write outputs
    links_combined = pd.concat(spectra_links_all).astype(int)
    links_combined.to_csv(
        os.path.join(output_dir, "ms_experiment_sample_data_links_spectra.txt"),
        sep="\t",
        index=False,
        header=False,
    )

    ms_backend_combined = pd.concat(ms_backend_all)
    _write_with_preserved_header(
        os.path.join(output_dir, "ms_backend_data.txt"),
        header_ms_backend,
        ms_backend_combined,
    )

    sample_data_combined = pd.concat(sample_data_all)
    _write_with_preserved_header(
        os.path.join(output_dir, "ms_experiment_sample_data.txt"),
        header_sample_data,
        sample_data_combined,
    )

    chrom_peaks_combined = pd.concat(chrom_peaks_all) if chrom_peaks_all else None
    _write_with_preserved_header(
        os.path.join(output_dir, "xcms_experiment_chrom_peaks.txt"),
        header_chrom_peaks,
        chrom_peaks_combined,
    )

    chrom_peak_data_combined = (
        pd.concat(chrom_peak_data_all) if chrom_peak_data_all else None
    )
    _write_with_preserved_header(
        os.path.join(output_dir, "xcms_experiment_chrom_peak_data.txt"),
        header_chrom_peak_data,
        chrom_peak_data_combined,
    )

    return collated_xcms_experiment
