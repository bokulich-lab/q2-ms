# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.core.type import Bool, Choices, Float, Int, Properties, Range, Str, TypeMap
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
from q2_ms.xcms.find_peaks_centwave import find_peaks_centwave
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

plugin.methods.register_function(
    function=read_ms_experiment,
    inputs={"spectra": SampleData[mzML]},
    outputs=[("xcms_experiment", XCMSExperiment % Properties("Peaks"))],
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

I_find_peaks, O_find_peaks = TypeMap(
    {
        XCMSExperiment: XCMSExperiment % Properties("peaks"),
        XCMSExperiment
        % Properties("rt-adjusted"): XCMSExperiment
        % Properties("peaks", "rt-adjusted"),
    }
)

plugin.methods.register_function(
    function=find_peaks_centwave,
    inputs={
        "spectra": SampleData[mzML],
        "xcms_experiment": I_find_peaks,
    },
    outputs=[("xcms_experiment_peaks", O_find_peaks)],
    parameters={
        "ppm": Float % Range(0, None),
        "min_peak_width": Float % Range(0, None),
        "max_peak_width": Float % Range(0, None),
        "sn_thresh": Float % Range(0, None),
        "prefilter_k": Float,
        "prefilter_i": Float,
        "mz_center_fun": Str
        % Choices(["wMean", "mean", "apex", "wMeanApex3", "meanApex3"]),
        "integrate": Int % Range(1, 3),
        "mz_diff": Float,
        "fit_gauss": Bool,
        "noise": Float,
        "first_baseline_check": Bool,
        "ms_level": Int % Range(1, 3),
        "threads": Int % Range(1, None),
        "extend_length_msw": Bool,
        "verbose_columns": Bool,
        "verbose_beta_columns": Bool,
    },
    input_descriptions={
        "spectra": "Spectra data as mzML files.",
        "xcms_experiment": "XCMSExperiment object exported to plain text.",
    },
    output_descriptions={
        "xcms_experiment_peaks": (
            "XCMSExperiment object with chromatographic peak information exported to "
            "plain text."
        )
    },
    parameter_descriptions={
        "ppm": (
            "Defines the maximal tolerated m/z deviation in consecutive scans in parts "
            "per million (ppm) for the initial ROI definition."
        ),
        "min_peak_width": (
            "Defines the minimal expected approximate peak width in chromatographic "
            "space in seconds."
        ),
        "max_peak_width": (
            "Defines the maximal expected approximate peak width in chromatographic "
            "space in seconds."
        ),
        "sn_thresh": "Defines the signal to noise ratio cutoff.",
        "prefilter_k": (
            "Specifies the prefilter step for the first analysis step (ROI detection). "
            "Mass traces are only retained if they contain at least k peaks."
        ),
        "prefilter_i": (
            "Specifies the prefilter step for the first analysis step (ROI detection). "
            "Mass traces are only retained if they contain peaks with intensity >= i."
        ),
        "mz_center_fun": (
            "Name of the function to calculate the m/z center of the chromatographic "
            'peak. Allowed are: "wMean": intensity weighted mean of the peaks '
            'm/z values, "mean": mean of the peaks m/z values, "apex": use the m/z '
            'value at the peak apex, "wMeanApex3": intensity weighted mean of the '
            "m/z value at the peak apex and the m/z values left and right of it and "
            '"meanApex3": mean of the m/z value of the peak apex and the m/z values '
            "left and right of it."
        ),
        "integrate": (
            "Integration method. For integrate = 1 peak limits are found through "
            "descent on the mexican hat filtered data, for integrate = 2 the descent "
            "is done on the real data. The latter method is more accurate but prone "
            "to noise, while the former is more robust, but less exact."
        ),
        "mz_diff": (
            "Represents the minimum difference in m/z dimension required for peaks with"
            " overlapping retention times; can be negative to allow overlap. During "
            "peak post-processing, peaks defined to be overlapping are reduced to the "
            "one peak with the largest signal."
        ),
        "fit_gauss": (
            "Whether or not a Gaussian should be fitted to each peak. This affects "
            "mostly the retention time position of the peak."
        ),
        "noise": (
            "Allowing to set a minimum intensity required for centroids to be "
            "considered in the first analysis step (centroids with intensity < noise "
            "are omitted from ROI detection)."
        ),
        "first_baseline_check": (
            "If TRUE continuous data within regions of interest is checked to be above "
            "the first baseline."
        ),
        "ms_level": (
            "Defines the MS level on which the peak detection should be performed."
        ),
        "threads": "Number of threads to be used.",
        "extend_length_msw": (
            "Option to force centWave to use all scales when running centWave rather "
            "than truncating with the EIC length. Uses the 'open' method to extend the "
            "EIC to a integer base-2 length prior to being passed to 'convolve' rather "
            "than the default 'reflect' method. See "
            "https://github.com/sneumann/xcms/issues/445 for more information."
        ),
        "verbose_columns": (
            "Option to add additional peak meta data columns to the peaks data."
        ),
        "verbose_beta_columns": (
            "Option to calculate two additional metrics of peak quality via comparison "
            "to an idealized bell curve. Adds 'beta_cor' and 'beta_snr' to the "
            "'chromPeaks' output, corresponding to a Pearson correlation coefficient "
            "to a bell curve with several degrees of skew as well as an estimate of "
            "signal-to-noise using the residuals from the best-fitting bell curve. "
            "See https://github.com/sneumann/xcms/pull/685 and "
            "https://doi.org/10.1186/s12859-023-05533-4 for more information."
        ),
    },
    name="Find chromatographic peaks with centWave",
    description=(
        "This function uses XCMS and the centWave algorithm to perform peak "
        "density and wavelet based chromatographic peak detection for high resolution "
        "LC/MS data."
    ),
    citations=[
        citations["kosters2018pymzml"],
        citations["tautenhahn2008highly"],
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
