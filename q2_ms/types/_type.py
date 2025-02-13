# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.core.type import SemanticType

mzML = SemanticType("mzML", variant_of=SampleData.field["type"])
XCMSExperiment = SemanticType("XCMSExperiment")
