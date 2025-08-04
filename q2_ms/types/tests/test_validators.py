# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.core.exceptions import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import XCMSExperimentDirFmt
from q2_ms.types._validators import (
    validate_xcms_experiment_features,
    validate_xcms_experiment_ms2,
    validate_xcms_experiment_peaks,
)


class TestValidators(TestPluginBase):
    package = "q2_ms.types.tests"

    def test_validate_xcms_experiment_ms2_error(self):
        data = XCMSExperimentDirFmt(self.get_data_path("XCMSExperiment"), mode="r")
        with self.assertRaisesRegex(ValidationError, "The property 'MS2'"):
            validate_xcms_experiment_ms2(data, None)

    def test_validate_xcms_experiment_ms2(self):
        data = XCMSExperimentDirFmt(self.get_data_path("ms_backend_MS2"), mode="r")
        validate_xcms_experiment_ms2(data, None)

    def test_validate_xcms_experiment_peaks_error(self):
        data = XCMSExperimentDirFmt(self.temp_dir.name, mode="r")
        with self.assertRaisesRegex(ValidationError, "The property 'peaks'"):
            validate_xcms_experiment_peaks(data, None)

    def test_validate_xcms_experiment_peaks(self):
        data = XCMSExperimentDirFmt(self.get_data_path("XCMSExperiment"), mode="r")
        validate_xcms_experiment_peaks(data, None)

    def test_validate_xcms_experiment_features_error(self):
        data = XCMSExperimentDirFmt(self.temp_dir.name, mode="r")
        with self.assertRaisesRegex(ValidationError, "The property 'features'"):
            validate_xcms_experiment_features(data, None)

    def test_validate_xcms_experiment_features(self):
        data = XCMSExperimentDirFmt(self.get_data_path("XCMSExperiment"), mode="r")
        validate_xcms_experiment_features(data, None)
