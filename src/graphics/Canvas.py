import numpy
import ctypes

from OpenGL.GL import *

class Canvas:

    vao: numpy.int32 = 0 
    vbo: numpy.int32 = 0
    ebo: numpy.int32 = 0

    num_indices: numpy.int32 = 0
    num_vertices: numpy.int32 = 0
    
    def __init__(self):
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

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride: numpy.uint32 = 8 * ctypes.sizeof(ctypes.c_float)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)