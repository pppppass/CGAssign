#! /usr/bin/env python3

import argparse

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

parser = argparse.ArgumentParser(description="Draw a circle using Bresenham's algorithm")
parser.add_argument("r", metavar="R", type=int, help="Radius of the circle")
parser.add_argument("n", metavar="N", type=int, nargs="?", default=20, help="Half size of the canvas")

args = parser.parse_args()
n = args.n
r = args.r

side = 2.0 / (2*n)

list_ = []

def draw_pixel(x, y):
    glVertex2d(x * side, y*side)
    glVertex2d((x+1) * side, y*side)
    glVertex2d((x+1) * side, (y+1)*side)
    glVertex2d(x * side, (y+1)*side)

def draw_axis():
    glVertex2d(-1.0, 0.0)
    glVertex2d(1.0, 0.0)
    glVertex2d(0.0, -1.0)
    glVertex2d(0.0, 1.0)
    for i in range(-n, n+1):
        glVertex2d(i * side, 0.0)
        glVertex2d(i * side, side / 2.0)
    for i in range(-n, n+1):
        glVertex2d(0.0, i * side)
        glVertex2d(side / 2.0, i * side)

def bresenham_circle(r):
    global list_
    x, y, d = 0, -r - 1, 4*r + 2
    while True:
        if d < 0:
            list_.append((x, y))
            x += 1
            d += 8*x
        else:
            y += 1
            list_.append((x, y))
            x += 1
            d += 8*x + 8*y + 4
        if x + y >= 0:
            break
    list_ += [(-x - 1, y) for (x, y) in list_]
    list_ += [(x, -y - 1) for (x, y) in list_]
    list_ += [(y, x) for (x, y) in list_]

def display():
    
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_QUADS)
    glColor3d(1.0, 1.0, 1.0)
    for (x, y) in list_:
        draw_pixel(x, y)
    glEnd()

    glBegin(GL_LINES)
    glColor3d(1.0, 1.0, 1.0)
    draw_axis()
    glEnd()

    glutSwapBuffers()

    glutPostRedisplay()

def redraw(w, h):
    
    glutPostRedisplay()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutInitWindowSize(800, 800)

glutCreateWindow("Python OpenGL Circle")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

bresenham_circle(r)

glutMainLoop()
