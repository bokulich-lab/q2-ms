# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.core.exceptions import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types._format import (
    MatchedSpectraDirFmt,
    MatchedSpectraFormat,
    MSBackendDataFormat,
    MSExperimentLinkMColsFormat,
    MSExperimentSampleDataFormat,
    MSExperimentSampleDataLinksSpectra,
    MSPDirFmt,
    MSPFormat,
    SpectraSlotsFormat,
    XCMSExperimentChromPeakDataFormat,
    XCMSExperimentChromPeaksFormat,
    XCMSExperimentDirFmt,
    XCMSExperimentFeatureDefinitionsFormat,
    XCMSExperimentFeaturePeakIndexFormat,
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
        with self.assertRaisesRegex(
            ValidationError,
            ".*Header does not match MSBackendDataFormat\\. .*\\n# MsBackendMzR\\n"
            "msLevel\\trtime\\tacquisitionNum\\tdataOrigin\\tpolarity\\tprecScanNum"
            "\\tprecursorMz\\tprecursorIntensity\\tprecursorCharge\\tcollisionEnergy"
            "\\tpeaksCount\\ttotIonCurrent\\tbasePeakMZ\\tbasePeakIntensity"
            "\\tionisationEnergy\\tlowMZ\\thighMZ\\tinjectionTime\\tspectrumId"
            "\\tdataStorage\\tscanIndex\\n\\nFound instead:\\nsubsetBy\\n1\\t1\\.1",
        ):
            format.validate()

    def test_ms_experiment_link_mcols_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/ms_experiment_link_mcols.txt")
        format = MSExperimentLinkMColsFormat(filepath, mode="r")
        format.validate()

    def test_ms_experiment_link_mcols_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSExperimentLinkMColsFormat(filepath, mode="r")
        with self.assertRaisesRegex(
            ValidationError,
            ".*Header does not match MSExperimentLinkMColsFormat\\..*:\\n"
            '"subsetBy"\\n\\nFound instead:\\n# MsBackendMzR',
        ):
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
        with self.assertRaisesRegex(ValidationError, ".*MSExperimentLinkMColsFormat.*"):
            format.validate()

    def test_ms_experiment_sample_data_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/ms_experiment_sample_data.txt")
        format = MSExperimentSampleDataFormat(filepath, mode="r")
        format.validate()

    def test_ms_experiment_sample_data_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = MSExperimentSampleDataFormat(filepath, mode="r")
        with self.assertRaisesRegex(
            ValidationError,
            ".*MSExperimentSampleDataFormat.*\\n\\nFound instead:\\n# MsBackendMzR",
        ):
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
        with self.assertRaisesRegex(ValidationError, "File is not valid JSON"):
            format.validate()

    def test_spectra_processing_queue_validate_negative_list(self):
        filepath = self.get_data_path(
            "XCMSExperiment_json_invalid/spectra_processing_queue_list_check.json"
        )
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "XCMSExperimentJSONFormat.*list"):
            format.validate()

    def test_spectra_processing_queue_validate_negative_keys(self):
        filepath = self.get_data_path(
            "XCMSExperiment_json_invalid/spectra_processing_queue_keys_check.json"
        )
        format = XCMSExperimentJSONFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "XCMSExperimentJSONFormat.*keys"):
            format.validate()

    def test_spectra_slots_validate_positive(self):
        filepath = self.get_data_path("XCMSExperiment/spectra_slots.txt")
        format = SpectraSlotsFormat(filepath, mode="r")
        format.validate()

    def test_spectra_slots_validate_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = SpectraSlotsFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "SpectraSlotsFormat"):
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
        with self.assertRaisesRegex(
            ValidationError,
            "XCMSExperimentChromPeakDataFormat.*\\nms_level, is_filled\\n\\n"
            "Found instead:\\n# MsBackendMzR",
        ):
            format.validate()

    def test_xcms_experiment_chrom_peaks_positive(self):
        filepath = self.get_data_path("XCMSExperiment/xcms_experiment_chrom_peaks.txt")
        format = XCMSExperimentChromPeaksFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_chrom_peaks_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentChromPeaksFormat(filepath, mode="r")
        with self.assertRaisesRegex(
            ValidationError,
            "XCMSExperimentChromPeaksFormat.*\\nmz, mzmin, mzmax, rt, rtmin, "
            "rtmax, into, intb, maxo, sn, sample\\n\\n"
            "Found instead:\\n# MsBackendMzR",
        ):
            format.validate()

    def test_xcms_experiment_feature_definitions_positive(self):
        filepath = self.get_data_path(
            "XCMSExperiment/xcms_experiment_feature_definitions.txt"
        )
        format = XCMSExperimentFeatureDefinitionsFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_feature_definitions_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentFeatureDefinitionsFormat(filepath, mode="r")
        with self.assertRaisesRegex(
            ValidationError,
            "XCMSExperimentFeatureDefinitionsFormat.*\\nmzmed, mzmin, mzmax, "
            "rtmed, rtmin, rtmax, npeaks, peakidx, ms_level\\n\\n"
            "Found instead:\\n# MsBackendMzR",
        ):
            format.validate()

    def test_xcms_experiment_feature_peak_index_positive(self):
        filepath = self.get_data_path(
            "XCMSExperiment/xcms_experiment_feature_peak_index.txt"
        )
        format = XCMSExperimentFeaturePeakIndexFormat(filepath, mode="r")
        format.validate()

    def test_xcms_experiment_feature_peak_index_negative(self):
        filepath = self.get_data_path("XCMSExperiment/ms_backend_data.txt")
        format = XCMSExperimentFeaturePeakIndexFormat(filepath, mode="r")
        with self.assertRaisesRegex(
            ValidationError,
            "XCMSExperimentFeaturePeakIndexFormat.*\\nfeature_index, "
            "peak_index\\n\\nFound instead:\\n# MsBackendMzR",
        ):
            format.validate()

    def test_xcms_experiment_dir_fmt_positive(self):
        filepath = self.get_data_path("XCMSExperiment")
        format = XCMSExperimentDirFmt(filepath, mode="r")
        format.validate()


