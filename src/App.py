import os
import pathlib
from PySide6.QtWidgets import QApplication

from src.components.MainWindow import MainWindow

class App(QApplication):
    """
    Qt application class that creates
    the main window and runs the app
    event loop.
    """

    main_window: MainWindow | None = None

    def __init__(self, argv: list[str]) -> None:
        """
        Docstring for __init__
        
        :param argv: arguments passed to main during the script invokation
        :type argv: list[str]
        """

        super().__init__(argv)
        os.environ["SHADER_PATH"] = os.path.join(os.getcwd(), "examples")

        self.main_window = MainWindow()
        self.main_window.show()