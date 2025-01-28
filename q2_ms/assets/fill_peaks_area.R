#!/usr/local/bin/Rscript --vanilla

library(xcms)
library(MsExperiment)
library(MsIO)
library(Spectra)
library(optparse)

# Define command-line options
option_list <- list(
  make_option(opt_str = "--spectra", type = "character"),
  make_option(opt_str = "--xcms_experiment", type = "character"),
  make_option(opt_str = "--mz_min", type = "character"),
  make_option(opt_str = "--mz_max", type = "character"),
  make_option(opt_str = "--rt_min", type = "character"),
  make_option(opt_str = "--rt_max", type = "character"),
  make_option(opt_str = "--threads", type = "integer"),
  make_option(opt_str = "--output_path", type = "character"),
  make_option(opt_str = "--ms_level", type = "integer")
)

# Parse arguments
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

XCMSExperiment <- readMsObject(XcmsExperiment(), PlainTextParam(opt$xcms_experiment))

# Set parameters
AreaParams <- ChromPeakAreaParam(
  mzmin = eval(parse(text = opt$mz_min)),
  mzmax = eval(parse(text = opt$mz_max)),
  rtmin = eval(parse(text = opt$rt_min)),
  rtmax = eval(parse(text = opt$rt_max))
)

# Fill gaps
XCMSExperiment <- fillChromPeaks(
  object = XCMSExperiment,
  param = AreaParams,
  msLevel = opt$ms_level,
  BPPARAM = MulticoreParam(workers = opt$threads)
)

# Export the XCMSExperiment object to the directory format
saveMsObject(XCMSExperiment, param = PlainTextParam(path = opt$output_path))
