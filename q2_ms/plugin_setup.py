# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin

from q2_ms import __version__
from q2_ms.types import mzML, mzMLDirFmt, mzMLFormat

citations = Citations.load("citations.bib", package="q2_ms")

plugin = Plugin(
    name="ms",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-ms",
    package="q2_ms",
    description="A qiime2 plugin for MS data processing.",
    short_description="A qiime2 plugin for MS data processing.",
)

# Registrations
plugin.register_semantic_types(
    mzML,
)

plugin.register_semantic_type_to_format(mzML, artifact_format=mzMLDirFmt)

plugin.register_formats(
    mzMLFormat,
    mzMLDirFmt,
)
