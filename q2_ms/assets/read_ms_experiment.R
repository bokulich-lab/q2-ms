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

# Get full paths to spectra files and read them into an MsExperiment object
mzmlFiles <- list.files(opt$spectra, full.names = TRUE)

# Create sample metadata data frame
sampleData <- read.table(file = opt$sample_metadata, header = TRUE, sep = "\t")

# Read the mzML files and sample data into an MsExperiment object
MsExperiment <- readMsExperiment(spectraFiles = mzmlFiles, sampleData = sampleData)

# Export the MsExperiment object to the directory format
saveMsObject(MsExperiment, param = PlainTextParam(path = opt$output_path))
