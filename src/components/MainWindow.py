import pathlib

from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QFileDialog

from src.components.CentralWidget import CentralWidget

ASSET_PATH = pathlib.Path.absolute(pathlib.Path.joinpath(
    pathlib.Path(__file__).parent.resolve(), "../../assets"
))

ICO_SAVE_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_save.png")
ICO_LOAD_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_load.png")
ICO_EXIT_PATH = pathlib.Path.joinpath(ASSET_PATH, "ico_exit.png")

class MainWindow(QMainWindow):

    central_widget: CentralWidget | None = None

    def __init__(self):
        super().__init__()

        self.central_widget = CentralWidget(self)

        save_action: QAction = QAction(QIcon(str(ICO_SAVE_PATH)), "Save", self)
        save_action.setStatusTip("Save Shader")
        save_action.triggered.connect(self.saveFile)

        load_action: QAction = QAction(QIcon(str(ICO_LOAD_PATH)), "Load", self)
        load_action.setStatusTip("Load Shader")
        load_action.triggered.connect(self.loadFile)

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

    def saveFile(self):
        filepath, check = QFileDialog.getSaveFileName(
            None, "Save Shader", "", self.tr("Supported Files (*.frag);;")
        )
        if not check: return
        with open(filepath, "w") as file: 
            file.write(self.central_widget.text_edit.document().toPlainText())


    def loadFile(self):
        filepath, check = QFileDialog.getOpenFileName(
            None, "Load Shader", "", self.tr("Supported Files (*.frag);;")
        )
        if not check: return
        with open(filepath, "r") as file:
            self.central_widget.text_edit.setPlainText(file.read())

    def exit(self): QApplication.quit()