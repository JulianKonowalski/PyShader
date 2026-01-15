import os
import sys
import pathlib
from src.app import App

os.chdir("C:/Users/Julek/Desktop/Szkoła/3rok/python/shadertoy")

if __name__ == "__main__":
    app = App(sys.argv)
    app.exec()
