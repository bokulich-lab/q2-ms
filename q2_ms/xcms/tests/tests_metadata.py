# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
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
        exp = pd.read_csv(
            self.get_data_path("metadata_expected/spectral_metadata.tsv"),
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
