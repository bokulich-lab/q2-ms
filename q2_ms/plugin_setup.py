# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import importlib

from q2_types.metadata import ImmutableMetadata
from q2_types.sample_data import SampleData
from qiime2.core.type import Choices, Properties, Str, TypeMap
from qiime2.plugin import Citations, Metadata, Plugin

from q2_ms import __version__
from q2_ms.types import (
    MSP,
    MatchedSpectra,
    MatchedSpectraDirFmt,
    MatchedSpectraFormat,
    MSBackendDataFormat,
    MSExperimentLinkMColsFormat,
    MSExperimentSampleDataFormat,
    MSExperimentSampleDataLinksSpectra,
    MSPDirFmt,
    MSPFormat,
    SpectraSlotsFormat,
    XCMSExperiment,
    XCMSExperimentChromPeakDataFormat,
    XCMSExperimentChromPeaksFormat,
    XCMSExperimentDirFmt,
    XCMSExperimentFeatureDefinitionsFormat,
    XCMSExperimentFeaturePeakIndexFormat,
    XCMSExperimentJSONFormat,
    mzML,
    mzMLDirFmt,
    mzMLFormat,
)
from q2_ms.xcms.database import fetch_massbank
from q2_ms.xcms.metadata import create_spectral_metadata
from q2_ms.xcms.read_ms_experiment import read_ms_experiment

citations = Citations.load("citations.bib", package="q2_ms")

plugin = Plugin(
    name="ms",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-ms",
    package="q2_ms",
    description="A QIIME 2 plugin for MS data processing.",
    short_description="A QIIME 2 plugin for MS data processing.",
)

plugin.methods.register_function(
    function=fetch_massbank,
    inputs={},
    outputs=[("massbank", MSP)],
    parameters={},
    input_descriptions={},
    output_descriptions={"massbank": "MassBank spectral library in NIST MSP format."},
    parameter_descriptions={},
    name="Fetch MassBank spectral library",
    description=(
        "Fetch the latest MassBank spectral library in NIST MSP format. It is "
        "downloaded from github.com/MassBank/MassBank-data."
    ),
    citations=[],
)

P_ms_level, I_xcms_experiment, _ = TypeMap(
    {
        (Str % Choices(["1"]), XCMSExperiment): ImmutableMetadata,
        (Str % Choices(["1"]), XCMSExperiment % Properties("peaks")): ImmutableMetadata,
        (
            Str % Choices(["1"]),
            XCMSExperiment % Properties("features"),
        ): ImmutableMetadata,
        (Str % Choices(["1"]), XCMSExperiment % Properties("MS2")): ImmutableMetadata,
        (
            Str % Choices(["1"]),
            XCMSExperiment % Properties("MS2", "peaks"),
        ): ImmutableMetadata,
        (
            Str % Choices(["1"]),
            XCMSExperiment % Properties("MS2", "features"),
        ): ImmutableMetadata,
        (Str % Choices(["2"]), XCMSExperiment % Properties("MS2")): ImmutableMetadata,
        (
            Str % Choices(["2"]),
            XCMSExperiment % Properties("MS2", "peaks"),
        ): ImmutableMetadata,
        (
            Str % Choices(["2"]),
            XCMSExperiment % Properties("MS2", "features"),
        ): ImmutableMetadata,
    }
)


plugin.methods.register_function(
    function=create_spectral_metadata,
    inputs={"xcms_experiment": I_xcms_experiment},
    outputs=[("spectral_metadata", ImmutableMetadata)],
    parameters={"ms_level": P_ms_level},
    input_descriptions={"xcms_experiment": "XCMSExperiment."},
    output_descriptions={"spectral_metadata": "Spectral metadata of all MS1 scans."},
    parameter_descriptions={
        "ms_level": "If the spectral metadata should be created for MS1 or MS2 scans."
    },
    name="Create spectral metadata",
    description=(
        "This action creates a spectral metadata table from a XCMSExperiment artifact. "
        "This metadata can be used to plot total ion chromatograms or base peak "
        "chromatograms and other line and box plots with q2-vizard.\n\nNOTE:\nThe data "
        "gets filtered by MS level and only MS1 scans are retained. Also the name of "
        "the column defining the sample id in the sample data will get '_' added as a "
        "suffix."
    ),
    citations=[],
)

plugin.methods.register_function(
    function=read_ms_experiment,
    inputs={"spectra": SampleData[mzML]},
    outputs=[("xcms_experiment", XCMSExperiment)],
    parameters={"sample_metadata": Metadata},
    input_descriptions={"spectra": "Spectra data as mzML files."},
    output_descriptions={
        "xcms_experiment": "XCMSExperiment object exported to plain text."
    },
    parameter_descriptions={
        "sample_metadata": (
            "Optional sample metadata. This can be used in downstream analyses for "
            "example for feature filtering with 'filter-features' and subset-based "
            "alignment with 'adjust-retention-time-obiwarp'. Samples should be ordered "
            "by injection index for subset-based alignment. "
        ),
    },
    name="Read spectra into XCMS experiment",
    description=(
        "This function uses the XCMS package to read in MS data from mzML files into "
        "an XcmsExperiment object and export it as plain text files."
    ),
    citations=[
        citations["kosters2018pymzml"],
        citations["smith2006xcms"],
        citations["msexperiment2024"],
    ],
)

# Registrations
plugin.register_semantic_types(
    mzML,
    XCMSExperiment,
    MSP,
    MatchedSpectra,
)

plugin.register_semantic_type_to_format(SampleData[mzML], artifact_format=mzMLDirFmt)
plugin.register_semantic_type_to_format(
    XCMSExperiment, artifact_format=XCMSExperimentDirFmt
)
plugin.register_semantic_type_to_format(MSP, artifact_format=MSPDirFmt)
plugin.register_semantic_type_to_format(
    MatchedSpectra, artifact_format=MatchedSpectraDirFmt
)


plugin.register_formats(
    mzMLFormat,
    mzMLDirFmt,
    MSBackendDataFormat,
    MSExperimentLinkMColsFormat,
    MSExperimentSampleDataFormat,
    MSExperimentSampleDataLinksSpectra,
    SpectraSlotsFormat,
    XCMSExperimentChromPeakDataFormat,
    XCMSExperimentChromPeaksFormat,
    XCMSExperimentDirFmt,
    XCMSExperimentFeatureDefinitionsFormat,
    XCMSExperimentFeaturePeakIndexFormat,
    XCMSExperimentJSONFormat,
    MSPFormat,
    MSPDirFmt,
    MatchedSpectraFormat,
    MatchedSpectraDirFmt,
)

importlib.import_module("q2_ms.types._validators")
