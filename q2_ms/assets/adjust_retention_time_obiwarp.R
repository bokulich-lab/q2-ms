#!/usr/local/bin/Rscript --vanilla

library(xcms)
library(MsIO)
library(Spectra)
library(optparse)

# Define command-line options
option_list <- list(
  make_option(opt_str = "--spectra", type = "character"),
  make_option(opt_str = "--chromatographic_peaks", type = "character"),
  make_option(opt_str = "--bin_size", type = "numeric"),
  make_option(opt_str = "--center_sample", type = "integer"),
  make_option(opt_str = "--response", type = "numeric"),
  make_option(opt_str = "--dist_fun", type = "character"),
  make_option(opt_str = "--gap_init", type = "numeric"),
  make_option(opt_str = "--gap_extend", type = "numeric"),
  make_option(opt_str = "--factor_diag", type = "numeric"),
  make_option(opt_str = "--factor_gap", type = "numeric"),
  make_option(opt_str = "--local_alignment", type = "logical"),
  make_option(opt_str = "--init_penalty", type = "numeric"),
  make_option(opt_str = "--subset", type = "integer"),
  make_option(opt_str = "--subset_adjust", type = "character"),
  make_option(opt_str = "--rtime_difference_threshold", type = "numeric"),
  make_option(opt_str = "--threads", type = "integer"),
  make_option(opt_str = "--output_path", type = "character"),
  make_option(opt_str = "--chunk_size", type = "integer")
)

# Parse arguments
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

XCMSExperiment <- readMsObject(XcmsExperiment(), PlainTextParam(opt$chromatographic_peaks))

# Set parameters
ObiwarpParams <- ObiwarpParam(
  binSize = opt$bin_size,
  response = opt$response,
  distFun = opt$dist_fun,
  factorDiag = opt$factor_diag,
  factorGap = opt$factor_gap,
  localAlignment = opt$local_alignment,
  initPenalty = opt$init_penalty,
  rtimeDifferenceThreshold = opt$rtime_difference_threshold
)

if (!is.null(opt$center_sample)) ObiwarpParams@centerSample <- opt$center_sample
if (!is.null(opt$gap_init)) ObiwarpParams@gapInit <- opt$gap_init
if (!is.null(opt$gap_extend)) ObiwarpParams@gapExtend <- opt$gap_extend
if (!is.null(opt$subset)) ObiwarpParams@subset <- opt$subset
if (!is.null(opt$subset_adjust)) ObiwarpParams@subsetAdjust <- opt$subset_adjust

# Adjust retention time using the Obiwarp algorithm
XCMSExperimentRT <- adjustRtime(
  object = XCMSExperiment,
  param = ObiwarpParams,
  chunkSize = opt$chunk_size,
  BPPARAM = MulticoreParam(workers = opt$threads)
)

# Export the XCMSExperiment object to the directory format
saveMsObject(XCMSExperimentRT, param = PlainTextParam(path = opt$output_path))
