import os
import sys
import pathlib
from src.App import App

os.chdir(str(pathlib.Path(__file__).parent.joinpath("..").resolve()))

if __name__ == "__main__":
    app = App(sys.argv)
    app.exec()