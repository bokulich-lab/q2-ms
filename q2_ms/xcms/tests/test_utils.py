# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

from qiime2.plugin.testing import TestPluginBase

from q2_ms.xcms.utils import create_fake_spectra_files


class TestXCMSUtils(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_create_fake_spectra_files(self):
        xcms_experiment_path = self.get_data_path("create_fake_spectra_files")
        tmp_dir = self.temp_dir
        create_fake_spectra_files(xcms_experiment_path, tmp_dir.name)
        self.assertTrue(os.path.exists(os.path.join(tmp_dir.name, "ko15.mzML")))
        self.assertTrue(os.path.exists(os.path.join(tmp_dir.name, "ko16.mzML")))
