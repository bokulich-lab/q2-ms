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
  make_option(opt_str = "--target_spectra", type = "character"),
  make_option(opt_str = "--map_fun", type = "character"),
  make_option(opt_str = "--type_join", type = "character"),
  make_option(opt_str = "--tolerance", type = "numeric"),
  make_option(opt_str = "--ppm", type = "numeric"),
  make_option(opt_str = "--fun", type = "character"),
  make_option(opt_str = "--fun_m", type = "numeric"),
  make_option(opt_str = "--fun_n", type = "numeric"),
  make_option(opt_str = "--fun_na_rm", type = "logical"),
  make_option(opt_str = "--require_precursor", type = "numeric"),
  make_option(opt_str = "--require_precursor_peak", type = "numeric"),
  make_option(opt_str = "--thresh_fun", type = "character"),
  make_option(opt_str = "--tolerance_rt", type = "integer"),
  make_option(opt_str = "--percent_rt", type = "numeric"),
  make_option(opt_str = "--scale_peaks", type = "logical"),
  make_option(opt_str = "--filter_intensity", type = "numeric"),
  make_option(opt_str = "--filter_num_peaks", type = "integer"),
  make_option(opt_str = "--threads", type = "integer"),
  make_option(opt_str = "--matched_spectra", type = "character")
)

# Parse arguments
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

# Load the XCMSExperiment
XCMSExperiment <- readMsObject(XcmsExperiment(), PlainTextParam(opt$xcms_experiment), spectraPath=opt$spectra)

# Extract the spectra from the XCMSExperiment
querySpectra <- chromPeakSpectra(XCMSExperiment, return.type = "Spectra")

# Load the target spectra library
targetSpectra <- Spectra(opt$target_spectra, source = MsBackendMsp(), BPPARAM=MulticoreParam(workers=opt$threads))

# Filter intensity
if (opt$filter_intensity) {
    low_int <- function(x) {x > max(x, na.rm = TRUE) * opt$filter_intensity}
    querySpectra <- filterIntensity(querySpectra, intensity = low_int)
    targetSpectra <- filterIntensity(targetSpectra, intensity = low_int)
}

# Filter num peaks per spectra
if (opt$filter_num_peaks) {
    querySpectra <- querySpectra[lengths(querySpectra) > opt$filter_num_peaks]
    targetSpectra <- targetSpectra[lengths(targetSpectra) > opt$filter_num_peaks]
}

# Scale the peaks
if (opt$scale_peaks) {
    querySpectra <- scalePeaks(querySpectra)
    targetSpectra <- scalePeaks(targetSpectra)
}

# Create paramter object for CentWave
CompareSpectraParams <- CompareSpectraParam(
  MAPFUN = match.fun(opt$map_fun),
  type = opt$type_join,
  tolerance = opt$tolerance,
  ppm = opt$ppm,
  FUN = match.fun(opt$fun),
  n = opt$fun_n,
  m = opt$fun_m,
  na.rm = opt$fun_na_rm,
  requirePrecursor =  opt$require_precursor,
  requirePrecursorPeak = opt$require_precursor_peak,
  THRESHFUN = eval(parse(text = opt$thresh_fun)),
  toleranceRt = opt$tolerance_rt,
  percentRt = opt$percent_rt,
)

# Find peaks using the CentWave algorithm
matchedSpectra <- matchSpectra(
  query = XCMSExperiment,
  target = CentWaveParams,
  param = CompareSpectraParams,
)

matched_df <- matchedData(mtch)
list_cols <- sapply(matched_df, is.list)

matched_df[list_cols] <- lapply(matched_df[list_cols], function(col) {
  sapply(col, paste, collapse = ";")
})

# Write to disk
write.table(matched_df,
            file = file.path(opt$matched_spectra, "matched_spectra.txt"),
            sep = "\t", row.names = FALSE, quote = FALSE)
