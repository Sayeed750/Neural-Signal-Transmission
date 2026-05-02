from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

width, height = 1000, 700

nodes = []
connections = []
signals = []

camera_x = 0
camera_z = 18
angle = 0


def create_network():
    global nodes, connections

    nodes = []
    connections = []

    for i in range(80):
        x = random.uniform(-5, 5)
        y = random.uniform(-4, 4)
        z = random.uniform(-5, 5)
        nodes.append((x, y, z))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.05:
                connections.append((i, j))


def spawn_signal():
    if len(connections) == 0:
        return

    c = random.choice(connections)
    signals.append([c, 0.0])


def draw_nodes():
    glDisable(GL_LIGHTING)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    for n in nodes:
        glColor4f(0.2, 0.8, 1.0, 0.8)

        glPushMatrix()
        glTranslatef(n[0], n[1], n[2])
        glutSolidSphere(0.12, 16, 16)
        glPopMatrix()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_connections():
    glDisable(GL_LIGHTING)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.3, 0.6, 1.0, 0.25)

    glBegin(GL_LINES)
    for c in connections:
        n1 = nodes[c[0]]
        n2 = nodes[c[1]]
        glVertex3f(*n1)
        glVertex3f(*n2)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_signals():
    glDisable(GL_LIGHTING)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    for s in signals:
        (i, j), t = s

        n1 = nodes[i]
        n2 = nodes[j]

        x = n1[0] + (n2[0] - n1[0]) * t
        y = n1[1] + (n2[1] - n1[1]) * t
        z = n1[2] + (n2[2] - n1[2]) * t

        glColor4f(1.0, 0.2, 1.0, 0.9)

        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidSphere(0.1, 12, 12)
        glPopMatrix()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def update_signals():
    global signals

    new_signals = []

    for s in signals:
        s[1] += 0.03
        if s[1] < 1.0:
            new_signals.append(s)

    signals = new_signals

    if random.randint(0, 5) == 0:
        spawn_signal()


def setup_fog():
    glEnable(GL_FOG)

    glFogfv(GL_FOG_COLOR, [0.02, 0.02, 0.05, 1])
    glFogi(GL_FOG_MODE, GL_EXP2)
    glFogf(GL_FOG_DENSITY, 0.05)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(
        camera_x, 0, camera_z,
        0, 0, 0,
        0, 1, 0
    )

    glRotatef(angle, 0, 1, 0)

    draw_connections()
    draw_nodes()
    draw_signals()

    glutSwapBuffers()


def update(value):
    global angle

    angle += 0.2
    update_signals()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def reshape(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, w / h, 1, 100)

    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    global camera_x, camera_z

    if key == b'w':
        camera_z -= 0.6
    elif key == b's':
        camera_z += 0.6
    elif key == b'a':
        camera_x -= 0.6
    elif key == b'd':
        camera_x += 0.6
    elif key == b'\x1b':
        glutLeaveMainLoop()


def init():
    glClearColor(0.01, 0.01, 0.04, 1)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    setup_fog()
    create_network()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutCreateWindow(b"Neural Activity")

init()

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)

glutMainLoop()