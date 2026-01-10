import os
import pathlib
from PySide6.QtWidgets import QApplication

from src.components.MainWindow import MainWindow

class App(QApplication):

    main_window: MainWindow | None = None

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        os.environ["SHADER_PATH"] = str(pathlib.Path.joinpath(
            pathlib.Path(__file__).parent.resolve(),
            "../examples"
        ))

        self.main_window = MainWindow()
        self.main_window.show()