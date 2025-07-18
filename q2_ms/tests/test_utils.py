# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess
import unittest
from unittest.mock import call, patch

from qiime2.plugin.testing import TestPluginBase

from q2_ms.utils import EXTERNAL_CMD_WARNING, run_command, run_r_script


class TestRunCommand(TestPluginBase):
    package = "q2_ms.tests"

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_run_command_verbose(self, mock_print, mock_subprocess_run):
        # Mock command and working directory
        cmd = ["echo", "Hello"]
        cwd = "/test/directory"

        # Run the function with verbose=True
        run_command(cmd, cwd=cwd, verbose=True)

        # Check if subprocess.run was called with the correct arguments
        mock_subprocess_run.assert_called_once_with(cmd, check=True, cwd=cwd, env=None)

        # Check if the correct print statements were called
        mock_print.assert_has_calls(
            [
                call(EXTERNAL_CMD_WARNING),
                call("\nCommand:", end=" "),
                call("echo Hello", end="\n\n"),
            ]
        )

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_run_command_non_verbose(self, mock_print, mock_subprocess_run):
        # Mock command and working directory
        cmd = ["echo", "Hello"]
        cwd = "/test/directory"

        # Run the function with verbose=False
        run_command(cmd, cwd=cwd, verbose=False)

        # Check if subprocess.run was called with the correct arguments
        mock_subprocess_run.assert_called_once_with(cmd, check=True, cwd=cwd, env=None)

        # Ensure no print statements were made
        mock_print.assert_not_called()

    @patch("subprocess.run")
    def test_run_r_script_success(self, mock_subprocess):
        # Call function
        run_r_script(
            params={"param1": "value1", "param2": 42, "param3": None},
            script_name="test_script",
            package_name="q2_ms",
        )

        # Check if subprocess.run was called correctly
        expected_cmd = [
            "test_script.R",
            "--param1",
            "value1",
            "--param2",
            "42",
        ]

        mock_subprocess.assert_called_once_with(
            expected_cmd, check=True, cwd=None, env=unittest.mock.ANY
        )

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd"))
    def test_run_r_script_failure(self, mock_subprocess):
        with self.assertRaises(Exception) as context:
            run_r_script({}, "", "q2_ms")

        self.assertIn("q2_ms", str(context.exception))
