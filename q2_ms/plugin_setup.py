# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.core.type import Choices, Str, Visualization
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
from q2_ms.xcms.metadata import chromatogram

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

plugin.pipelines.register_function(
    function=chromatogram,
    inputs={"xcms_experiment": XCMSExperiment},
    outputs=[("chromatogram", Visualization)],
    parameters={
        "x_measure": Str,
        "y_measure": Str,
        "replicate_method": Str % Choices("none", "median", "mean"),
        "group_by": Str,
        "title": Str,
    },
    input_descriptions={"xcms_experiment": "XCMSExperiment."},
    output_descriptions={"chromatogram": "Visualization"},
    parameter_descriptions={
        "x_measure": (
            "Numeric measure from the input Metadata that should be plotted on the "
            "x-axis."
        ),
        "y_measure": (
            "Numeric measure from the input Metadata that should be plotted on the "
            "y-axis."
        ),
        "replicate_method": (
            "The method for averaging replicates if present in the chosen `x_measure`. "
            "Available methods are `median` and `mean`."
        ),
        "group_by": (
            "Categorical measure from the input Metadata that should be used for "
            "grouping the lineplot."
        ),
        "title": "The title of the lineplot.",
    },
    name="chromatogram",
    description="chromatogram",
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
