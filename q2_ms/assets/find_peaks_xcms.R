#!/usr/bin/env Rscript

library(xcms)
library(MsExperiment)
library(MsIO)


update_params <- function(params, opt) {
  for (key in names(params)) {
    if (!is.null(opt[[key]])) {
      params[[key]] <- opt[[key]]
    }
  }
  return(params)
}

# Define command-line options
option_list <- list(
  make_option(opt_str = "--mzml_files", type = "character"),
  make_option(opt_str = "--ppm", type = "numeric"),
  make_option(opt_str = "--min_peakwidth", type = "numeric"),
  make_option(opt_str = "--max_peakwidth", type = "numeric"),
  make_option(opt_str = "--snthresh", type = "numeric"),
  make_option(opt_str = "--prefilter_k", type = "numeric"),
  make_option(opt_str = "--prefilter_i", type = "numeric"),
  make_option(opt_str = "--mz_center_fun", type = "numeric"),
  make_option(opt_str = "--integrate", type = "integer"),
  make_option(opt_str = "--mzdiff", type = "numeric"),
  make_option(opt_str = "--fitgauss", type = "logical"),
  make_option(opt_str = "--noise", type = "numeric"),
  make_option(opt_str = "--first_baseline_check", type = "logical"),
  make_option(opt_str = "--ms_level", type = "integer"),
  make_option(opt_str = "--threads", type = "integer"),
  make_option(opt_str = "--output_path", type = "character")
)

# Parse arguments
opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

# Get full paths to mzML files and read them into an MsExperiment object
mzml_files <- list.files(opt$mzml_files, pattern = "\\.mzML$", full.names = TRUE)
msexperiment <- readMsExperiment(spectraFiles = mzml_files, sampleData = pd, BPPARAM = SerialParam())

# Load default parameters for CentWave
CentWaveParams <- CentWaveParam(method="centWave")

# Update params with command-line arguments
CentWaveParams <- update_params(CentWaveParams, opt)

# Find peaks using the CentWave algorithm
XCMSExperiment <- findChromPeaks(chr_raw, param = CentWaveParams)

# Export the XCMSExperiment object to the directory format
saveMsObject(XCMSExperiment, param = PlainTextParam(path = opt$output_path))
