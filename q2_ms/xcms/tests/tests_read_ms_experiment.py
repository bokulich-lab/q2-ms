import os

import pandas as pd
import qiime2
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import mzMLDirFmt
from q2_ms.xcms.read_ms_experiment import _validate_metadata, read_ms_experiment


class TestReadMsExperiment(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def setUp(self):
        super().setUp()
        self.sample_metadata = pd.read_csv(
            self.get_data_path("faahKO_sample_data/sample_metadata.tsv"),
            sep="\t",
            index_col=0,
        )
        self.spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")

    def test_read_ms_experiment_metadata(self):
        xcms_experiment = read_ms_experiment(
            spectra=self.spectra,
            sample_metadata=qiime2.Metadata(self.sample_metadata),
        )
        sample_data_exp = pd.read_csv(
            self.get_data_path(
                "ms_experiment_sample_data/ms_experiment_sample_data_metadata.txt"
            ),
            sep="\t",
            index_col=0,
        )
        sample_data_obs = pd.read_csv(
            os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt"),
            sep="\t",
            index_col=0,
        )
        sample_data_exp.drop(columns=["spectraOrigin"], inplace=True)
        sample_data_obs.drop(columns=["spectraOrigin"], inplace=True)

        pd.testing.assert_frame_equal(sample_data_exp, sample_data_obs)

    def test_read_ms_experiment_without_metadata(self):
        xcms_experiment = read_ms_experiment(spectra=self.spectra)
        sample_data_exp = pd.read_csv(
            self.get_data_path(
                "ms_experiment_sample_data/ms_experiment_sample_data_default.txt"
            ),
            sep="\t",
            index_col=0,
        )
        sample_data_obs = pd.read_csv(
            os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt"),
            sep="\t",
            index_col=0,
        )
        sample_data_exp.drop(columns=["spectraOrigin"], inplace=True)
        sample_data_obs.drop(columns=["spectraOrigin"], inplace=True)

        pd.testing.assert_frame_equal(sample_data_exp, sample_data_obs)

    def test_validate_metadata_missing(self):
        metadata_missing = self.sample_metadata.drop(index="wt22")
        with self.assertRaisesRegex(ValueError, "missing in sample-metadata: {'wt22'}"):
            _validate_metadata(metadata_missing, str(self.spectra))

    def test_read_ms_experiment_added(self):
        metadata_added = self.sample_metadata.copy()
        metadata_added.loc["wt23"] = ["WT", "study"]
        with self.assertRaisesRegex(ValueError, "missing in spectra: {'wt23'}"):
            _validate_metadata(metadata_added, str(self.spectra))
