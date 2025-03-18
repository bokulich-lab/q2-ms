# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest
from unittest.mock import Mock, patch

from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import MSPDirFmt
from q2_ms.xcms.database import fetch_massbank


class TestmzMLFormats(TestPluginBase):
    package = "q2_ms.types.tests"

    @patch("q2_ms.xcms.database.requests.get")
    def test_fetch_massbank(self, mock_get):
        # Mock the response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_massbank()

        # Check if the file exists
        file_path = os.path.join(str(result), "MassBank_NIST.msp")
        self.assertTrue(os.path.exists(file_path))
        self.assertIsInstance(result, MSPDirFmt)

    @patch("q2_ms.xcms.database.requests.get")
    def test_fetch_massbank_error(self, mock_get):
        # Mock the response object
        mock_response = Mock()
        mock_response.status_code = 502
        mock_response.content = b""
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(ValueError, "502"):
            fetch_massbank()


if __name__ == "__main__":
    unittest.main()
