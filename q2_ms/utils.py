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


def run_r_script(params, script_name, package_name):
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
