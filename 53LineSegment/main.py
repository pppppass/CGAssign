#! /usr/bin/env python3

import argparse

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

parser = argparse.ArgumentParser(description="Draw a line segment using Bresenham's algorithm")
parser.add_argument("x1", metavar="X1", type=int, help="x-coordinate of the first endpoint")
parser.add_argument("y1", metavar="Y1", type=int, help="y-coordinate of the first endpoint")
parser.add_argument("x2", metavar="X2", type=int, help="x-coordinate of the second endpoint")
parser.add_argument("y2", metavar="Y2", type=int, help="y-coordinate of the second endpoint")
parser.add_argument("n", metavar="N", type=int, nargs="?", default=20, help="Half size of the canvas")

args = parser.parse_args()
n = args.n
x1, y1, x2, y2 = args.x1, args.y1, args.x2, args.y2

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

def bresenham_segment(x1, y1, x2, y2):
    global list_
    dx, dy = x2 - x1, y2 - y1
    if dx + dy < 0:
        x1, y1, x2, y2, dx, dy = x2, y2, x1, y1, -dx, -dy
    if -dx + dy <= 0:
        if dy >= 0:
            x, y, d = x1, y1 - 1, -dy
            for i in range(dx+1):
                if d > 0:
                    list_.append((x, y))
                    x += 1
                    d -= 2*dy
                else:
                    y += 1
                    list_.append((x, y))
                    x += 1
                    d -= 2*(dy - dx)
        else:
            x, y, d = x1, y1 + 1, -dy
            for i in range(dx+1):
                if d < 0:
                    list_.append((x, y))
                    x += 1
                    d -= 2*dy
                else:
                    y -= 1
                    list_.append((x, y))
                    x += 1
                    d -= 2*(dy + dx)
    else:
        if dx >= 0:
            x, y, d = x1 - 1, y1, -dx
            for i in range(dy+1):
                if d > 0:
                    list_.append((x, y))
                    y += 1
                    d -= 2*dx
                else:
                    x += 1
                    list_.append((x, y))
                    y += 1
                    d -= 2*(dx - dy)
        else:
            x, y, d = x1 + 1, y1, -dx
            for i in range(dy+1):
                if d < 0:
                    list_.append((x, y))
                    y += 1
                    d -= 2*dx
                else:
                    x -= 1
                    list_.append((x, y))
                    y += 1
                    d -= 2*(dx + dy)

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

glutCreateWindow("Python OpenGL Line Segment")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

bresenham_segment(x1, y1, x2, y2)

glutMainLoop()
