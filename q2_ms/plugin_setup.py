# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.metadata import ImmutableMetadata
from q2_types.sample_data import SampleData
from qiime2.plugin import Citations, Plugin

from q2_ms import __version__
from q2_ms.types import (
    MSP,
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

plugin.methods.register_function(
    function=create_spectral_metadata,
    inputs={"xcms_experiment": XCMSExperiment},
    outputs=[("spectral_metadata", ImmutableMetadata)],
    parameters={},
    input_descriptions={"xcms_experiment": "XCMSExperiment."},
    output_descriptions={"spectral_metadata": "Spectral metadata of all MS1 scans."},
    parameter_descriptions={},
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

# Registrations
plugin.register_semantic_types(
    mzML,
    XCMSExperiment,
    MSP,
)

plugin.register_semantic_type_to_format(SampleData[mzML], artifact_format=mzMLDirFmt)
plugin.register_semantic_type_to_format(
    XCMSExperiment, artifact_format=XCMSExperimentDirFmt
)
plugin.register_semantic_type_to_format(MSP, artifact_format=MSPDirFmt)

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
)
