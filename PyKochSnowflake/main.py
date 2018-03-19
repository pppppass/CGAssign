#! /usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy
import scipy.linalg

omega = scipy.linalg.expm(numpy.cross(numpy.eye(3), numpy.array([0., 0., 1.]) * math.pi * 2. / 3.))

def koch(s, e, rem=6):
    if rem < 0:
        return None
    elif rem == 0:
        glBegin(GL_LINES)

        glVertex3dv(s)
        glVertex3dv(e)

        glEnd()
    else:
        v = (e - s) / 3.
        m1 = s + v
        m2 = m1 - omega.dot(v)
        m3 = e - v
        
        koch(s, m1, rem=rem-1)
        koch(m1, m2, rem=rem-1)
        koch(m2, m3, rem=rem-1)
        koch(m3, e, rem=rem-1)

def display():
    
    glClear(GL_COLOR_BUFFER_BIT)

    s1 = numpy.array([0.5, 0.0, 0.0])
    s2 = omega.dot(s1)
    s3 = omega.dot(s2)

    koch(s1, s2)
    koch(s2, s3)
    koch(s3, s1)

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
