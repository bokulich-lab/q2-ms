# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess

EXTERNAL_CMD_WARNING = (
    "Running external command line application(s). "
    "This may print messages to stdout and/or stderr.\n"
    "The command(s) being run are below. These commands "
    "cannot be manually re-run as they will depend on "
    "temporary files that no longer exist."
)


def run_command(cmd, cwd, verbose=True, env=None):
    if verbose:
        print(EXTERNAL_CMD_WARNING)
        print("\nCommand:", end=" ")
        print(" ".join(cmd), end="\n\n")
    subprocess.run(cmd, check=True, cwd=cwd, env=env)


def run_r_script(script_name, params, package_name):
    """
    Constructs a command-line call to an R script with parameters passed as
    command-line flags and executes it.

    Parameters:
        params (dict):
            A dictionary of parameter names and values to be passed as
            command-line arguments to the R script.
        script_name (str):
            The base name of the R script. The script is assumed to be located at
            q2_ms/assets and registered in pyproject.toml.
        package_name (str):
            The name of the R package being invoked, used for error messaging.

    Raises:
        Exception:
            If the R script returns a non-zero exit status, an Exception is raised
            with the relevant package name and return code.
    """
    cmd = [f"{script_name}.R"]

    for key, value in params.items():
        if value is not None:
            cmd.extend([f"--{key}", str(value)])

    try:
        run_command(cmd, verbose=True, cwd=None)
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"An error was encountered while running {package_name}, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )
