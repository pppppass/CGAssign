#! /usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angle = 0.0

def display():

    global angle

    angle += 1.0
    
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(angle, 0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)
    glColor3d(1.0, 0.0, 0.0)
    glVertex3d(1.0, 0.0, 0.0)
    glColor3d(0.0, 1.0, 0.0)
    glVertex3d(0.0, 1.0, 0.0)
    glColor3d(0.0, 0.0, 1.0)
    glVertex3d(0.0, 0.0, 1.0)
    glEnd()

    glutSwapBuffers()

    glutPostRedisplay()

def redraw(w, h):
    
    glutPostRedisplay()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutInitWindowSize(800, 800)

glutCreateWindow("Python OpenGL Framework")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
