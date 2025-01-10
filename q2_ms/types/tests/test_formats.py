# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.core.exceptions import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types._format import mzMLDirFmt, mzMLFormat


class TestMSTypesAndFormats(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_mzml_dir_fmt_validate_positive(self):
        format = mzMLDirFmt(self.get_data_path("mzML_valid"), mode="r")
        format.validate()

    def test_mzml_format_validate_positive(self):
        filepath = self.get_data_path("mzML_valid/tiny.mzML")
        format = mzMLFormat(filepath, mode="r")
        format.validate()

    def test_mzml_format_validate_negative(self):
        filepath = self.get_data_path("mzML_invalid/invalid.mzML")
        format = mzMLFormat(filepath, mode="r")
        with self.assertRaises(ValidationError):
            format.validate()
