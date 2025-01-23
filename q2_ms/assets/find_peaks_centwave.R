#!/usr/bin/env Rscript --vanilla



library(BiocParallel)
library(xcms)
library(MsExperiment)
library(MsIO)
library(jsonlite)
library(optparse)

# Define command-line options
option_list <- list(
  make_option(opt_str = "--mzml", type = "character"),
  make_option(opt_str = "--sample_metadata", type = "character"),
  make_option(opt_str = "--ppm", type = "numeric"),
  make_option(opt_str = "--min_peakwidth", type = "numeric"),
  make_option(opt_str = "--max_peakwidth", type = "numeric"),
  make_option(opt_str = "--snthresh", type = "numeric"),
  make_option(opt_str = "--prefilter_k", type = "numeric"),
  make_option(opt_str = "--prefilter_i", type = "numeric"),
  make_option(opt_str = "--mz_center_fun", type = "character"),
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
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

# Get full paths to mzML files and read them into an MsExperiment object
mzmlFiles <- list.files(opt$mzml, pattern = "\\.mzML$", full.names = TRUE)

# Create sample metadata
sampleData <- read.table(file = opt$sample_metadata, header = TRUE, sep = "\t")

# Read the mzML files and sample data into an MsExperiment object
msexperiment <- readMsExperiment(spectraFiles = mzmlFiles, sampleData = sampleData)

# Load default parameters for CentWave
CentWaveParams <- CentWaveParam(
  ppm = opt$ppm,
  peakwidth = c(opt$min_peakwidth, opt$max_peakwidth),
  snthresh = opt$snthresh,
  prefilter = c(opt$prefilter_k, opt$prefilter_i),
  mzCenterFun = opt$mz_center_fun,
  integrate = opt$integrate,
  mzdiff = opt$mzdiff,
  fitgauss = opt$fitgauss,
  noise = opt$noise,
  firstBaselineCheck = opt$first_baseline_check,
)

# Find peaks using the CentWave algorithm
XCMSExperiment <- findChromPeaks(
  object = msexperiment,
  param = CentWaveParams,
  msLevel = opt$ms_level,
  BPPARAM = MulticoreParam(workers = opt$threads)
)

# Export the XCMSExperiment object to the directory format
saveMsObject(XCMSExperiment, param = PlainTextParam(path = opt$output_path))
