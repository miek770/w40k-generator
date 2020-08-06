from pathlib import Path
from shutil import rmtree, copytree
import PyInstaller.__main__


def main():
    try:
        rmtree(Path("dist"))
    except FileNotFoundError:
        pass
    PyInstaller.__main__.run([
        "main.spec",
    ])
    for folder in ("codices", "configs"):
        copytree(Path(folder), Path("dist", folder))


if __name__ == "__main__":
    main()
