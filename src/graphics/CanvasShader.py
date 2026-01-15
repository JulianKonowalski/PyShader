import pathlib

from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram

VERT_SOURCE: str = """
#version 330 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 tex_coord;

uniform int     u_frame;
uniform float   u_time;
uniform float   u_time_delta;
uniform vec2    u_mouse;
uniform vec2    u_resolution;

out int     i_frame;
out float   i_time;
out float   i_time_delta;
out vec2    i_mouse;
out vec2    i_resolution;
out vec3    i_normal;
out vec3    i_position;
out vec2    i_tex_coord;

void main() {
    gl_Position = vec4(pos, 1.0);

    i_frame         = u_frame;
    i_time          = u_time;
    i_time_delta    = u_time_delta;
    i_mouse         = u_mouse;
    i_resolution    = u_resolution;
    i_position      = gl_Position.xyz;
    i_normal        = normal;
    i_tex_coord     = tex_coord;
}
"""

class CanvasShader(QOpenGLShaderProgram):
    """
    A class representing the shader program.
    It can be altered and recompiled at any
    time by updating its uniform variables or
    supplying new source code.
    """

    # locations of shader uniform variables
    frame_uniform: int      = 0
    time_uniform: int       = 0
    time_delta_uniform: int = 0
    mouse_uniform: int      = 0
    resolution_uniform: int = 0

    def __init__(self, fragment_source: str):
        """
        Initializes a CanvasShader object by
        loading a default vertex shader and 
        combining it with the supplied fragment 
        shader source code.

        :param fragment_source: source code of the fragment shader
        :type fragment_source: str
        """
        super().__init__()

        if not self.addShaderFromSourceCode(
            QOpenGLShader.ShaderTypeBit.Vertex,
            VERT_SOURCE
        ): raise RuntimeError(self.log())

        # if not self.addShaderFromSourceFile(
        #     QOpenGLShader.ShaderTypeBit.Vertex,
        #     str(pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "passthrough.vert"))
        # ): raise RuntimeError(self.log())

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

    def setFrame(self, frame: int):
        """
        Sets the value of the uniform variable
        that stores the current frame number.

        :param frame: current frame number
        :type frame: int
        """
        self.setUniformValue1i(self.frame_uniform, frame)

    def setTime(self, time: float):
        """
        Sets the value of the uniform variable
        that stores the current time.
        
        :param time: current time in seconds
        :type time: float
        """
        self.setUniformValue1f(self.time_uniform, time)

    def setTimeDelta(self, time_delta: float):
        """
        Sets the value of the uniform variable
        that stores the last frame generation time.
        
        :param time_delta: frame generation time in seconds
        :type time_delta: float
        """
        self.setUniformValue1f(self.time_delta_uniform, time_delta)

    def setMouse(self, mouse: list[float]):
        """
        Sets the value of the uniform variable
        that stores the mouse position.
        
        :param mouse: mouse position in screen coordinates [0-max_screen_width, 0-max_screen_height]
        :type mouse: list[float]
        """
        self.setUniformValueArray(self.mouse_uniform, mouse, 1, 2)

    def setResolution(self, resolution: list[float]):
        """
        Sets the value of the uniform variable
        that stores the screen resolution.
        
        :param resolution: screen resolution in pixels [screen_width, screen_height]
        :type resolution: list[float]
        """
        self.setUniformValueArray(self.resolution_uniform, resolution, 1, 2)