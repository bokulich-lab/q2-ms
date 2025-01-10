# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import json
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


class MSExperimentLinkMColsFormat(model.TextFileFormat):
    def _validate(self):
        with open(str(self), "r") as file:
            first_line = file.readline().strip()

        if first_line != '"subsetBy"':
            raise ValidationError(
                "Header does not match MSExperimentLinkMColsFormat. It must "
                "consist of the following line:\n"
                '"subsetBy"\n\n'
                "Found instead:\n"
                f"{first_line}"
            )

    def _validate_(self, level):
        self._validate()


class MSExperimentSampleDataLinksSpectra(model.TextFileFormat):
    def _validate(self):
        first_line = pd.read_csv(str(self), sep="\t", nrows=0).columns.tolist()

        if len(first_line) != 2:
            raise ValidationError(
                "File does not match MSExperimentLinkMColsFormat. "
                "It must consist of exactly two columns."
            )

    def _validate_(self, level):
        self._validate()


class MSExperimentSampleDataFormat(model.TextFileFormat):
    def _validate(self):
        header_exp = ["sample_name", "sample_group", "spectraOrigin"]

        header_obs = pd.read_csv(str(self), sep="\t", nrows=0).columns.tolist()

        if header_exp != header_obs:
            raise ValidationError(
                "Header does not match MSExperimentSampleDataFormat. It must "
                "consist of the following columns:\n"
                + ", ".join(header_exp)
                + "\n\nFound instead:\n"
                + ", ".join(header_obs)
            )

    def _validate_(self, level):
        self._validate()


class SpectraProcessingQueueFormat(model.TextFileFormat):
    def _validate(self):
        try:
            with self.open() as file:
                content = file.read()
            data = json.loads(content)

            if not isinstance(data, list):
                raise ValidationError(
                    "File does not match SpectraProcessingQueueFormat. "
                    "The root element must be a list."
                )

            parsed_item = json.loads(data[0])

            required_keys = {"type", "attributes", "value"}
            if not required_keys.issubset(parsed_item.keys()):
                raise ValidationError(
                    "File does not match SpectraProcessingQueueFormat. "
                    "JSON object must contain the keys: " + ", ".join(required_keys)
                )

        except json.JSONDecodeError as e:
            raise ValidationError(f"File is not valid JSON: {e}")

    def _validate_(self, level):
        self._validate()


class SpectraSlotsFormat(model.TextFileFormat):
    def _validate(self):
        expected_keys = {
            "processingQueueVariables",
            "processing",
            "processingChunkSize",
            "backend",
        }

        with self.open() as file:
            lines = file.readlines()

        keys = set()
        for line in lines:
            if "=" not in line:
                continue

            key = line.split("=", 1)[0].strip()
            keys.add(key)

        if keys != expected_keys:
            raise ValidationError(
                "File does not match SpectraSlotsFormat. "
                "File must have the following structure:\n"
                "processingQueueVariables = ...\n"
                "processing = ...\n"
                "processingChunkSize = ...\n"
                "backend = ...\n"
            )

    def _validate_(self, level):
        self._validate()


class XCMSExperimentChromPeakDataFormat(model.TextFileFormat):
    def _validate(self):
        header_exp = ["ms_level", "is_filled"]
        header_obs = pd.read_csv(str(self), sep="\t", nrows=0).columns.tolist()

        if header_exp != header_obs:
            raise ValidationError(
                "Header does not match XCMSExperimentChromPeakDataFormat. It must "
                "consist of the following columns:\n"
                + ", ".join(header_exp)
                + "\n\nFound instead:\n"
                + ", ".join(header_obs)
            )

    def _validate_(self, level):
        self._validate()


class XCMSExperimentChromPeaksFormat(model.TextFileFormat):
    def _validate(self):
        header_exp = [
            "mz",
            "mzmin",
            "mzmax",
            "rt",
            "rtmin",
            "rtmax",
            "into",
            "intb",
            "maxo",
            "sn",
            "sample",
        ]
        header_obs = pd.read_csv(str(self), sep="\t", nrows=0).columns.tolist()

        if header_exp != header_obs:
            raise ValidationError(
                "Header does not match XCMSExperimentChromPeaksFormat. It must "
                "consist of the following columns:\n"
                + ", ".join(header_exp)
                + "\n\nFound instead:\n"
                + ", ".join(header_obs)
            )

    def _validate_(self, level):
        self._validate()
