from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.xcms.find_peaks_centwave import find_peaks_centwave


class TestFindPeaksCentWave(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_read_ms_experiment_without_metadata(self):
        xcms_experiment = XCMSExperimentDirFmt(
            self.get_data_path("read_ms_experiment_exported"), mode="r"
        )
        spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        find_peaks_centwave(
            spectra=spectra,
            xcms_experiment=xcms_experiment,
            min_peakwidth=20,
            max_peakwidth=80,
            noise=5000,
            prefilter_i=5000,
            prefilter_k=6,
        )
        # sample_data_exp = pd.read_csv(
        #     self.get_data_path(
        #         "ms_experiment_sample_data/ms_experiment_sample_data_default.txt"
        #     ),
        #     sep="\t",
        #     index_col=0,
        # )
        # sample_data_obs = pd.read_csv(
        #     os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt"),
        #     sep="\t",
        #     index_col=0,
        # )
        # sample_data_exp.drop(columns=["spectraOrigin"], inplace=True)
        # sample_data_obs.drop(columns=["spectraOrigin"], inplace=True)
        #
        # pd.testing.assert_frame_equal(sample_data_exp, sample_data_obs)
