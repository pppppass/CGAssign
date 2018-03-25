#! /usr/bin/env python3

import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy

x = numpy.array([0., 0., 1.])

n = 4
m = [
    numpy.array([
        [0., 0., 0.],
        [0., 0.16, 0.],
        [0., 0., 1.],
    ]),
    numpy.array([
        [0.85, 0.04, 0.],
        [-0.04, 0.85, 1.6],
        [0., 0., 1.]
    ]),
    numpy.array([
        [0.2, -0.26, 0.],
        [0.23, 0.22, 1.6],
        [0., 0., 1.],
    ]),
    numpy.array([
        [-0.15, 0.28, 0.],
        [0.26, 0.24, 0.44],
        [0., 0., 1.],
    ]),
]
p = [0.01, 0.85, 0.07, 0.07]

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

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslated(0., -1., 0.)
glScaled(0.2, 0.2, 0.2)

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
