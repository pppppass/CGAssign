#! /usr/bin/env python3

import math
from time import time

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

last = time()

n = 7

gravity = numpy.array([0.0, -1.0, 0.0])
velocity = numpy.array([
    [0.7, 0.3, 0.0],
    [0.5, 0.2, 0.0],
    [-0.2, 0.3, 0.0],
    [-0.5, 0.7, 0.0],
    [-0.6, 0.5, 0.0],
    [-0.5, 0.2, 0.0],
    [0.4, -0.8, 0.0],
])
position = numpy.array([
    [0.2, 0.0, 0.0],
    [-0.2, 0.4, 0.0],
    [0.5, 0.2, 0.0],
    [-0.4, 0.3, 0.0],
    [0.3, 0.6, 0.0],
    [-0.6, -0.3, 0.0],
    [0.5, -0.1, 0.0],
])
color = numpy.array([
    [1.0, 1.0, 1.0],
    [1.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
])
radius = numpy.array([
    0.1,
    0.2,
    0.05,
    0.12,
    0.07,
    0.23,
    0.13,
])
mass = numpy.array([
    1.0,
    2.0,
    0.5,
    0.3,
    0.5,
    2.0,
    1.7
])
elascity = numpy.array([
    [0.5, 0.7, 0.3, 0.5, 0.8, 0.8, 0.8],
    [0.7, 0.9, 0.4, 0.7, 0.8, 0.8, 0.8],
    [0.3, 0.4, 0.2, 0.8, 0.8, 0.8, 0.8],
    [0.5, 0.7, 0.1, 0.8, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
])
decay = numpy.array([
    [0.5, 0.5, 0.5],
    [0.7, 0.7, 0.7],
    [1.0, 1.0, 1.0],
    [0.9, 0.9, 0.9],
    [0.9, 0.9, 0.9],
    [0.9, 0.9, 0.9],
    [0.9, 0.9, 0.9],
])

width = 0.7
height = 0.7

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
    
    for i in range(n):
        glPushMatrix()
        glTranslated(*position[i])
        glScaled(*(radius[i] * numpy.ones(3)))
        glColor3dv(color[i])
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
    for i in range(sides):
        glVertex2d(math.cos(2.0 * math.pi * i / sides), math.sin(2.0 * math.pi * i / sides))
    glEnd()

    glEndList()

    glNewList(2, GL_COMPILE)

    glBegin(GL_LINES)
    glColor3d(1.0, 1.0, 1.0)
    glVertex2d(-width, 1.0)
    glVertex2d(-width, -height)
    glVertex2d(-width, -height)
    glVertex2d(width, -height)
    glVertex2d(width, -height)
    glVertex2d(width, 1.0)
    glEnd()

    glEndList()

def update(interval):
    
    global position, velocity

    reflect()

    position += velocity * interval + gravity * interval**2 / 2.0
    velocity += gravity * interval
    pass

def reflect():

    global position, velocity

    for i in range(n):
        for j, e in enumerate(equations):
            if e[:3].dot(position[i]) + e[3] - radius[i] < 0.0 and e[:3].dot(velocity[i]) < 0.0:
                velocity[i] = velocity[i] - (1 + decay[i, j]) * e[:3] * (e[:3].dot(velocity[i]))
                position[i] -= (e[:3].dot(position[i]) + e[3] - radius[i]) * e[:3]
    
    for i in range(n):
        for j in range(i+1, n):
            delta_ij = position[j] - position[i]
            length_ij = numpy.linalg.norm(delta_ij)
            norm_ij = delta_ij / length_ij
            if length_ij < radius[i] + radius [j] and norm_ij.dot(velocity[j] - velocity[i]) < 0.0:
                proj_vel_i = norm_ij.dot(velocity[i])
                proj_vel_j = norm_ij.dot(velocity[j])
                new_proj_vel_i = (mass[i] * proj_vel_i + mass[j] * proj_vel_j + (proj_vel_j - proj_vel_i) * elascity[i, j] * mass[j]) / (mass[i] + mass[j])
                new_proj_vel_j = new_proj_vel_i - elascity[i, j] * (proj_vel_j - proj_vel_i)
                velocity[i] += (new_proj_vel_i - proj_vel_i) * norm_ij
                velocity[j] += (new_proj_vel_j - proj_vel_j) * norm_ij
                position[i] -= norm_ij * radius[i] / (radius[i] + radius[j]) * (radius[i] + radius [j] - length_ij)
                position[j] += norm_ij * radius[j] / (radius[i] + radius[j]) * (radius[i] + radius [j] - length_ij)
                
    
glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

glutInitWindowSize(800, 800)

glutCreateWindow("Python Gravity Simulator")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

initialize()

make()

glutMainLoop()
