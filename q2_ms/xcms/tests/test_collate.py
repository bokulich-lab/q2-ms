# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import tempfile

import pandas as pd
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt
from q2_ms.xcms.collate import (
    _check_headers,
    _read_table_and_index,
    _remove_dates_json,
    _verify_and_copy_file,
    _write_with_preserved_header,
    collate_xcms_experiments,
)


class TestCollate(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def setUp(self):
        super().setUp()
        self.ko15 = XCMSExperimentDirFmt(self.get_data_path("collate/ko15"), mode="r")
        self.ko16 = XCMSExperimentDirFmt(self.get_data_path("collate/ko16"), mode="r")
        self.wt21 = XCMSExperimentDirFmt(self.get_data_path("collate/wt21"), mode="r")
        self.wt22 = XCMSExperimentDirFmt(self.get_data_path("collate/wt22"), mode="r")
        self.ko15_empty_peaks = XCMSExperimentDirFmt(
            self.get_data_path("collate/ko15_empty_peaks"), mode="r"
        )

    def test_collate_xcms_experiments(self):
        obs = collate_xcms_experiments([self.ko15, self.ko16, self.wt21, self.wt22])
        exp_path = self.get_data_path("xcms_experiment_peaks")
        self._test_collate_xcms_experiments_helper(obs, exp_path)

    def test_collate_xcms_experiments_empty_peaks(self):
        obs = collate_xcms_experiments([self.ko15_empty_peaks, self.ko16])
        exp_path = self.get_data_path("xcms_experiment_empty_peaks")
        self._test_collate_xcms_experiments_helper(obs, exp_path)

    def _test_collate_xcms_experiments_helper(self, obs, exp_path):
        for file_name in os.listdir(exp_path):
            if not file_name == "ms_backend_data.txt":
                path1 = os.path.join(str(obs), file_name)
                path2 = os.path.join(exp_path, file_name)

                if os.path.isfile(path1) and os.path.isfile(path2):
                    with open(path1, "rb") as f1, open(path2, "rb") as f2:
                        content1 = f1.read()
                        content2 = f2.read()
                        self.assertEqual(
                            content1,
                            content2,
                            msg=f"Files differ: {file_name}\n{path1}\n{path2}",
                        )

        # Check ms_backend_data.txt file, dataOrigin and dataStorage columns have to be
        # dropped because paths change for every test run.
        ms_backend_obs = pd.read_csv(
            os.path.join(obs.path, "ms_backend_data.txt"),
            sep="\t",
            index_col=0,
            skiprows=1,
        )
        ms_backend_exp = pd.read_csv(
            os.path.join(obs.path, "ms_backend_data.txt"),
            sep="\t",
            index_col=0,
            skiprows=1,
        )
        ms_backend_obs.drop(["dataOrigin", "dataStorage"], axis=1, inplace=True)
        ms_backend_exp.drop(["dataOrigin", "dataStorage"], axis=1, inplace=True)
        self.assertTrue(ms_backend_obs.equals(ms_backend_exp))

    def test_verify_and_copy_file_passes(self):
        with tempfile.TemporaryDirectory() as output_dir:
            _verify_and_copy_file(
                [
                    self.get_data_path("verify_and_copy_file/dir1"),
                    self.get_data_path("verify_and_copy_file/dir2"),
                ],
                "file.txt",
                output_dir,
            )

            output_file = os.path.join(output_dir, "file.txt")
            self.assertTrue(os.path.exists(output_file))

    def test_verify_and_copy_file_passes_process_history(self):
        with tempfile.TemporaryDirectory() as output_dir:
            _verify_and_copy_file(
                [
                    self.get_data_path("verify_and_copy_file/dir1"),
                    self.get_data_path("verify_and_copy_file/dir2"),
                ],
                "xcms_experiment_process_history.json",
                output_dir,
            )

            output_file = os.path.join(
                output_dir, "xcms_experiment_process_history.json"
            )
            self.assertTrue(os.path.exists(output_file))

    def test_verify_and_copy_file_raises_value_error_on_mismatch(self):
        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaisesRegex(ValueError, r".*file\.txt:.*file\.txt"):
                _verify_and_copy_file(
                    [
                        self.get_data_path("verify_and_copy_file/dir1"),
                        self.get_data_path("verify_and_copy_file/dir3"),
                    ],
                    "file.txt",
                    output_dir,
                )

    def test_write_with_preserved_header(self):
        header = "## this is a preserved header line\n"
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]}, index=["row1", "row2"])

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.tsv")

            _write_with_preserved_header(output_path, header, df)

            with open(output_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            self.assertEqual(lines[0], header)

            self.assertIn("row1\t1\t3\n", lines)
            self.assertIn("row2\t2\t4\n", lines)

    def test_read_table_with_content(self):
        header, df = _read_table_and_index(
            self.get_data_path("read_table_and_index/file.txt"),
            header_lines=2,
            index_prefix="CP",
            offset=7,
        )

        self.assertEqual(header, '## header\n"mz"\t"mzmin"\t"mzmax"\n')
        self.assertListEqual(list(df.index), ['"CP8"', '"CP9"'])

    def test_check_headers_passes(self):
        df1 = pd.DataFrame(columns=["A", "B", "C"])
        df2 = pd.DataFrame(columns=["A", "B", "C"])
        df3 = pd.DataFrame(columns=["A", "B", "C"])
        _check_headers([df1, df2, df3], "test_file.csv")

    def test_check_headers_raises_with_message(self):
        df1 = pd.DataFrame(columns=["A", "B", "C"])
        df2 = pd.DataFrame(columns=["A", "X", "C"])
        df3 = pd.DataFrame(columns=["A", "B", "C"])
        expected_regex = (
            r"There is a column mismatch in one of the files called: file\.txt\n"
            r"Columns of DataFrame at index 0:\nA,B,C\n"
            r"Columns of DataFrame at index 1:\nA,X,C"
        )
        with self.assertRaisesRegex(ValueError, expected_regex):
            _check_headers([df1, df2, df3], "file.txt")

    def test_remove_dates_json(self):
        test_file = self.get_data_path(
            os.path.join(
                "verify_and_copy_file", "dir1", "xcms_experiment_process_history.json"
            )
        )

        with open(test_file, "r", encoding="utf-8") as f:
            result = _remove_dates_json(f)

        for step in result["value"]:
            self.assertNotIn("date", step["attributes"])
