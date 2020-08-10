from subprocess import run
from pathlib import Path
from shutil import rmtree, copy, copytree
from sys import platform
from os import environ, makedirs
from shutil import make_archive
from argparse import ArgumentParser


# Either import or define the application name
from main import __title__
# __title__ = ""

# Either import or define the version string
from main import __version__
# __version = ""

main_file = "main.py"

gooey_path = Path("..", "Lib", "site-packages", "gooey")

arch = environ["PROCESSOR_ARCHITECTURE"]
final_dist_path = f"{__title__}_{platform}_{arch}_{__version__}"

data = {
    "codices",
    "configs",
}

nuitka_options = [
    "--standalone",  # No Python installation required; implies --recurse-all
    "--plugin-enable=numpy",  # Needed for Gooey
    "--mingw64",  # Needed on Windows
    # "--windows-disable-console",  # On Windows, disable the console (best with GUI)
    # "--show-progress",
    "--assume-yes-for-downloads",
    "--remove-output",  # Delete the build folder
    "--verbose",
]

pyinstaller_options = [
    f"--distpath={final_dist_path}",
    "--noconfirm",
    "--clean",
    "--onedir",
    f"--name={__title__}",
    "--hidden-import=pkg_resources.py2_warn",
    "--hidden-import=PyQt5.sip",
    "--windowed",
]


def main():
    parser = ArgumentParser()
    parser.add_argument("utility", choices=("nuitka", "pyinstaller"))
    args = parser.parse_args()

    # Remove the previous build
    rmtree(final_dist_path, ignore_errors=True)

    if args.utility == "pyinstaller":
        # Build using PyInstaller
        run(["pyinstaller", *pyinstaller_options, main_file])

        # Copy the data folders
        for folder in data:
            copytree(Path(folder), Path(final_dist_path, __title__, folder))

    elif args.utility == "nuitka":
        # Determine default output directory
        default_dist_path = Path(f"{main_file.replace('.py', '')}.dist")

        # Build using Nuitka
        run(["python", "-m", "nuitka",  *nuitka_options, main_file]).check_returncode()

        # Rename the main executable to the application title
        Path(default_dist_path, main_file.replace('.py', '.exe')).rename(
            Path(default_dist_path, f"{__title__}.exe"))

        # Rename the output folder to the full build title
        Path(default_dist_path).rename(final_dist_path)

        # Create Gooey's stuff
        makedirs(Path(f"{final_dist_path}", "gooey"))
        copy(
            gooey_path,
            Path(f"{final_dist_path}", "gooey"),
        )

        # Copy the data folders
        for folder in data:
            copytree(Path(folder), Path(final_dist_path, folder))

    # Create ZIP archive
    make_archive(f"{final_dist_path}.zip", "zip", final_dist_path)


if __name__ == "__main__":
    main()
