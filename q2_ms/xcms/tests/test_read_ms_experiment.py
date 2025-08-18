# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
import qiime2
from qiime2 import Artifact
from qiime2.plugin.testing import TestPluginBase
from qiime2.sdk import parse_type

from q2_ms.types import XCMSExperimentDirFmt, mzMLDirFmt
from q2_ms.xcms.read_ms_experiment import _get_type, _validate_metadata


class TestReadMsExperiment(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def setUp(self):
        super().setUp()
        self.sample_metadata = qiime2.Metadata.load(
            self.get_data_path("faahKO_sample_data/sample_metadata.tsv")
        )
        self.spectra_dir = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        self.spectra = Artifact.import_data("SampleData[mzML]", self.spectra_dir)
        self.spectra_ms2_dir = mzMLDirFmt(self.get_data_path("ms2_spectra"), mode="r")
        self.spectra_ms2 = Artifact.import_data(
            "SampleData[mzML]", self.spectra_ms2_dir
        )
        self.read_ms_experiment = self.plugin.pipelines["read_ms_experiment"]

    def test_read_ms_experiment_metadata(self):
        (xcms_experiment,) = self.read_ms_experiment(
            spectra=self.spectra, sample_metadata=self.sample_metadata
        )
        self._test_read_ms_experiment_helper(
            xcms_experiment, "ms_experiment_sample_data_metadata.txt"
        )

    def test_read_ms_experiment_no_metadata(self):
        (xcms_experiment,) = self.read_ms_experiment(
            spectra=self.spectra,
        )
        self._test_read_ms_experiment_helper(
            xcms_experiment, "ms_experiment_sample_data_default.txt"
        )

    def _test_read_ms_experiment_helper(self, xcms_experiment, exp_sample_data):
        self.assertEqual(xcms_experiment.type, parse_type("XCMSExperiment"))

        xcms_experiment = xcms_experiment.view(XCMSExperimentDirFmt)

        sample_data_exp = pd.read_csv(
            self.get_data_path(
                os.path.join("ms_experiment_sample_data", exp_sample_data)
            ),
            sep="\t",
            index_col=0,
        )
        sample_data_obs = pd.read_csv(
            os.path.join(str(xcms_experiment), "ms_experiment_sample_data.txt"),
            sep="\t",
            index_col=0,
        )
        sample_data_obs.drop(columns=["spectraOrigin"], inplace=True)

        pd.testing.assert_frame_equal(sample_data_exp, sample_data_obs)

    def test_read_ms_experiment_ms2(self):
        (xcms_experiment,) = self.read_ms_experiment(spectra=self.spectra_ms2)
        self.assertEqual(
            xcms_experiment.type, parse_type("XCMSExperiment % Properties('MS2')")
        )

    def test_validate_metadata_missing(self):
        metadata_missing = self.sample_metadata.to_dataframe().drop(index="wt22")
        with self.assertRaisesRegex(ValueError, "missing in sample-metadata: {'wt22'}"):
            _validate_metadata(metadata_missing, str(self.spectra_dir))

    def test_read_ms_experiment_added(self):
        metadata_added = self.sample_metadata.to_dataframe().copy()
        metadata_added.loc["wt23"] = ["WT", "study"]
        with self.assertRaisesRegex(ValueError, "missing in spectra: {'wt23'}"):
            _validate_metadata(metadata_added, str(self.spectra_dir))

    def test_get_type_ms2(self):
        type = _get_type(self.get_data_path("get_type/ms2"))
        self.assertEqual(type, 'XCMSExperiment % Properties("MS2")')

    def test_get_type_ms1(self):
        type = _get_type(self.get_data_path("get_type/ms1"))
        self.assertEqual(type, "XCMSExperiment")
