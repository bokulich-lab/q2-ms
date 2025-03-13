# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.core.type import Choices, Str
from qiime2.plugin import Citations, Plugin

from q2_ms import __version__
from q2_ms.types import mzML, mzMLDirFmt, mzMLFormat
from q2_ms.types._format import (
    MSBackendDataFormat,
    MSExperimentLinkMColsFormat,
    MSExperimentSampleDataFormat,
    MSExperimentSampleDataLinksSpectra,
    MSPDirFmt,
    MSPFormat,
    SpectraSlotsFormat,
    XCMSExperimentChromPeakDataFormat,
    XCMSExperimentChromPeaksFormat,
    XCMSExperimentDirFmt,
    XCMSExperimentFeatureDefinitionsFormat,
    XCMSExperimentFeaturePeakIndexFormat,
    XCMSExperimentJSONFormat,
)
from q2_ms.types._type import MSP, XCMSExperiment
from q2_ms.xcms.database import fetch_massbank

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
    parameters={
        "release": Str
        % Choices(
            "2024.11",
            "2024.06",
            "2023.11",
            "2023.09",
            "2023.06",
            "2022.12.1",
            "2022.12",
            "2022.06",
            "2021.12",
            "2021.03",
            "2021.02",
            "2020.11",
        ),
    },
    input_descriptions={},
    output_descriptions={"massbank": "MassBank spectral library in NIST MSP format."},
    parameter_descriptions={
        "release": (
            "Specify the release that you want to download. Per default the latest "
            "release is downloaded."
        ),
    },
    name="Fetch MassBank spectral library",
    description=(
        "Fetch the MassBank spectral library in NIST MSP format. It is downloaded from "
        "github.com/MassBank/MassBank-data."
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
