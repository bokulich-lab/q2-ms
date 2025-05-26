# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.core.type import Bool, Choices, Float, Int, Properties, Range, Str
from qiime2.plugin import Citations, Plugin

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
from q2_ms.xcms import match_spectra
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
    function=match_spectra,
    inputs={
        "spectra": SampleData[mzML],
        "xcms_experiment": XCMSExperiment % Properties("peaks"),
        "target_spectra": MSP,
    },
    outputs=[("matched_spectra", MatchedSpectra)],
    parameters={
        "map_fun": Str % Choices(["joinPeaks", "joinPeaksGnps"]),
        "type_join": Str % Choices(["outer", "left", "right", "inner"]),
        "tolerance": Float % Range(0, None),
        "ppm": Float % Range(0, None),
        "fun": Str
        % Choices(["ndotproduct", "neuclidean", "navdist", "nspectraangle", "gnps"]),
        "fun_m": Float,
        "fun_n": Float,
        "fun_na_rm": Bool,
        "require_precursor": Bool,
        "require_precursor_peak": Bool,
        "thresh_fun": Str,
        "tolerance_rt": Float % Range(0, None),
        "percent_rt": Float,
        "scale_peaks": Bool,
        "filter_intensity": Float % Range(0, 1),
        "filter_num_peaks": Int % Range(1, None),
        "threads": Int % Range(1, None),
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
        "map_fun": (
            "Function used to map peaks between the compared spectra. 'joinPeaks' maps "
            "peaks from two spectra allowing to specify the type of join that should "
            "be performed. 'joinPeaksGnps' matches/maps peaks between spectra with the "
            "same approach used in GNPS: peaks are considered matching if a) the "
            "difference in their m/z values is smaller than defined by tolerance and "
            "ppm (this is the same as joinPeaks) and b) the difference of their m/z "
            "adjusted for the difference of the spectras' precursor is smaller than "
            "defined by tolerance and ppm. Based on this definition, peaks in x can "
            "match up to two peaks in y hence peaks in the returned matrices might be "
            "reported multiple times."
        ),
        "type_join": (
            "Specify the type of join that should be performed. With 'outer' each peak "
            "in x will be matched with each peak in y, for peaks that do not match any "
            "peak in the other spectra an NA intensity is returned. With 'left' all "
            "peaks from the left spectrum (x) will be matched with peaks in y. Peaks "
            "in y that do not match any peak in x are omitted. 'right' is the same as "
            "'left' only for y. Only peaks that can be matched between x and y are "
            "returned with 'inner', i.e. only peaks present in both spectra are "
            "reported."
        ),
        "tolerance": (
            "Defines the absolute maximal accepted difference between m/z values. This "
            "will be used in compareSpectra as well as for eventual precursor m/z "
            "matching."
        ),
        "ppm": (
            "Defines a relative, m/z-dependent, maximal accepted difference between "
            "m/z values. This will be used in compareSpectra as well as for eventual "
            "precursor m/z matching."
        ),
        "fun": (
            "Function used to calculate similarity between spectra. The normalized dot "
            "product (ndotproduct) is described in Stein and Scott 1994 as: NDP = "
            r"\frac{∑(W_1 W_2)^2}{∑(W_1)^2 ∑(W_2)^2}; where W_i = x^m * y^n. The "
            "normalized euclidean distance (neuclidean) is described in Stein and "
            r"Scott 1994 as: NED = (1 + \frac{∑((W_1 - W_2)^2)}{sum((W_2)^2)})^{-1}; "
            "where W_i = x^m * y^n. The normalized absolute values distance (navdist) "
            r"is described in Stein and Scott 1994 as: NED = (1 + \frac{∑(|W_1 - W_2|)}"
            "{sum((W_2))})^{-1}; where W_i = x^m * y^n. The normalized spectra angle "
            r"is described in Toprak et al 2014 as: NSA = 1 - \frac{2*\cos^{-1}(W_1 "
            r"\cdot W_2)}{π}; where W_i = x^m * y^n. Where x and y are the m/z and "
            "intensity values. the method gnps calculates the GNPS similarity score. "
            "To use gnps, the join_gnps method has to be used with the map_fun "
            "parameter. For multi-mapping peaks the pair with the higher similarity "
            "are considered in the final score calculation."
        ),
        "fun_m": (
            "Weighting for the mz values. Default: 0 means don't weight by the mz "
            "values."
        ),
        "fun_n": (
            "Weighting for the intensity values. Default: 0.5 means effectly using "
            "sqrt(x[,2]) and sqrt(y[,2])."
        ),
        "fun_na_rm": ("Should NA be removed prior to calculation of the distance."),
        "require_precursor": (
            "Whether only target spectra are considered in the similarity calculation "
            "with a precursor m/z that matches the precursor m/z of the query spectrum "
            "(considering also ppm and tolerance). With requirePrecursor = TRUE (the "
            "default) the function will complete much faster, but will not find any "
            "hits for target (or query spectra) with missing precursor m/z. It is "
            "suggested to check first the availability of the precursor m/z in target "
            "and query."
        ),
        "require_precursor_peak": (
            "Whether only target spectra will be considered in the spectra similarity "
            "calculation that have a peak with an m/z matching the precursor m/z of "
            "the query spectrum. Defaults to requirePrecursorPeak = FALSE. It is "
            "suggested to check first the availability of the precursor m/z in query, "
            "as no match will be reported for query spectra with missing precursor m/z."
        ),
        "thresh_fun": (
            "Defines the function applied to the similarity score to define which "
            "target spectra are considered matching. Defaults to function(x) "
            "which(x >= 0.7) hence selects all target spectra matching a query "
            "spectrum with a similarity higher or equal than 0.7. Any function that "
            "takes a numeric vector with similarity scores from the comparison of a "
            "query spectrum with all target spectra as input and returns a logical "
            "vector (same dimensions as the similarity scores)."
        ),
        "tolerance_rt": (
            "Defines the maximal accepted (absolute) difference in retention time "
            "between query and target spectra. By default the retention time-based "
            "filter is not considered."
        ),
        "percent_rt": (
            "Defines the maximal accepted relative difference in retention time "
            "between query and target spectra expressed in percentage of the query rt. "
            "For percent_rt = 10, similarities are defined between the query spectrum "
            "and all target spectra with a retention time within query rt +/- 10% of "
            "the query. By default the retention time-based filter is not considered. "
            "Thus, to consider the percent_rt parameter, tolerance_rt should be set to "
            "a value different than that."
        ),
        "scale_peaks": (
            "Whether to scale the peak intensities per spectrum using the scalePeaks() "
            "function. While most spectra similarity scoring algorithms are "
            "independent of absolute peak intensities, peak scaling will improve the "
            "graphical visualization of results."
        ),
        "intensity_threshold": (
            "This parameter defines the relative intensity threshold used to remove "
            "low-intensity peaks, removing all peaks that have a lower intensity than "
            "the threshold relative to the peak with the maximum intensity in the "
            "spectrum."
        ),
        "num_peaks_threshold": (
            "Spectra with the same amount or fewer peaks than this threshold will be "
            "removed."
        ),
        "threads": (
            "Number of threads to be used. Multiple threads will only be used for "
            "reading in target spectra."
        ),
    },
    name="Match Spectra",
    description=(
        "This function uses the function matchSpectra() of the MetaboAnnotation "
        "package to match query and target spectra."
    ),
    citations=[],
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
