import subprocess
import time


def install_pip(pip_name: str) -> bool:
    """
    Installs or updates a module using pip and reports if an error occurred

    Returns True on success and False on failure

    :param pip_name: The name of the module as found on PyPI (the name you would use for `pip install {pip_name}`), "name==version"
    :type pip_name: str
            
    :return: If the install command succeeded
    :rtype: bool
    """

    print(f"Installing: {pip_name}\x1b]9;4;3\x07")

    if len(pip_name) == 0:

        print("Nothing specified to install\x1b]9;4;0\x07")
        return True

    proc = subprocess.Popen(
        f"pip install {pip_name} --upgrade --break-system-packages",
        stderr=subprocess.PIPE,
    )
    code = proc.wait()

    if code == 0:
        print(f"Done (code: {code})\x1b]9;4;0\x07")
        return True

    else:

        print(f"Install failed (code: {code})\x1b]9;4;0\x07")
        if proc.stderr is None:
            return False
        print(proc.stderr.read().decode("utf-8"))
        return False


def verify_exists(name: str, pip_name: str) -> None:
    """
    Verifies that a given module exists (can be imported)

    Also preloads the given module

    If the module doesn't exist, it will prompt stdin to install

    :param name: The name of the module (the name you would use for `import {name}`)
    :type name: str
    :param pip_name: The name of the module as found on PyPI (the name you would use for `pip install {pip_name}`), "name==version"
    :type pip_name: str

    .. code-block:: python3

        # Check for Pygame-CE

        verify_exists("pygame","pygame-ce")

    """

    try:

        __import__(name)

    except ModuleNotFoundError:

        if (
            input(
                f"Missing module {name} / {pip_name} (not installed)\nInstall now? (Y/N)\n"
            ).lower()
            == "y"
        ):

            install_pip(pip_name)

        else:

            print("Installation skipped (module will not work)")


def check_all(pip_names: list[str]) -> None:
    """
    Checks all given modules and allows a user to install them from stdin

    :param pip_names: The names of the modules as found on PyPI (the name you would use for `pip install {pip_name}`), "name==version"
    :type pip_names: list[str]
    """

    # Ensure at least 1 name specified
    if len(pip_names) == 0:
        print("No modules specified to check")
        return

    # Get packages by PIP
    proc = subprocess.Popen("pip freeze", stdout=subprocess.PIPE)

    # Make linter happy (this will never trigger btw)
    if proc.stdout is None:
        return

    # Get package list
    packages: list[str] = proc.stdout.read().decode("utf-8").splitlines()
    packages_n = [pkg.split("=")[0] for pkg in packages]
    packages_v = [pkg.split("=")[-1] for pkg in packages]

    # Check each
    pip_found = [name.split("=")[0] in packages_n for name in pip_names]
    pip_version_correct = [
        name.split("=")[-1] in packages_v or "=" not in name for name in pip_names
    ]

    # Find the largest length string
    if len(pip_names) == 1:
        max_len = len(pip_names[0])
    else:
        max_len = max(*[len(name) for name in pip_names])

    # Allow user to choose
    choices = [False]*len(pip_names)

    while True:

        # Print packages
        print(
            "\n".join(
                [
                    f"{'\x1b[35m' if choices[i] else ''}{i:<4} : {name.ljust(max_len)} \x1b[0m| {'\x1b[32mFound     ' if found else '\x1b[31mNot Found '}\x1b[0m|{'' if version else ' \x1b[33mWrong Version'}\x1b[0m"
                    for i, name, found, version in zip(
                        range(len(pip_names)), pip_names, pip_found, pip_version_correct
                    )
                ]
            )
        )

        print(
            "\nEnter the number of the package to install/update to toggle it\nPress enter with no number to begin installation"
        )
        chosen = input("\x1b[2K> ")

        if chosen == "":
            break

        if not chosen.isnumeric():
            print(f"Please enter a number within the range of [0-{len(pip_names)-1}]")
            time.sleep(1)
            print("\x1b[H\x1b[2J\x1b[3J", end="")
            continue

        chosen_i = int(chosen)

        if chosen_i < 0 or chosen_i >= len(pip_names):
            print(f"Please enter a number within the range of [0-{len(pip_names)-1}]")
            time.sleep(1)
            print("\x1b[H\x1b[2J\x1b[3J", end="")
            continue

        choices[chosen_i] = not choices[chosen_i]

        print("\x1b[H\x1b[2J\x1b[3J", end="")

    install_pip(" ".join(x for i,x in zip(choices,pip_names) if i))
