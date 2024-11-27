# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import sys

import pymzml
from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


class mzMLFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        try:
            # Suppressing warning print "Not index found and build_index_from_scratch
            # is False". This could also be solved with setting build_index_from_scratch
            # to True but this builds the index and slows down validation.
            sys.stdout = open(os.devnull, "w")
            pymzml.run.Reader(str(self))
            sys.stdout = sys.__stdout__
        except Exception as e:
            raise ValidationError(e)

    def _validate_(self, level):
        self._validate()


class mzMLDirFmt(model.DirectoryFormat):
    mzml = model.FileCollection(r".*\.mzML$", format=mzMLFormat)

    @mzml.set_path_maker
    def mzml_path_maker(self, sample_id):
        return f"{sample_id}.mzML"
