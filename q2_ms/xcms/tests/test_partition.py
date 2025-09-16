# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest

import pandas as pd
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt
from q2_ms.xcms.partition import partition_xcms_experiment


class TestPartition(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def setUp(self):
        super().setUp()
        self.xcms_experiment = XCMSExperimentDirFmt(
            self.get_data_path("xcms_experiment_read_in"), mode="r"
        )

    def test_partition_xcms_experiment(self):
        obs = partition_xcms_experiment(self.xcms_experiment)
        sample_ids = {"ko15", "ko16", "wt21", "wt22"}
        self.assertEqual(obs.keys(), sample_ids)
        for _id in sample_ids:
            sample_data = pd.read_csv(
                os.path.join(str(obs[_id]), "ms_experiment_sample_data.txt"), sep="\t"
            )
            self.assertEqual(len(sample_data), 1)
            self.assertEqual(sample_data["sample_name"].iloc[0], _id)

    def test_partition_xcms_experiment_uneven(self):
        obs = partition_xcms_experiment(self.xcms_experiment, num_partitions=2)
        self.assertEqual(obs.keys(), {1, 2})

        sample_data_1 = pd.read_csv(
            os.path.join(str(obs[1]), "ms_experiment_sample_data.txt"), sep="\t"
        )
        self.assertEqual(len(sample_data_1), 2)
        self.assertEqual(sample_data_1["sample_name"].to_list(), ["ko15", "ko16"])

        sample_data_2 = pd.read_csv(
            os.path.join(str(obs[2]), "ms_experiment_sample_data.txt"), sep="\t"
        )
        self.assertEqual(len(sample_data_2), 2)
        self.assertEqual(sample_data_2["sample_name"].to_list(), ["wt21", "wt22"])

    def test_partition_xcms_experiment_warning(self):
        with self.assertWarnsRegex(
            UserWarning, "You have requested a number of.*5.*4.*4"
        ):
            partition_xcms_experiment(self.xcms_experiment, 5)


if __name__ == "__main__":
    unittest.main()
