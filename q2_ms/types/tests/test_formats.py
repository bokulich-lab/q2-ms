# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.core.exceptions import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types._format import (
    MSBackendDataFormat,
    MSExperimentLinkMColsFormat,
    MSExperimentSampleDataFormat,
    MSExperimentSampleDataLinksSpectra,
    SpectraSlotsFormat,
    XCMSExperimentChromPeakDataFormat,
    XCMSExperimentChromPeaksFormat,
    XCMSExperimentJSONFormat,
    mzMLDirFmt,
    mzMLFormat,
)


class TestmzMLFormats(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_mzml_dir_fmt_validate_positive(self):
        format = mzMLDirFmt(self.get_data_path("mzML_valid"), mode="r")
        format.validate()

    def test_mzml_format_validate_positive(self):
        filepath = self.get_data_path("mzML_valid/tiny.mzML")
        format = mzMLFormat(filepath, mode="r")
        format.validate()

    def test_mzml_format_validate_negative(self):
        filepath = self.get_data_path("mzML_invalid/invalid.mzML")
        format = mzMLFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()


class TestXCMSExperimentFormats(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_ms_backend_data_format_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSBackendDataFormat(filepath, mode="r")
        format.validate()

    def test_ms_backend_data_format_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_experiment_link_mcols.txt")
        format = MSBackendDataFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_ms_experiment_link_mcols_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/ms_experiment_link_mcols.txt")
        format = MSExperimentLinkMColsFormat(filepath, mode="r")
        format.validate()

    def test_ms_experiment_link_mcols_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSExperimentLinkMColsFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_ms_experiment_sample_data_links_spectra_validate_positive(self):
        filepath = self.get_data_path(
            "XCMSExperiment/ms_experiment_sample_data_links_spectra.txt"
        )
        format = MSExperimentSampleDataLinksSpectra(filepath, mode="r")
        format.validate()

    def test_ms_experiment_sample_data_links_spectra_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSExperimentSampleDataLinksSpectra(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_ms_experiment_sample_data_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/ms_experiment_sample_data.txt")
        format = MSExperimentSampleDataFormat(filepath, mode="r")
        format.validate()

    def test_ms_experiment_sample_data_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSExperimentSampleDataFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_xcms_experiment_json_queue_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/spectra_processing_queue.json")
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_json_history_validate_positive(self):
        filepath = self.get_data_path(
            "XCMSExperiment/xcms_experiment_process_history.json"
        )
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        format.validate()

    def test_spectra_processing_queue_validate_negative_json(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "JSON"):
            format.validate()

    def test_spectra_processing_queue_validate_negative_list(self):
        filepath = self.get_data_path(
            "XCMSExperiment_extra/spectra_processing_queue_list_check.json"
        )
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "list"):
            format.validate()

    def test_spectra_processing_queue_validate_negative_keys(self):
        filepath = self.get_data_path(
            "XCMSExperiment_extra/spectra_processing_queue_keys_check.json"
        )
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "keys"):
            format.validate()

    def test_spectra_slots_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/spectra_slots.txt")
        format = SpectraSlotsFormat(filepath, mode="r")
        format.validate()

    def test_spectra_slots_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = SpectraSlotsFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_xcms_experiment_chrom_peak_data_positive(self):
        filepath = self.get_data_path(
            "XCMSExperiment/xcms_experiment_chrom_peak_data.txt"
        )
        format = XCMSExperimentChromPeakDataFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_chrom_peak_data_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentChromPeakDataFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()

    def test_xcms_experiment_chrom_peaks_positive(self):
        filepath = self.get_data_path("XCMSExperiment/xcms_experiment_chrom_peaks.txt")
        format = XCMSExperimentChromPeaksFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_chrom_peaks_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentChromPeaksFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()
