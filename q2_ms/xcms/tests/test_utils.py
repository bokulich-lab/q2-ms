import os

from qiime2.plugin.testing import TestPluginBase

from q2_ms.xcms.utils import create_fake_mzml_files


class TestXCMSUtils(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_create_fake_mzml_files(self):
        xcms_experiment_path = self.get_data_path("change_paths")
        tmp_dir = self.temp_dir
        create_fake_mzml_files(xcms_experiment_path, tmp_dir.name)
        self.assertTrue(os.path.exists(os.path.join(tmp_dir.name, "ko15.CDF")))
        self.assertTrue(os.path.exists(os.path.join(tmp_dir.name, "ko16.CDF")))
