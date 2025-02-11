import os

import pandas as pd
import qiime2
from pandas._testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import mzMLDirFmt
from q2_ms.xcms.read_ms_experiment import read_ms_experiment


class TestRunCommand(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_find_peaks_centwave(self):
        spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        sample_data = pd.read_csv(
            self.get_data_path("faahKO_sample_data/sample_data.tsv"),
            sep="\t",
            index_col=0,
        )
        dfs = []
        for i in range(2):
            xcms_experiment = read_ms_experiment(
                spectra=spectra,
                sample_metadata=qiime2.Metadata(sample_data),
            )
            peaks = pd.read_csv(
                os.path.join(str(xcms_experiment), "ms_backend_data.txt"),
                sep="\t",
                index_col=0,
                skiprows=1,
            )
            dfs.append(peaks)
        assert_frame_equal(dfs[0], dfs[1])
        print(xcms_experiment)
