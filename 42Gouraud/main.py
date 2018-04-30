#! /usr/bin/env python3

import math
from time import time
import argparse

import numpy
import scipy.linalg

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

parser = argparse.ArgumentParser(description="Show comparision about different shading models, including Gouraud shading")
parser.add_argument("n", metavar="N", type=int, help="Number of iterations of subdivision")

args = parser.parse_args()
n = args.n

delta_angle = 0.05

view_matrix = numpy.eye(4)

light_pos = numpy.array([1.0, 1.0, 1.0, 1.0])
light_amb = numpy.array([0.5, 0.0, 0.0, 1.0])
light_diff = numpy.array([0.0, 0.0, 1.0, 1.0])
light_spec = numpy.array([0.0, 1.0, 0.0, 1.0])
mat_amb = numpy.array([0.2, 0.2, 0.2, 1.0])
mat_diff = numpy.array([0.8, 0.8, 0.8, 1.0])
mat_spec = numpy.array([1.0, 1.0, 1.0, 1.0])
mat_shin = numpy.array([20.0])

tetra_verts = [
    numpy.array([0.0, 0.0, -1.0]),
    numpy.array([0.0, 2.0*math.sqrt(2)/3.0, 1.0/3.0]),
    numpy.array([-math.sqrt(6)/3.0, -math.sqrt(2)/3.0, 1.0/3.0]),
    numpy.array([math.sqrt(6)/3.0, -math.sqrt(2)/3.0, 1.0/3.0]),
]
tetra_edges = [
    [1, 2, 3],
    [2, 3],
    [3],
    []
]
tetra_surfs = []
tetra_norms = []
vert_norms = []

def sub_div():

    global tetra_verts, tetra_edges
    
    leng_lst = []
    for i, lst in enumerate(tetra_edges):
        leng_lst.append(len(tetra_verts))
        for j in lst:
            new_vert = tetra_verts[i] + tetra_verts[j]
            new_vert /= numpy.linalg.norm(new_vert)
            tetra_verts.append(new_vert)
    
    new_edges = [[] for i in range(len(tetra_verts))]
    for i, lst in enumerate(tetra_edges):
        for j_ in range(len(lst)):
            j = lst[j_]
            for k_ in range(j_+1, len(lst)):
                k = lst[k_]
                if k not in tetra_edges[j]:
                    continue
                ij, ik, jk = leng_lst[i] + j_,  leng_lst[i] + k_, leng_lst[j] + tetra_edges[j].index(k)
                new_edges[i].append(ij)
                new_edges[i].append(ik)
                new_edges[j].append(ij)
                new_edges[j].append(jk)
                new_edges[k].append(ik)
                new_edges[k].append(jk)
                new_edges[ij].append(ik)
                new_edges[ij].append(jk)
                new_edges[ik].append(jk)
    
    for i in range(len(new_edges)):
        new_edges[i] = list(set(new_edges[i]))
        new_edges[i].sort()
    
    tetra_edges = new_edges

def gen_surfs():
    global tetra_surfs, vert_norms
    vert_norms = [numpy.zeros(3) for i in range(len(tetra_verts))]
    surf_ctrs = [0 for i in range(len(tetra_verts))]
    for i, lst in enumerate(tetra_edges):
        for j_ in range(len(lst)):
            j = lst[j_]
            for k_ in range(j_+1, len(lst)):
                k = lst[k_]
                if k not in tetra_edges[j]:
                    continue
                normal = tetra_verts[i]
                vi, vj, vk = (tetra_verts[t] for t in (i, j, k))
                sign = numpy.dot(vi, numpy.cross(vj, vk))
                if sign >= 0.0:
                    tetra_surfs.append((i, j, k))
                else:
                    tetra_surfs.append((i, k, j))
                norm = numpy.cross(vj - vi, vk - vi) * sign
                norm /= numpy.linalg.norm(norm)
                tetra_norms.append(norm)
                for u in (i, j, k):
                    vert_norms[u] += norm
                    surf_ctrs[u] += 1
    for i in range(len(tetra_verts)):
        vert_norms[i] /= surf_ctrs[i]


