import pathlib

from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QFileDialog

from src.components.central_widget import CentralWidget

ASSET_PATH = pathlib.Path.absolute(pathlib.Path.joinpath(
    pathlib.Path(__file__).parent.resolve(), "../../assets"
))

ICO_SAVE_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_save.png")
ICO_LOAD_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_load.png")
ICO_EXIT_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_exit.png")

class MainWindow(QMainWindow):
    """
    Applications main window, that holds
    all of its components.
    """

    central_widget: CentralWidget | None = None

    def __init__(self):
        """
        Initializes a MainWindow object by
        creating a central widget and a main
        application taskbar.
        """

        super().__init__()

        self.central_widget = CentralWidget(self)

        save_action: QAction = QAction(QIcon(str(ICO_SAVE_PATH)), "Save", self)
        save_action.setStatusTip("Save Shader")
        save_action.triggered.connect(self.save_file)

        load_action: QAction = QAction(QIcon(str(ICO_LOAD_PATH)), "Load", self)
        load_action.setStatusTip("Load Shader")
        load_action.triggered.connect(self.load_file)

        exit_action: QAction = QAction(QIcon(str(ICO_EXIT_PATH)), "Exit", self)
        exit_action.setStatusTip("Exit Application")
        exit_action.triggered.connect(self.exit)

        toolbar: QToolBar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.addAction(save_action)
        toolbar.addAction(load_action)
        toolbar.addAction(exit_action)

        self.setMinimumSize(800, 600)
        self.setWindowTitle("Shader Preview")
        self.setCentralWidget(self.central_widget)
        self.addToolBar(toolbar)

    def save_file(self):
        """
        Opens a file dialog and saves the contents
        of the main widget's text edit. If no output
        file is supplied the method takes an early
        exit.
        """
        filepath, check = QFileDialog.getSaveFileName(
            None, "Save Shader", "", self.tr("Supported Files (*.frag);;")
        )
        if not check:
            return
        with open(filepath, "w", encoding="UTF-8") as file:
            file.write(self.central_widget.text_edit.document().toPlainText())


    def load_file(self):
        """
        Opens a file dialog and loads the contents
        of the supplied file to the main widget's 
        tex edit. If no input file is supplied the
        method takes an early exit.
        """
        filepath, check = QFileDialog.getOpenFileName(
            None, "Load Shader", "", self.tr("Supported Files (*.frag);;")
        )
        if not check:
            return
        with open(filepath, "r", encoding="UTF-8") as file:
            self.central_widget.text_edit.setPlainText(file.read())

    def exit(self):
        """
        Closes the application
        """
        QApplication.quit()
