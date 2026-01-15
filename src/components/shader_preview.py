import time

import OpenGL.GL as gl

from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from src.graphics.canvas import Canvas
from src.graphics.canvas_shader import CanvasShader

class ShaderPreview(QOpenGLWidget):
    """
    A shader preview widget that holds the 
    OpenGL context and renders the shader 
    output. It automatically handles events 
    crucial to correct rendering (window 
    resizing and mouse events), as well as 
    updating the shader uniform variables 
    each frame.
    """

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
        """
        Initializes the shader preview by
        temporarily saving the fragment source 
        code.

        :param fragment_source: fragment shader source code
        :type fragment_source: str
        :param parent: parent widget
        :type parent: QWidget
        """
        super().__init__(parent)
        self.fragment_source = fragment_source

    # this is a method from Qt, please don't hang me for non-PEP8 naming convention
    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Handles a mouse move event. A mouse move
        gets called on press and drag.
        
        :param event: mouse move event
        :type event: QMouseEvent
        """
        position = event.position()
        self.mouse = [float(position.x()), float(position.y())]

    # also overriden method from Qt
    def initializeGL(self):
        """
        Initializes all of the OpenGL subcomponents, 
        such as the internal render plane and shader.
        It gets called by Qt when it decides to 
        initialize the opengl context.
        """
        super().initializeGL()
        self.canvas = Canvas()
        self.shader = CanvasShader(self.fragment_source)

    # also Qt
    def resizeGL(self, width: int, height: int):
        """
        Handles a components resize event.
        
        :param width: new component width
        :type width: int
        :param height: new component height
        :type height: int
        """
        super().resizeGL(width, height)
        self.resolution = [float(width), float(height)]
        gl.glViewport(0, 0, width, height)

    # Qqqqttttttt
    def paintGL(self):
        """
        Renders the shader output and requests
        next render pass from Qt. Additionally
        updates the shader if it need to be 
        updated. This method gets called automatically 
        by the Qt event loop.
        """
        if self.needs_update:
            try:
                self.shader = CanvasShader(self.fragment_source)
            except RuntimeError as error:
                self.compileFailed.emit(str(error))
            self.needs_update = False

        if self.last_frame_time == 0.0:
            self.last_frame_time = time.time()
            frame_time: float = 0.0
        else:
            current_time = time.time()
            frame_time = current_time - self.last_frame_time
            self.time_elapsed += frame_time
            self.last_frame_time = current_time

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

        self.shader.bind()

        self.shader.set_frame(self.frame_number)
        self.shader.set_time(self.time_elapsed)
        self.shader.set_time_delta(frame_time)
        self.shader.set_mouse(self.mouse)
        self.shader.set_resolution(self.resolution)

        self.canvas.draw()
        self.shader.release()

        self.frame_number += 1

        self.update()

    def update_shader(self, fragment_source: str):
        """
        Saves the supplied fragment source code
        and sets a flag to update the shader during
        the next render pass.
        
        :param fragment_source: fragment shader source code
        :type fragment_source: str
        """
        self.fragment_source = fragment_source
        self.needs_update = True
