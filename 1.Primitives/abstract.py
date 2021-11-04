import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(720, 600, "Cores", None, None)
glfw.make_context_current(window)

def key_event(window,key,scancode,action,mods):
    print('[key event] key=',key)
    print('[key event] scancode=',scancode)
    print('[key event] action=',action)
    print('[key event] mods=',mods)
    print('-------')

def mouse_event(window,button,action,mods):
    print('[mouse event] button=',button)
    print('[mouse event] action=',action)
    print('[mouse event] mods=',mods)
    print('-------')
glfw.set_mouse_button_callback(window,mouse_event)

def setupGL():
    vertex_code = """
            attribute vec2 position;
            void main(){
                gl_Position = vec4(position,0.0,1.0);
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
    return program

# Setup vertex and shaders
program = setupGL()


# preparando espaço para 3 vértices usando 2 coordenadas (x,y)
num_simples = 36
num_circle_vertices = 50
vertices = np.zeros(num_simples + num_circle_vertices, [("position", np.float32, 2)])
vertices_aux = np.zeros(num_simples, [("position", np.float32, 2)])
# preenchendo as coordenadas de cada vértice
vertices_aux['position'] = [
                            #star
                            #1
                            (0.1,0.1),
                            (-0.1,0.1),
                            (-0.1,-0.1),
                            #2
                            (0.1,-0.1),
                            (-0.1,-0.1),
                            (0.1,0.1),
                            #3
                            (0.1,0.1),
                            (-0.1,0.1),
                            (0,0.4),
                            #4
                            (0.1,-0.1),
                            (-0.1,-0.1),
                            (0,-0.4),
                            #5
                            (0.1,0.1),
                            (0.1,-0.1),
                            (0.4,0),
                            #6
                            (-0.1,0.1),
                            (-0.1,-0.1),
                            (-0.4,0),
                            
                            #square
                            #1
                            (0.4,0.6),
                            (0.4,0.4),
                            (0.6,0.4),
                            #2
                            (0.6,0.4),
                            (0.6,0.6),
                            (0.4,0.6),
                            
                            #rectangle
                            #1
                            (0.9,0.6),
                            (0.6, 0.9),
                            (-0.6, -0.9),
                            #2
                            (-0.6, -0.9),
                            (0.6, 0.9),
                            (-0.9, -0.6),
                            
                            #square
                            #1
                            (-0.4,-0.6),
                            (-0.4,-0.4),
                            (-0.6,-0.4),
                            #2
                            (-0.6,-0.4),
                            (-0.6,-0.6),
                            (-0.4,-0.6),
                            
                        ]

vertices[:num_simples] = vertices_aux


radius = 0.4
pi = 3.1415

import math
angle = 0.0

for i in range(num_circle_vertices):
    x = math.cos(angle)*radius
    y = math.sin(angle)*radius
    vertices[i+num_simples] = [x,y]
    angle += 2*pi/num_circle_vertices

# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
# --------------------------------------
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, "color")
R = 1.0
G = 0.0
B = 0.0

glfw.show_window(window)

while not glfw.window_should_close(window):

    glfw.poll_events() 

    # R,G,B = random.randint(0, 1), random.randint(0, 1),random.randint(0, 1)
    
    print(vertices)
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    #circle
    glUniform4f(loc_color, 0.0, 1.0, 1.0, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLE_FAN, num_simples, num_circle_vertices)  
    
    #rectangle
    glUniform4f(loc_color, 0.0, 0.0, 1.0, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLES, 24, 6)  
    
    #star
    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLES, 0, 18)    
    
    #square1
    glUniform4f(loc_color, 0.0, 1.0, 0.0, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLES, 18, 6)
    
    #square2
    glUniform4f(loc_color, 0.0, 1.0, 0.0, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLES, 30, 6)
    
    
    glfw.swap_buffers(window)

glfw.terminate()