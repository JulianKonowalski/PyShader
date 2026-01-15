import os
import pathlib

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout

from src.components.shader_preview import ShaderPreview

class CentralWidget(QWidget):
    """
    Main application widget containing
    all of app components.
    """

    # all of the subcomponents
    console: QPlainTextEdit | None = None
    text_edit: QPlainTextEdit | None = None
    compile_button: QPushButton | None = None
    shader_preview: ShaderPreview | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialized a CentralWidget object by
        creating all of its subcomponents and
        connecting the required signals.
        
        :param parent: parent widget
        :type parent: QWidget | None
        """
        super().__init__(parent)

        frag_path = pathlib.Path.joinpath(pathlib.Path(os.environ["SHADER_PATH"]), "UV.frag")
        with open(frag_path, "r", encoding="UTF-8") as frag_shader:
            frag_source = frag_shader.read()

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.document().setPlainText("Messages from the app:\n")

        self.text_edit = QPlainTextEdit()
        self.text_edit.document().setPlainText(frag_source)

        self.compile_button = QPushButton()
        self.compile_button.setText("Compile Shader")
        self.compile_button.pressed.connect(self.update_shader)

        self.shader_preview = ShaderPreview(self.text_edit.document().toPlainText())
        self.shader_preview.compileFailed.connect(self.on_error)

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

    def update_shader(self):
        """
        Updates the currently displayed shader
        by reading the contents of the text edit
        and passing them to the shader as fragment
        source code.
        """
        self.shader_preview.update_shader(self.text_edit.document().toPlainText())

    def on_error(self, error_message: str):
        """
        Handles the error message by printing
        it to the console.

        :param error_message: error message to be printed
        :type error_message: str
        """
        self.console.setPlainText(self.console.document().toPlainText() + error_message)
