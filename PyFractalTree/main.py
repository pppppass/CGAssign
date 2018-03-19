#! /usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy
import scipy.linalg

rot1 = scipy.linalg.expm(numpy.cross(numpy.eye(3), numpy.array([0., 0., 1.]) * math.pi * 1. / 4.))
rot2 = scipy.linalg.expm(numpy.cross(numpy.eye(3), numpy.array([0., 0., 1.]) * math.pi * (-1. / 4.)))

def tree(s, e, rem=12):
    if rem < 0:
        return None
    else:
        glBegin(GL_LINES)
        
        glVertex3dv(s)
        glVertex3dv(e)

        glEnd()
        
        v = e - s
        x = e + rot1.dot(v) * 0.7
        y = e + rot2.dot(v) * 0.7

        tree(e, x, rem=rem-1)
        tree(e, y, rem=rem-1)
        
def display():
    
    glClear(GL_COLOR_BUFFER_BIT)

    s = numpy.array([0.0, -0.5, 0.0])
    e = numpy.array([0.0, 0.0, 0.0])
    
    tree(s, e)

    glutSwapBuffers()

def redraw(w, h):
    
    glutPostRedisplay()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)

glutInitWindowSize(800, 800)

glutCreateWindow("Python Koch Snowflake")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
