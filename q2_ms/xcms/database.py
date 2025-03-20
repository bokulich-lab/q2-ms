# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import requests

from q2_ms.types import MSPDirFmt


def fetch_massbank() -> MSPDirFmt:
    """
    Downloads the MassBank_NIST.msp file from the latest release of the MassBank-data
    GitHub repository.
    """
    massbank = MSPDirFmt()

    response = requests.get(
        "https://github.com/MassBank/MassBank-data/releases/latest/download"
        "/MassBank_NIST.msp"
    )

    if response.status_code == 200:
        with open(os.path.join(str(massbank), "MassBank_NIST.msp"), "wb") as file:
            file.write(response.content)
    else:
        raise ValueError(f"Failed to download file. Code: {response.status_code}")

    return massbank
