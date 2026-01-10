import os
import pathlib

from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram

class CanvasShader(QOpenGLShaderProgram):

    frame_uniform: int      = 0
    time_uniform: int       = 0
    time_delta_uniform: int = 0
    mouse_uniform: int      = 0
    resolution_uniform: int = 0

    def __init__(self, fragment_source: str):
        super().__init__()
        
        if not self.addShaderFromSourceFile(
            QOpenGLShader.ShaderTypeBit.Vertex,
            str(pathlib.Path.joinpath(pathlib.Path(os.environ["SHADER_PATH"]), "passthrough.vert"))
        ): raise RuntimeError(self.log())

        if not self.addShaderFromSourceCode(
            QOpenGLShader.ShaderTypeBit.Fragment,
            fragment_source
        ): raise RuntimeError(self.log())

        if not self.link(): raise RuntimeError(self.log())

        self.frame_uniform      = self.uniformLocation("u_frame")
        self.time_uniform       = self.uniformLocation("u_time")
        self.time_delta_uniform = self.uniformLocation("u_time_delta")
        self.mouse_uniform      = self.uniformLocation("u_mouse")
        self.resolution_uniform = self.uniformLocation("u_resolution")

    def setFrame(self, frame: int): self.setUniformValue1i(self.frame_uniform, frame)
    def setTime(self, time: float): self.setUniformValue1f(self.time_uniform, time)
    def setTimeDelta(self, time_delta: float): self.setUniformValue1f(self.time_delta_uniform, time_delta)
    def setMouse(self, mouse: list[float]): self.setUniformValueArray(self.mouse_uniform, mouse, 1, 2)
    def setResolution(self, resolution: list[float]): self.setUniformValueArray(self.resolution_uniform, resolution, 1, 2)