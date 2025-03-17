# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_ms.xcms.metadata import create_metadata


class TestMetadata(TestPluginBase):
    package = "q2_ms.types.tests"


def test_create_metadata():
    df = create_metadata(
        "/Users/rischv/Documents/data/metabolomics/xcms_test_data_mzml/"
        "out_R_rt_correction_filtered"
    )
    print(df)
