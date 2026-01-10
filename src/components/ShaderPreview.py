import time

from OpenGL.GL import *

from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from src.graphics.Canvas import Canvas
from src.graphics.CanvasShader import CanvasShader

class ShaderPreview(QOpenGLWidget):

    compileFailed: Signal = Signal(str, name="error_message")

    canvas: Canvas | None = None
    shader: CanvasShader | None = None
    needs_update: bool = False
    fragment_source: str = ""

    frame_number: int = 0
    time_elapsed: float = 0.0
    last_frame_time: float = 0.0
    mouse: list[float] = [0.0, 0.0]
    resolution: list[float] = [0.0, 0.0]

    def __init__(self, fragment_source: str, parent: QWidget = None):
        super().__init__(parent)
        self.fragment_source = fragment_source

    def mouseMoveEvent(self, event: QMouseEvent):
        position = event.position()
        self.mouse = [float(position.x()), float(position.y())]

    def initializeGL(self):
        super().initializeGL()
        self.canvas = Canvas()
        self.shader = CanvasShader(self.fragment_source)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        self.resolution = [float(w), float(h)]
        glViewport(0, 0, w, h)

    def paintGL(self): 
        if self.needs_update:
            try: self.shader = CanvasShader(self.fragment_source)
            except RuntimeError as error: self.compileFailed.emit(str(error))
            self.needs_update = False

        if self.last_frame_time == 0.0:
            self.last_frame_time = time.time()
            frame_time: float = 0.0
        else:
            current_time = time.time()
            frame_time = current_time - self.last_frame_time
            self.time_elapsed += frame_time
            self.last_frame_time = current_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.shader.bind()

        self.shader.setFrame(self.frame_number)
        self.shader.setTime(self.time_elapsed)
        self.shader.setTimeDelta(frame_time)
        self.shader.setMouse(self.mouse)
        self.shader.setResolution(self.resolution)

        self.canvas.draw()
        self.shader.release()

        self.frame_number += 1
        
        self.update()

    def updateShader(self, fragment_source: str):
        self.fragment_source = fragment_source
        self.needs_update = True