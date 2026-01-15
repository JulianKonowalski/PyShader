import numpy
import ctypes

import OpenGL.GL as gl

class Canvas:
    """
    A rectangular plane that spans from
    [-1.0, -1.0] to [1.0, 1.0] and is 
    projected straight onto the screen.
    """

    # GPU buffers and helper variables
    # related to creating and rendering 
    # the plane
    vao: numpy.int32 = 0
    vbo: numpy.int32 = 0
    ebo: numpy.int32 = 0
    num_indices: numpy.int32 = 0
    num_vertices: numpy.int32 = 0
    
    def __init__(self):
        """
        Initializes a Canvas object by
        creating the plane geometry on
        the GPU.
        """
        vertices = numpy.array([
            # position          # normal            # tex coord
            -1.0, -1.0, 0.0,    0.0, 0.0, -1.0,     0.0, 0.0,
             1.0, -1.0, 0.0,    0.0, 0.0, -1.0,     1.0, 0.0,
             1.0,  1.0, 0.0,    0.0, 0.0, -1.0,     1.0, 1.0,
            -1.0,  1.0, 0.0,    0.0, 0.0, -1.0,     0.0, 1.0
        ], dtype=numpy.float32)

        indices = numpy.array([
            0, 1, 2,
            0, 2, 3
        ], dtype=numpy.uint32)

        self.num_indices = len(indices)
        self.num_vertices = len(vertices)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        
        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        self.ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)

        stride: numpy.uint32 = 8 * ctypes.sizeof(ctypes.c_float)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(0))

        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def draw(self) -> None:
        """
        Binds the internal plane geometry
        and issues a draw call to the GPU.
        """
        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glDrawElements(gl.GL_TRIANGLES, self.num_indices, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)