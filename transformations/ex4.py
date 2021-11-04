# Ex. 4 -  Computacao Grafica - 
# Ao final do programa a matriz de transformação será mostrada no terminal

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import vertices as vt

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(700, 700, "Cubo", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec3 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
        }
        """
        
fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

vertices = np.zeros(1728, [("position", np.float32, 3)])
vertices_aux = vt.getteapot().reshape(-1, 3)

vertices['position'] = vertices_aux


# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, "color")

glfw.show_window(window)

import math
d = 0.0
glEnable(GL_DEPTH_TEST) ### importante para 3D

from numpy import random


def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

def rotateZ(d, mat_transform):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    mat_rotation_z = np.array([     cos_d, -sin_d, 0.0, 0.0, 
                                    sin_d,  cos_d, 0.0, 0.0, 
                                    0.0,      0.0, 1.0, 0.0, 
                                    0.0,      0.0, 0.0, 1.0], np.float32)
    return multiplica_matriz(mat_rotation_z, mat_transform)

def rotateX(d, mat_transform):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    mat_rotation_x = np.array([     1.0,   0.0,    0.0, 0.0, 
                                    0.0, cos_d, -sin_d, 0.0, 
                                    0.0, sin_d,  cos_d, 0.0, 
                                    0.0,   0.0,    0.0, 1.0], np.float32)
    return multiplica_matriz(mat_rotation_x, mat_transform)

def rotateY(d, mat_transform):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    mat_rotation_y = np.array([     cos_d,  0.0, sin_d, 0.0, 
                                    0.0,    1.0,   0.0, 0.0, 
                                    -sin_d, 0.0, cos_d, 0.0, 
                                    0.0,    0.0,   0.0, 1.0], np.float32)
    
    return multiplica_matriz(mat_rotation_y, mat_transform)

import time
while not glfw.window_should_close(window):
    
    glfw.poll_events() 
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)

    mat_transform = np.array([0.3,0.0,0.0,0.0,
                              0.0,0.3,0.0,0.0,
                              0.0,0.0,0.3,0.0,
                              0.0,0.0,0.0,1])
    
    mat_transform = rotateX(3.14, mat_transform)
    mat_transform = rotateY(3.14/6, mat_transform)
    mat_transform = rotateX(-3.14/9, mat_transform)
    
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    # glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    for triangle in range(0,len(vertices),3):
    
        random.seed( triangle )
        R = random.random()
        G = random.random()
        B = random.random() 
    
        glUniform4f(loc_color, R, G, B, 1.0)
        
        glDrawArrays(GL_TRIANGLES, triangle, 3) 
    
    glfw.swap_buffers(window)

print(f"Mat_transform: {mat_transform}")
glfw.terminate()