import os
import shutil
import pathlib
import subprocess

APP_NAME: str = "PyShader"
ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.joinpath("..").resolve()

# ------------------------------------------------------------------------------------------------ #

def preprocessMain():
    with open(ROOT_DIR.joinpath("src").joinpath("main.py").resolve(), "r") as main_file:
        main_contents: list[str] = main_file.readlines()

    for index, line in enumerate(main_contents):
        if not line.startswith("os.chdir"): continue
        main_contents[index] = f"os.chdir(\"{str(ROOT_DIR).replace("\\", "/")}\")\n"

    with open(ROOT_DIR.joinpath("src").joinpath(f"{APP_NAME}.py").resolve(), "w") as tmp_main_file:
        tmp_main_file.writelines(main_contents)

# ------------------------------------------------------------------------------------------------ #

def build():
    os.chdir(ROOT_DIR)
    subprocess.run(["pyinstaller", f"src/{APP_NAME}.py", "--noconfirm", "--onefile", "--windowed"])

# ------------------------------------------------------------------------------------------------ #

def copyAssets():
    src_asset_dir: pathlib.Path = ROOT_DIR.joinpath("assets").resolve()
    dest_asset_dir: pathlib.Path = ROOT_DIR.joinpath("dist").joinpath("assets").resolve()
    os.mkdir(str(dest_asset_dir))
    for filename in os.listdir(str(src_asset_dir)):
        shutil.copy(
            str(src_asset_dir.joinpath(filename).resolve()),
            str(dest_asset_dir.joinpath(filename).resolve())
        )

# ------------------------------------------------------------------------------------------------ #

def cleanup():
    os.remove(str(ROOT_DIR.joinpath("src").joinpath(f"{APP_NAME}.py")))

# ------------------------------------------------------------------------------------------------ #

if __name__ == "__main__":
    preprocessMain()
    build()
    copyAssets()
    cleanup()

# ------------------------------------------------------------------------------------------------ #