def display():

    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glTranslated(-1.5, 0.0, 0.0)
    glScaled(0.45, 0.45, 0.45)
    set_lights()
    glShadeModel(GL_FLAT)
    glCallList(3)
    glPopMatrix()

    glPushMatrix()
    glTranslated(-0.5, 0.0, 0.0)
    glScaled(0.45, 0.45, 0.45)
    set_lights()
    glShadeModel(GL_SMOOTH)
    glCallList(3)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0.5, 0.0, 0.0)
    glScaled(0.45, 0.45, 0.45)
    set_lights()
    glCallList(4)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.5, 0.0, 0.0)
    glScaled(0.45, 0.45, 0.45)
    set_lights()
    glCallList(5)
    glPopMatrix()

    glDisable(GL_LIGHTING)
    glCallList(1)

    glPushMatrix()
    glTranslated(*light_pos[:3])
    glCallList(2)
    glPopMatrix()

    glutSwapBuffers()

    glutPostRedisplay()


def initialize():

    for i in range(n):
        sub_div()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)

    glPointSize(2.5)
    glLineWidth(3.5)

    glMatrixMode(GL_PROJECTION)
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)

    gen_surfs()


def set_lights():
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_amb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diff)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_spec)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_amb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diff)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_spec)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shin)


def make():

    glNewList(1, GL_COMPILE)
    glBegin(GL_LINES)
    glColor3d(0.3, 0.0, 0.0)
    glVertex3d(-1.0, 0.0, 0.0)
    glColor3d(1.0, 0.0, 0.0)
    glVertex3d(1.0, 0.0, 0.0)
    glColor3d(0.0, 0.3, 0.0)
    glVertex3d(0.0, -1.0, 0.0)
    glColor3d(0.0, 1.0, 0.0)
    glVertex3d(0.0, 1.0, 0.0)
    glColor3d(0.0, 0.0, 0.3)
    glVertex3d(0.0, 0.0, -1.0)
    glColor3d(0.0, 0.0, 1.0)
    glVertex3d(0.0, 0.0, 1.0)
    glColor3d(1.0, 1.0, 1.0)
    glEnd()
    glEndList()

    glNewList(2, GL_COMPILE)
    glColor3d(1.0, 1.0, 1.0)
    glutSolidSphere(0.1, 20, 20)
    glEndList()

    glNewList(3, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for lst, norm in zip(tetra_surfs, tetra_norms):
        glNormal3dv(norm)
        for i in range(3):
           glVertex3dv(tetra_verts[lst[i]])
    glEnd()
    glEndList()

    glNewList(4, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for lst, norm in zip(tetra_surfs, tetra_norms):
        for i in range(3):
            glNormal3dv(vert_norms[lst[i]])
            glVertex3dv(tetra_verts[lst[i]])
    glEnd()
    glEndList()

    glNewList(5, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for lst, norm in zip(tetra_surfs, tetra_norms):
        for i in range(3):
            glNormal3dv(tetra_verts[lst[i]])
            glVertex3dv(tetra_verts[lst[i]])
    glEnd()
    glEndList()


def redraw(w, h):
    glutPostRedisplay()


def rotate(k, x, y):

    global view_matrix

    if k in {b'd', b'a', b'w', b's'}:

        if k == b'd':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([0.0, -1.0, 0.0]) * delta_angle))
        elif k == b'a':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([0.0, +1.0, 0.0]) * delta_angle))
        elif k == b'w':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([+1.0, 0.0, 0.0]) * delta_angle))
        elif k == b's':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([-1.0, 0.0, 0.0]) * delta_angle))

        view_matrix[:3, :3] = view_matrix[:3, :3].dot(rot)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixd(view_matrix)
    
    elif k in {b'h', b'j', b'n', b'm'}:

        if k == b'h':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([0.0, -1.0, 0.0]) * delta_angle))
        elif k == b'j':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([0.0, +1.0, 0.0]) * delta_angle))
        elif k == b'n':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([+1.0, 0.0, 0.0]) * delta_angle))
        elif k == b'm':
            rot = scipy.linalg.expm(numpy.cross(
                numpy.eye(3), numpy.array([-1.0, 0.0, 0.0]) * delta_angle))

        light_pos[:3] = rot.dot(light_pos[:3])

glutInit(sys.argv)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)

glutInitWindowSize(800, 800)

glutCreateWindow("Python Gouraud Shading")

glutDisplayFunc(display)

glutReshapeFunc(redraw)

glutKeyboardFunc(rotate)

initialize()

make()

glutMainLoop()
