from shutil import copytree

from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.xcms.adjust_retention_time_obiwarp import (
    _validate_parameters,
    adjust_retention_time_obiwarp,
)


class TestFindPeaksCentWave(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_adjust_retention_time_obiwarp(self):
        xcms_experiment = XCMSExperimentDirFmt()
        copytree(
            self.get_data_path("xcms_experiment_read_in"),
            str(xcms_experiment),
            dirs_exist_ok=True,
        )
        spectra = mzMLDirFmt()
        copytree(self.get_data_path("faahKO"), str(spectra), dirs_exist_ok=True)
        adjust_retention_time_obiwarp(
            spectra=spectra,
            xcms_experiment=xcms_experiment,
            bin_size=0.1,
            center_sample="ko21",
            response=0.2,
            dist_fun="cor",
            gap_init=-2,
            gap_extend=-0.5,
            factor_diag=0,
            factor_gap=0,
            local_alignment=True,
            init_penalty=0,
            sample_metadata_column="sampletype",
            subset_label="QC",
            subset_adjust="previous",
            rtime_difference_threshold=-0.5,
            chunk_size=-7,
            threads=1,
        )
        # chrom_peaks_exp = pd.read_csv(
        #     self.get_data_path("chrom_peaks_R/xcms_experiment_chrom_peaks.txt"),
        #     sep="\t",
        #     index_col=0,
        # )
        # chrom_peaks_obs = pd.read_csv(
        #     os.path.join(str(xcms_experiment_peaks),
        #     "xcms_experiment_chrom_peaks.txt"),
        #     sep="\t",
        #     index_col=0,
        # )
        # pd.testing.assert_frame_equal(chrom_peaks_exp, chrom_peaks_obs)

    def test_invalid_combination_of_subset_parameters(self):
        with self.assertRaisesRegex(ValueError, r"combination"):
            _validate_parameters(True, False, True, True, False)
        with self.assertRaisesRegex(ValueError, r"combination"):
            _validate_parameters(True, True, False, True, False)
        with self.assertRaisesRegex(ValueError, r"combination"):
            _validate_parameters(False, True, True, True, False)

    def test_valid_mixed_subset_parameters(self):
        try:
            _validate_parameters(True, True, True, True, False)
            _validate_parameters(False, False, False, True, False)
        except ValueError:
            self.fail("_validate_parameters raised ValueError unexpectedly!")

    def test_init_penalty_without_local_alignment(self):
        with self.assertRaisesRegex(
            ValueError, r"--p-init-penalty.*--p-local-alignment"
        ):
            _validate_parameters(True, True, True, False, True)
