#! /usr/bin/env python3

import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy

x = numpy.array([0., 0., 1.])

n = 3
m = [
    numpy.array([
        [0.5, 0., 0.],
        [0., 0.5, -0.4],
        [0., 0., 1.],
    ]),
    numpy.array([
        [0.5, 0., -0.4],
        [0., 0.5, 0.4],
        [0., 0.0, 1.],
    ]),
    numpy.array([
        [0.5, 0., 0.4],
        [0., 0.5, 0.4],
        [0., 0., 1.],
    ]),
]
p = [1. / 3. for i in range(3)]

def repeat_ifs(l=100, s=0.01):

    global x

    ind = numpy.random.choice(n, l, p=p)

    for i in ind:
        glVertex2dv(x[:2])
        x = m[i].dot(x)
    
    time.sleep(s)

def display():

    glBegin(GL_POINTS)
    repeat_ifs()
    glEnd()

    glutSwapBuffers()

    glutPostRedisplay()

def redraw(w, h):
    
    glClear(GL_COLOR_BUFFER_BIT)

    glutPostRedisplay()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE)

glutInitWindowSize(800, 800)

glutCreateWindow("Python ISF Sierpinski")

glClear(GL_COLOR_BUFFER_BIT)

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
