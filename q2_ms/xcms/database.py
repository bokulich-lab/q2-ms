import os

import requests

from q2_ms.types import MSPDirFmt


def fetch_massbank(release: str = None) -> MSPDirFmt:
    """
    Downloads the MassBank_NIST.msp file from the specified release of the
    MassBank-data repository.

    Parameters:
        release (str): The release version to download (e.g., '2024.11'). If None,
        downloads the latest release.
    """
    massbank = MSPDirFmt()
    base_url = "https://github.com/MassBank/MassBank-data/releases"

    if release:
        # Download from the specified release
        download_url = f"{base_url}/download/{release}/MassBank_NIST.msp"
    else:
        # Download from the latest release
        download_url = f"{base_url}/latest/download/MassBank_NIST.msp"

    response = requests.get(download_url)

    if response.status_code == 200:
        with open(os.path.join(str(massbank), "MassBank_NIST.msp"), "wb") as file:
            file.write(response.content)
    else:
        raise ValueError(f"Failed to download file. Code: {response.status_code}")

    return massbank
