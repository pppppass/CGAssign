#! /usr/bin/env python3

from time import time

import numpy
import scipy.linalg

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angle = 0.0
rotate_speed = 1.0

delta_angle = 0.05

check_interval = 0.5
now_interval = time() // check_interval
frame_counter = 0

view_matrix = numpy.eye(4)


def frame_per_second():

    global frame_counter, now_interval

    frame_counter += 1

    next_interval = time() // check_interval
    if next_interval > now_interval:
        output = frame_counter / check_interval
        print("FPS: ", output)
        frame_counter = 0
        now_interval = next_interval


def display():

    global angle

    angle += rotate_speed

    frame_per_second()

    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    glPushMatrix()

    glRotated(angle, 0.0, 0.0, 1.0)

    glCallList(2)

    glPopMatrix()

    glCallList(1)

    glutSwapBuffers()

    glutPostRedisplay()


def initialize():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)

    glPointSize(2.5)
    glLineWidth(3.5)


def make():

    glNewList(1, GL_COMPILE)

    glBegin(GL_LINES)
    glColor3d(0.5, 0.0, 0.0)
    glVertex3d(-1.0, 0.0, 0.0)
    glColor3d(1.0, 0.0, 0.0)
    glVertex3d(1.0, 0.0, 0.0)
    glColor3d(0.0, 0.5, 0.0)
    glVertex3d(0.0, -1.0, 0.0)
    glColor3d(0.0, 1.0, 0.0)
    glVertex3d(0.0, 1.0, 0.0)
    glColor3d(0.0, 0.0, 0.5)
    glVertex3d(0.0, 0.0, -1.0)
    glColor3d(0.0, 0.0, 1.0)
    glVertex3d(0.0, 0.0, 1.0)
    glEnd()

    glEndList()

    glNewList(2, GL_COMPILE)

    glBegin(GL_TRIANGLES)
    glColor3d(1.0, 0.0, 0.0)
    glVertex3d(1.0, 0.0, 0.0)
    glColor3d(0.0, 1.0, 0.0)
    glVertex3d(0.0, 1.0, 0.0)
    glColor3d(0.0, 0.0, 1.0)
    glVertex3d(0.0, 0.0, 1.0)
    glEnd()

    glEndList()


def redraw(w, h):
    glutPostRedisplay()


def rotate(k, x, y):

    global view_matrix

    if k == b'd':
        rot = scipy.linalg.expm(numpy.cross(
            numpy.eye(3), numpy.array([0.0, 1.0, 0.0]) * delta_angle))
    elif k == b'a':
        rot = scipy.linalg.expm(numpy.cross(
            numpy.eye(3), numpy.array([0.0, -1.0, 0.0]) * delta_angle))
    elif k == b'w':
        rot = scipy.linalg.expm(numpy.cross(
            numpy.eye(3), numpy.array([-1.0, 0.0, 0.0]) * delta_angle))
    elif k == b's':
        rot = scipy.linalg.expm(numpy.cross(
            numpy.eye(3), numpy.array([1.0, 0.0, 0.0]) * delta_angle))
    else:
        return None

    view_matrix[:3, :3] = view_matrix[:3, :3].dot(rot)

    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(view_matrix)


glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)

glutInitWindowSize(800, 800)

glutCreateWindow("Python OpenGL Framework")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutKeyboardFunc(rotate)

initialize()

make()

glutMainLoop()
