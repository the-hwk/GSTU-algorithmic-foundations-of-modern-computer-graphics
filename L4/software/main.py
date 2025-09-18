import pygame
from pygame.locals import DOUBLEBUF, OPENGL, NOFRAME

import OpenGL.GL as GL
from OpenGL.GLU import gluPerspective

import numpy as np

from math import pi, sin, cos

import geometry

class Util:
    @staticmethod
    def centralize_points(points):
        X_MIN = np.min(points[:, 0])
        X_MAX = np.max(points[:, 0])

        Y_MIN = np.min(points[:, 1])
        Y_MAX = np.max(points[:, 1])

        Z_MIN = np.min(points[:, 2])
        Z_MAX = np.max(points[:, 2])

        D = [
            [1, 0, 0, -(X_MAX - X_MIN) / 2.0],
            [0, 1, 0, -(Y_MAX - Y_MIN) / 2.0],
            [0, 0, 1, -(Z_MAX - Z_MIN) / 2.0],
            [0, 0, 0, 1]
        ]

        points_ones = np.append(np.swapaxes(points, 0, 1), [np.ones(points.shape[0])], axis=0)

        return np.swapaxes((D @ points_ones), 0, 1)[:, :3]

    @staticmethod
    def rotate(points, angle_x, angle_y, angle_z):
        a_x = angle_x * pi / 180
        a_y = angle_y * pi / 180
        a_z = angle_z * pi / 180

        RX = [
            [1, 0, 0, 0],
            [0, cos(a_x), -sin(a_x), 0],
            [0, sin(a_x), cos(a_x), 0],
            [0, 0, 0, 1]
        ]
        RY = [
            [cos(a_y), 0, sin(a_y), 0],
            [0, 1, 0, 0],
            [-sin(a_y), 0, cos(a_y), 0],
            [0, 0, 0, 1]
        ]
        RZ = [
            [cos(a_z), -sin(a_z), 0, 0],
            [sin(a_z), cos(a_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        points_ones = np.column_stack((points, np.ones(points.shape[0])))
        
        return (points_ones @ RX @ RY @ RZ)[:, :3]

class MainWindow:
    _BACKGROUND = np.array([32, 33, 37, 255]) / 255
    _EDGE = np.array([0, 0, 0]) / 255

    _screen : pygame.Surface = None
    _clock : pygame.time.Clock = None

    _poly_count : int = 0

    def __init__(self, width:int, height:int) -> None:    
        self._screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)

        self._clock = pygame.time.Clock()

        GL.glClearColor(*MainWindow._BACKGROUND)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        gluPerspective(75, (width / height), 0.1, 30.0)
        GL.glTranslatef(0.0, 0.0, -9)

    def _calc_color(self, poly_ind):
        c = (1.0 / self._poly_count) * poly_ind
        return np.array([c, c, c])
    
    def _draw_polygon(self, points:list[float], color:list[float]=[1, 1, 1]):
        c = color

        GL.glBegin(GL.GL_POLYGON)
        GL.glColor3f(c[0], c[1], c[2])
        
        for p in points:
            GL.glVertex3f(p[0], p[1], p[2])

        GL.glEnd()

        self._draw_edges(points)

    def _draw_edges(self, points:list[float]):
        c = MainWindow._EDGE

        GL.glBegin(GL.GL_LINE_LOOP)

        GL.glColor3f(c[0], c[1], c[2])
        
        for p in points:
            GL.glVertex3f(p[0], p[1], p[2])

        GL.glEnd()

    def cycle_poly_draw(self):
        cent_points = Util.centralize_points(geometry.POINTS)
        geom_points = Util.rotate(cent_points, 0, 30, 0)

        polygons = geometry.calc_poly_order(geom_points)
        self._poly_count = len(polygons)
        poly_ind = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            color = self._calc_color(poly_ind)
            self._draw_polygon(geometry.get_poly_points(polygons[poly_ind], geom_points), color)

            poly_ind += 1

            pygame.display.flip()

            if poly_ind == self._poly_count:
                pygame.time.wait(3000)

                poly_ind = 0
                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            else:
                pygame.time.wait(1000)
            
        pygame.quit()

    def rotate_and_draw(self, framerate=30):
        angle_y = 0
        
        cent_points = Util.centralize_points(geometry.POINTS)

        self._poly_count = len(geometry.POLYGONS)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            geom_points = Util.rotate(cent_points, 0, angle_y, 0)

            polygons = geometry.calc_poly_order(geom_points)

            for ind, poly in enumerate(polygons):
                color = self._calc_color(ind)
                self._draw_polygon(geometry.get_poly_points(poly, geom_points), color)

            pygame.display.flip()

            if angle_y == 359:
                angle_y = 0
            else:
                angle_y += 1

            self._clock.tick(framerate)            

if __name__ == "__main__":
    window = MainWindow(800, 600)
    window.rotate_and_draw()