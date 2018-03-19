#! /usr/bin/env python3

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

numpy.random.seed(0)

def fractal(a, b, c, rem=8):

    if rem < 0:
        return None
    elif rem == 0:
        glBegin(GL_LINES)

        glVertex3dv(b)
        glVertex3dv(c)
    
        glVertex3dv(c)
        glVertex3dv(a)
    
        glVertex3dv(a)
        glVertex3dv(b)

        glEnd()
    else:
        dd, de, df = ((numpy.random.rand(3) - 0.5) * 0.0015 * 2.**rem for i in range(3))

        fractal(a, (a + b) / 2. + df, (a + c) / 2. + de, rem=rem-1)
        fractal((b + a) / 2. + df, b, (b + c) / 2. + dd, rem=rem-1)
        fractal((c + a) / 2. + de, (c + b) / 2. + dd, c, rem=rem-1)

def display():
    
    glClear(GL_COLOR_BUFFER_BIT)

    a, b, c = numpy.array([-0.7, -0.6, 0.0]), numpy.array([0.7, -0.6, 0.0]), numpy.array([0.0, 0.8, 0.0])
    
    fractal(a, b, c)

    glutSwapBuffers()

def redraw(w, h):
    
    glutPostRedisplay()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)

glutInitWindowSize(800, 800)

glutCreateWindow("Python Fractal Mountain")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