class TestMSPFormat(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_msp_validate_positive(self):
        format = MSPFormat(self.get_data_path("MSP_valid/valid.msp"), mode="r")
        format.validate()

    def test_msp_validate_negative(self):
        format = MSPFormat(self.get_data_path("MSP_invalid/invalid.msp"), mode="r")
        pattern = r"Line 6: Inv.+\nPrecursor_type \[M\+H\]\+\nLine 21: Peak.+\n311.0914"
        with self.assertRaisesRegex(ValidationError, pattern):
            format.validate()

    def test_msp_directory_format_validate_positive(self):
        format = MSPDirFmt(self.get_data_path("MSP_valid"), mode="r")
        format.validate()


class TestMatchedSpectra(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_matched_spectra_format_validate_positive(self):
        format = MatchedSpectraFormat(
            self.get_data_path("MatchedSpectra_valid/matched_spectra.txt"), mode="r"
        )
        format.validate()

    def test_matched_spectra_format_validate_positive_min(self):
        format = MatchedSpectraFormat(
            self.get_data_path("MatchedSpectra_invalid/matched_spectra_min.txt"),
            mode="r",
        )
        format.validate("min")

    def test_matched_spectra_format_validate_negative_header(self):
        format = MatchedSpectraFormat(
            self.get_data_path("MatchedSpectra_invalid/matched_spectra_header.txt"),
            mode="r",
        )
        with self.assertRaisesRegex(
            ValidationError,
            "MatchedSpectraFormat.*\\n.original_query_index, target_spectrum_id, "
            "score\\n\\nFound instead:\\n.original_query_index, target_spectrum_id",
        ):
            format.validate()

    def test_matched_spectra_format_validate_negative_col_number(self):
        format = MatchedSpectraFormat(
            self.get_data_path("MatchedSpectra_invalid/matched_spectra_col_number.txt"),
            mode="r",
        )
        with self.assertRaisesRegex(ValidationError, "Line 2 does not have 3 columns."):
            format.validate()

    def test_matched_spectra_format_validate_negative_score_range(self):
        format = MatchedSpectraFormat(
            self.get_data_path(
                "MatchedSpectra_invalid/matched_spectra_score_range.txt"
            ),
            mode="r",
        )
        with self.assertRaisesRegex(
            ValidationError, "Line 2 has an out-of-range score: 16.0"
        ):
            format.validate()

    def test_matched_spectra_format_validate_negative_score_type(self):
        format = MatchedSpectraFormat(
            self.get_data_path("MatchedSpectra_invalid/matched_spectra_score_type.txt"),
            mode="r",
        )
        with self.assertRaisesRegex(
            ValidationError, "Line 2 has a non-numeric score: value"
        ):
            format.validate()

    def test_matched_spectra_directory_format_validate_positive(self):
        format = MatchedSpectraDirFmt(
            self.get_data_path("MatchedSpectra_valid"), mode="r"
        )
        format.validate()
