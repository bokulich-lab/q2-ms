# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
from pandas._testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt
from q2_ms.xcms.metadata import create_spectral_metadata


class TestMetadata(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_create_spectral_metadata(self):
        xcms_experiment = XCMSExperimentDirFmt(self.get_data_path("metadata"), "r")
        obs = create_spectral_metadata(xcms_experiment)
        self._test_create_spectral_metadata_helper(obs, "spectral_metadata_ms1.tsv")

    def test_create_spectral_metadata_ms2(self):
        xcms_experiment = XCMSExperimentDirFmt(self.get_data_path("metadata"), "r")
        obs = create_spectral_metadata(xcms_experiment, "2")
        self._test_create_spectral_metadata_helper(obs, "spectral_metadata_ms2.tsv")

    def _test_create_spectral_metadata_helper(self, obs, exp_metadata):
        exp = pd.read_csv(
            self.get_data_path(os.path.join("metadata_expected", exp_metadata)),
            sep="\t",
            index_col=0,
        )
        exp.index = exp.index.astype(str)
        columns_to_convert = [
            "msLevel",
            "acquisitionNum",
            "polarity",
            "peaksCount",
            "ionisationEnergy",
            "injectionTime",
            "scanWindowLowerLimit",
            "scanWindowUpperLimit",
            "scanIndex",
            "sample_id",
        ]
        exp[columns_to_convert] = exp[columns_to_convert].astype("float64")
        exp["centroided"] = exp["centroided"].astype("str")

        assert_frame_equal(obs.to_dataframe(), exp)
