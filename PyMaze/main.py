#! /usr/bin/env python3

import argparse
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy

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

def perimeter(k):
    if k < m*(n+1):
        return k < m or k >= m*n
    else:
        return k < m*(n+1) + n or k >= m*(n+1) + m*n

def connected(store=False):

    vis = [[False for j in range(m)] for i in range(n)]
    ctr = 0
    queue = []
    mem = []
    
    def check(k):
        if not perimeter(k):
            if not maze[k]:
                return True
            else:
                if store:
                    mem.append(k)
                return False
        else:
            False
    
    u, v = random.randint(0, n-1), random.randint(0, m-1)
    queue.append((u, v))

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

    random.shuffle(mem)

    return ctr, mem

def generate_maze():

    global maze

    while True:
        ctr, mem = connected(store=True)
        if ctr == n*m:
            break
        else:
            for k in mem:
                maze[k] = False
                nctr, _ = connected()
                if nctr > ctr:
                    ctr = nctr
                    break
                else:
                    maze[k] = True
    
    for i in range(2):
        while True:
            k = random.randint(0, m*(n+1) + n*(m+1) - 1)
            if perimeter(k) and maze[k]:
                maze[k] = False
                break

def draw_maze():
    
    glBegin(GL_LINES)
    
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

def display():
    
    draw_maze()

    glutSwapBuffers()

def redraw(w, h):
    
    glutPostRedisplay()

generate_maze()

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutInitWindowSize(800, 800)

glutCreateWindow("Python OpenGL Framework")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutMainLoop()
