#!/usr/bin/env Rscript --vanilla

library(xcms)
library(Spectra)
library(MsExperiment)
library(MsIO)
library(optparse)
library(MSnbase)

# Define command-line options
option_list <- list(
  make_option(opt_str = "--spectra", type = "character"),
  make_option(opt_str = "--xcms_experiment", type = "character"),
  make_option(opt_str = "--mapfun", type = "numeric"),
  make_option(opt_str = "--tolerance", type = "numeric"),
  make_option(opt_str = "--ppm", type = "numeric"),
  make_option(opt_str = "--fun", type = "numeric"),
  make_option(opt_str = "--require_precursor", type = "numeric"),
  make_option(opt_str = "--require_precursor_peak", type = "numeric"),
  make_option(opt_str = "--threshfun", type = "character"),
  make_option(opt_str = "--tolerance_rt", type = "integer"),
  make_option(opt_str = "--percent_rt", type = "numeric"),
  make_option(opt_str = "--scale_peaks", type = "logical"),
  make_option(opt_str = "--filter_intensity", type = "numeric"),
  make_option(opt_str = "--filter_num_peaks", type = "integer"),
  make_option(opt_str = "--threads", type = "integer"),
  make_option(opt_str = "--matches", type = "character")
)

# Parse arguments
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

# Load the XCMSExperiment
XCMSExperiment <- readMsObject(XcmsExperiment(), PlainTextParam(opt$xcms_experiment), spectraPath=opt$spectra)

# Extract the spectra from the XCMSExperiment
querySpectra <- chromPeakSpectra(XCMSExperiment, return.type = "Spectra")

# Load the target spectra library
targetSpectra <- Spectra(opt$target, source = MsBackendMsp(), BPPARAM=MulticoreParam(workers=opt$threads))

# Filter intensity
if (opt$scale_peaks) {
    querySpectra <- filterIntensity(querySpectra, intensity = opt$filter_intensity)
    targetSpectra <- filterIntensity(targetSpectra, intensity = opt$filter_intensity)
}

# Filter num peaks per spectra
if (opt$scale_peaks) {
    querySpectra <- pest_ms2[lengths(pest_ms2) > opt$filter_num_peaks]
    targetSpectra <- pest_ms2[lengths(pest_ms2) > opt$filter_num_peaks]
}

# Scale the peaks
if (opt$scale_peaks) {
    querySpectra <- scalePeaks(querySpectra)
    targetSpectra <- scalePeaks(targetSpectra)
}

# Create paramter object for CentWave
CompareSpectraParams <- CompareSpectraParam(
  MAPFUN = opt$mapfun,
  tolerance = opt$tolerance,
  ppm = opt$ppm,
  FUN = opt$fun,
  requirePrecursor =  opt$require_precursor,
  requirePrecursorPeak = opt$require_precursor_peak,
  THRESHFUN = opt$threshfun,
  toleranceRt = opt$tolerance_rt,
  percentRt = opt$percent_rt,
)

# Find peaks using the CentWave algorithm
matchedSpectra <- matchSpectra(
  query = XCMSExperiment,
  target = CentWaveParams,
  param = CompareSpectraParams,
)

# Export the XCMSExperiment object to the directory format
saveMsObject(XCMSExperiment, param = PlainTextParam(path = opt$xcms_experiment_peaks))
