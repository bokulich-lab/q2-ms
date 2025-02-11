#!/usr/bin/env Rscript --vanilla

library(xcms)
library(MsExperiment)
library(MsIO)
library(jsonlite)
library(optparse)

# Define command-line options
option_list <- list(
  make_option(opt_str = "--spectra", type = "character"),
  make_option(opt_str = "--sample_metadata", type = "character"),
  make_option(opt_str = "--output_path", type = "character")
)

# Parse arguments
optParser <- OptionParser(option_list = option_list)
opt <- parse_args(optParser)

# Read in MsExperiment with or without sampleData
if (is.null(opt$sample_metadata)) {
  # Get paths to spectra files from directory
  spectraFiles <- list.files(opt$spectra, full.names = TRUE)
  MsExperiment <- readMsExperiment(spectraFiles = spectraFiles)

} else {
  # Get paths to spectra files from sample data
  sampleData <- read.table(file = opt$sample_metadata, header = TRUE, sep = "\t")
  spectraFiles <- file.path(opt$spectra, paste0(sampleData[[1]], ".mzML"))
  MsExperiment <- readMsExperiment(spectraFiles = spectraFiles, sampleData = sampleData)
}

# Export the MsExperiment object to the directory format
saveMsObject(MsExperiment, param = PlainTextParam(path = opt$output_path))
