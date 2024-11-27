# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import pymzml
from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


class mzMLFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        try:
            run = pymzml.run.Reader(str(self))
            for _ in run:
                pass
        except Exception as e:
            raise ValidationError(f"File is not a valid mzML format: {e}")

    def _validate_(self, level):
        self._validate()


class mzMLDirFmt(model.DirectoryFormat):
    mzml = model.FileCollection(r".*\.mzML$", format=mzMLFormat)

    @mzml.set_path_maker
    def mzml_path_maker(self, sample_id):
        return f"{sample_id}.mzML"
