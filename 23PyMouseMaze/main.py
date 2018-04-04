#! /usr/bin/env python3

import math
import argparse
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy
import scipy.linalg

random.seed(1)

parser = argparse.ArgumentParser(description="Draw a maze of given size")
parser.add_argument("n", metavar="N", type=int, help="Size in columns")
parser.add_argument("m", metavar="M", type=int, help="Size in rows")

args = parser.parse_args()
m, n = args.m, args.n

maze = [True for i in range(m*(n+1) + n*(m+1))]

ul = 1.6 / max(m, n)
sp = numpy.array([-ul * n / 2., -ul * m / 2.])
vx = numpy.array([ul, 0.])
vy = numpy.array([0., ul])

p = numpy.array([
    [1.0, 0.0, 0.0, 1.0],
    [math.cos(2.5), math.sin(2.5), 0.0, 1.0],
    [math.cos(2.5), -math.sin(2.5), 0.0, 1.0],
])

t = numpy.eye(4)
t[:2, :2] *= 0.24 * ul
t[3, 0] = -0.9

mtf, mtb, mrl, mrr = [numpy.eye(4) for i in range(4)]
mtf[3, 0] = 0.2
mtb[3, 0] = -0.2
mrl[:3, :3] = scipy.linalg.expm(numpy.cross(numpy.eye(3), numpy.array([0.0, 0.0, 1.0]) * 0.1))
mrr[:3, :3] = scipy.linalg.expm(numpy.cross(numpy.eye(3), numpy.array([0.0, 0.0, 1.0]) * -0.1))

def perimeter(k):
    if k < m*(n+1):
        return k < m or k >= m*n
    else:
        return k < m*(n+1) + n or k >= m*(n+1) + m*n

def generate():

    global maze

    vis = [[False for j in range(m)] for i in range(n)]
    ctr = 0
    queue = []
    mem = []
    u, v = n-1, m//2
    
    def check(k):
        if not perimeter(k):
            if not maze[k]:
                return True
            else:
                mem.append(k)
                return False
        else:
            False
    
    def distinct(k):
        nonlocal u, v

        if k < m*(n+1):
            x = k // m
            y = k - m*x
            if x <= 0 or x > n:
                return False
            else:
                if not vis[x-1][y]:
                    u, v = x-1, y
                    return True
                elif not vis[x][y]:
                    u, v = x, y
                    return True
                else:
                    return False
        else:
            y = (k - m*(n+1)) // n
            x = (k - m*(n+1)) - n*y
            if y <= 0 or y > n:
                return False
            else:
                if not vis[x][y-1]:
                    u, v = x, y-1
                    return True
                elif not vis[x][y]:
                    u, v = x, y
                    return True
                else:
                    return False

    def start():
        nonlocal ctr

        while len(queue):
            x, y = queue.pop()
            if not vis[x][y]:
                ctr += 1
                vis[x][y] = True
                if check(x*m + y):
                    queue.append((x-1, y))
                if check((x+1)*m + y):
                    queue.append((x+1, y))
                if check(m*(n+1) + x + y*n):
                    queue.append((x, y-1))
                if check(m*(n+1) + x + (y+1)*n):
                    queue.append((x, y+1))

    while ctr < n*m:
        queue.append((u, v))
        start()
        if ctr >= n*m:
            break
        else:
            while True:
                k = random.randint(0, len(mem) - 1)
                t = mem[k]
                del mem[k]
                if distinct(t):
                    maze[t] = False
                    break

    p1 = random.randint(0, m // 3)
    maze[p1] = False
    p2 = random.randint((2 * m) // 3, m-1)
    maze[p2] = False

def make():
    
    glNewList(1, GL_COMPILE)

    glBegin(GL_LINES)
    glColor3d(1.0, 1.0, 1.0)
    for i in range(n+1):
        for j in range(m):
            if maze[i*m + j]:
                glVertex2dv(sp + i*vx + j*vy)
                glVertex2dv(sp + i*vx + (j+1)*vy)
    for i in range(n):
        for j in range(m+1):
            if maze[m*(n+1) + i + j*n]:
                glVertex2dv(sp + i*vx + j*vy)
                glVertex2dv(sp + (i+1)*vx + j*vy)
    glEnd()
    
    glEndList()

    glNewList(2, GL_COMPILE)
    
    glBegin(GL_POLYGON)
    glColor3d(0.6, 0.6, 0.6)
    for c in p:
        glVertex4dv(c)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glColor3d(0.3, 0.3, 0.3)
    for c in p:
        glVertex4dv(c)
    glEnd()

    glEndList()

def display():
    
    glClear(GL_COLOR_BUFFER_BIT)

    glCallList(1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixd(t)
    glCallList(2)
    glPopMatrix()

    glutSwapBuffers()

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

def move(k, x, y):

    global t

    if k == b'w':
        nt = mtf.dot(t)
    elif k == b's':
        nt = mtb.dot(t)
    elif k == b'a':
        nt = mrr.dot(t)
    elif k == b'd':
        nt = mrl.dot(t)
    else:
        return None
    
    if check(nt):
        t = nt

    glutPostRedisplay()

def check(nt):
    np = nt[3, 0:2]
    x, y = (np - sp) // ul
    x, y = int(x+0.5), int(y+0.5)
    
    for i in range(max(0, x), min(n+1, x+2)):
        for j in range(max(0, y-1), min(m, y+2)):
            if maze[i*m + j] and intersect_mouse(sp + i*vx + j*vy, sp + i*vx + (j+1)*vy, nt):
                return False

    for i in range(max(0, x-1), min(n, x+2)):
        for j in range(max(0, y), min(m+1, y+2)):
            if maze[m*(n+1) + i + j*n] and intersect_mouse(sp + i*vx + j*vy, sp + (i+1)*vx + j*vy, nt):
                return False
    
    return True

def orientation(p1, p2, p3):
    area = p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
    return numpy.sign(area)

def intersect(p1, p2, q1, q2):
    return (orientation(p1, p2, q1) != orientation(p1, p2, q2) and orientation(q1, q2, p1) != orientation(q1, q2, p2))

def intersect_mouse(p1, p2, nt):
    q1, q2, q3 = p.dot(nt)[:, :2]
    return intersect(p1, p2, q1, q2) or intersect(p1, p2, q2, q3) or intersect(p1, p2, q3, q1)

generate()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutInitWindowSize(800, 800)

glutCreateWindow("Python OpenGL Framework")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutKeyboardFunc(move)

initialize()

make()

glutMainLoop()
