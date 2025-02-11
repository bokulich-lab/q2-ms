import pandas as pd
import qiime2
from qiime2.plugin.testing import TestPluginBase

from q2_ms.types import mzMLDirFmt
from q2_ms.xcms.read_ms_experiment import _validate_metadata, read_ms_experiment


class TestReadMsExperiment(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_read_ms_experiment(self):
        spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        sample_data = pd.read_csv(
            self.get_data_path("faahKO_sample_data/sample_data.tsv"),
            sep="\t",
            index_col=0,
        )
        xcms_experiment = read_ms_experiment(
            spectra=spectra,
            sample_metadata=qiime2.Metadata(sample_data),
        )
        # peaks = pd.read_csv(
        #     os.path.join(str(xcms_experiment), "ms_backend_data.txt"),
        #     sep="\t",
        #     index_col=0,
        #     skiprows=1,
        # )
        print(xcms_experiment)


class TestValidateMetadata(TestPluginBase):
    package = "q2_ms.xcms.tests"

    def test_validate_metadata_missing(self):
        spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        metadata = pd.read_csv(
            self.get_data_path("faahKO_sample_data/sample_data_missing.tsv"),
            sep="\t",
            index_col=0,
        )
        with self.assertRaisesRegex(ValueError, "missing in sample-metadata: {'wt22'}"):
            _validate_metadata(
                spectra_path=str(spectra),
                metadata=metadata,
            )

    def test_read_ms_experiment_added(self):
        spectra = mzMLDirFmt(self.get_data_path("faahKO"), mode="r")
        metadata = pd.read_csv(
            self.get_data_path("faahKO_sample_data/sample_data_added.tsv"),
            sep="\t",
            index_col=0,
        )
        with self.assertRaisesRegex(ValueError, "missing in spectra: {'wt23'}"):
            _validate_metadata(
                spectra_path=str(spectra),
                metadata=metadata,
            )
