# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import sys

import pandas as pd
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


class MSBackendDataFormat(model.TextFileFormat):
    def _validate(self):
        header_exp_rt = [
            "msLevel",
            "rtime",
            "acquisitionNum",
            "dataOrigin",
            "polarity",
            "precScanNum",
            "precursorMz",
            "precursorIntensity",
            "precursorCharge",
            "collisionEnergy",
            "peaksCount",
            "totIonCurrent",
            "basePeakMZ",
            "basePeakIntensity",
            "ionisationEnergy",
            "lowMZ",
            "highMZ",
            "mergedScan",
            "mergedResultScanNum",
            "mergedResultStartScanNum",
            "mergedResultEndScanNum",
            "injectionTime",
            "spectrumId",
            "ionMobilityDriftTime",
            "rtime_adjusted",
            "dataStorage",
            "scanIndex",
        ]

        header_exp = header_exp_rt.pop(24)
        header_obs_1 = pd.read_csv(str(self), sep="\t", nrows=0).columns.tolist()
        header_obs_2 = pd.read_csv(
            str(self), sep="\t", skiprows=1, nrows=1
        ).columns.tolist()

        if (
            header_exp != header_obs_2 and header_exp_rt != header_obs_2
        ) or header_obs_1[0] != "# MsBackendMzR":
            raise ValidationError(
                "Header does not match MSBackendDataFormat. It must "
                "consist of the following two lines ('rtime_adjusted' is optional):\n"
                "# MsBackendMzR\n" + "\t".join(header_exp_rt) + "\n\nFound instead:\n"
                f"{header_obs_1[0]}\n" + "\t".join(header_obs_2)
            )

    def _validate_(self, level):
        self._validate()
