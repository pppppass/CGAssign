#! /usr/bin/env python3

import math
from time import time

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

last = time()

gravity = numpy.array([0.0, -1.0, 0.0])
velocity = numpy.array([0.7, 0.3, 0.0])
position = numpy.array([0.2, 0.0, 0.0])

width = 0.7
height = 0.7
radius = 0.1

sides = 50

equations = numpy.array([
    [1.0, 0.0, 0.0, width],
    [0.0, 1.0, 0.0, height],
    [-1.0, 0.0, 0.0, width],
])

def display():

    global last
    
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    glTranslated(*position)
    glScaled(*(radius * numpy.ones(3)))
    
    glCallList(1)

    glPopMatrix()

    glCallList(2)

    now = time()
    interval = now - last
    update(interval)
    last = now

    glutSwapBuffers()

    glutPostRedisplay()

def redraw(w, h):
    
    glutPostRedisplay()

def initialize():

    glEnable(GL_BLEND)
    
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    glLineWidth(2.5)
    glPointSize(2.5)

def make():

    glNewList(1, GL_COMPILE)

    glBegin(GL_POLYGON)
    glColor3d(1.0, 1.0, 1.0)
    for i in range(sides):
        glVertex2d(math.cos(2.0 * math.pi * i / sides), math.sin(2.0 * math.pi * i / sides))
    glEnd()

    glEndList()

    glNewList(2, GL_COMPILE)

    glBegin(GL_LINES)
    glColor3d(1.0, 1.0, 1.0)
    glVertex2d(-width, height)
    glVertex2d(-width, -height)
    glVertex2d(-width, -height)
    glVertex2d(width, -height)
    glVertex2d(width, -height)
    glVertex2d(width, height)
    glEnd()

    glEndList()

def update(interval):
    
    global position, velocity

    reflect()

    position += velocity * interval + gravity * interval**2 / 2
    velocity += gravity * interval

def reflect():

    global position, velocity

    for e in equations:
        if e[:3].dot(position) + e[3] - radius < 0.0 and e[:3].dot(velocity) < 0.0:
            velocity = velocity - 2.0 * e[:3] * (e[:3].dot(velocity))
    
glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

glutInitWindowSize(800, 800)

glutCreateWindow("Python Bouncing Ball")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

initialize()

make()

glutMainLoop()
