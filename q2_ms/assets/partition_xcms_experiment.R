#!/usr/bin/env Rscript

library(jsonlite)
library(xcms)
library(Spectra)
library(MsExperiment)
library(MsIO)
library(optparse)

option_list <- list(
  make_option("--xcms_experiment", type = "character"),
  make_option("--output_paths", type = "character"),
  make_option("--partition_indices", type = "character"),
  make_option("--fake_spectra", type = "character")
)
opt <- parse_args(OptionParser(option_list = option_list))

# Parse index partitions and output paths
partition_indices <- fromJSON(opt$partition_indices, simplifyVector = FALSE)

output_paths <- fromJSON(opt$output_paths)

# Load the XCMSExperiment or MsExperiment
XCMSExperiment <- tryCatch({
    readMsObject(XcmsExperiment(), PlainTextParam(opt$xcms_experiment), spectraPath=opt$fake_spectra)
}, error = function(e) {
    readMsObject(MsExperiment(), PlainTextParam(opt$xcms_experiment), spectraPath=opt$fake_spectra)
})

# Loop over partitions
for (i in seq_along(partition_indices)) {
  idx <- as.integer(partition_indices[[i]]) + 1  # R is 1-based
  subset_xset <- XCMSExperiment[idx]
  saveMsObject(subset_xset, PlainTextParam(output_paths[[i]]))
}
