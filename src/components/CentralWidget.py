import os
import pathlib

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout

from src.components.ShaderPreview import ShaderPreview

class CentralWidget(QWidget):

    console: QPlainTextEdit | None = None
    text_edit: QPlainTextEdit | None = None
    compile_button: QPushButton | None = None
    shader_preview: ShaderPreview | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        frag_path = pathlib.Path.joinpath(pathlib.Path(os.environ["SHADER_PATH"]), "UV.frag")
        with open(frag_path, "r") as frag_shader: frag_source = frag_shader.read()

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.document().setPlainText("Messages from the app:\n")

        self.text_edit = QPlainTextEdit()
        self.text_edit.document().setPlainText(frag_source)

        self.compile_button = QPushButton()
        self.compile_button.setText("Compile Shader")
        self.compile_button.pressed.connect(self.updateShader)

        self.shader_preview = ShaderPreview(self.text_edit.document().toPlainText())
        self.shader_preview.compileFailed.connect(self.onError)

        text_layout: QVBoxLayout = QVBoxLayout()
        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(self.compile_button)

        preview_layout: QHBoxLayout = QHBoxLayout()
        preview_layout.addLayout(text_layout, 1)
        preview_layout.addWidget(self.shader_preview, 1)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addLayout(preview_layout, 3)
        main_layout.addWidget(self.console, 1)

        self.setLayout(main_layout)

    def updateShader(self):
        self.shader_preview.updateShader(self.text_edit.document().toPlainText())

    def onError(self, error_message: str):
        self.console.setPlainText(self.console.document().toPlainText() + error_message)