# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

description = "Plugin template."

setup(
    name="q2-ms",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="QIIME 2 development team",
    author_email="rischv@ethz.ch",
    description=description,
    url="https://github.com/bokulich-lab/q2-ms",
    entry_points={"qiime2.plugins": ["q2_ms=q2_ms.plugin_setup:plugin"]},
    package_data={
        "q2_ms": ["citations.bib"],
        "q2_ms.tests": ["data/*"],
    },
    zip_safe=False,
)
