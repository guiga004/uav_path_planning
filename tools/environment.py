"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import math
import matplotlib.pyplot as plt
import numpy as np

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


class Environment:
    """
    This defines an environment, an m x n sized grid
    """

    def __init__(self, width, length, obstacles=None):
        """
        :param width     : in arbitrary units
        :param length    : in arbitrary units
        :param obstacles : a list of Obstacle objects
        """
        self.width = width
        self.length = length
        self.obstacles = obstacles

        self.center = [width / 2, length / 2]

        # populate cities based on width and height
        # these cities are simply evenly spaced points in a graph
        self.cities = []
        self.get_cities

    # this will populate a list of cities based on the environment dimensions
    @property
    def get_cities(self):

        # calculate city coordinates if not yet calculated
        if not self.cities:

            for w in range(self.width):

                for h in range(self.length):
                    # these will calculate the cities' coordinates
                    # assumption made that each city is in the center of a square on an mxn grid
                    city_w = w + 0.5
                    city_h = h + 0.5

                    # add each new city to the list of cities
                    self.cities.append([city_w, city_h])

        return self.cities

    # https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    @staticmethod
    def angle_between(v1, v2):
        """
        :param v1   : first np.array, this is the reference axis
        :param v2   : second np.array, this is a vector from the center to the desired point
        :return     :
        """

        def unit_vector(vector):
            """
            :param vector : a numpy 1x2 array
            :return       : unit vector
            """
            return vector / np.linalg.norm(vector)

        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)

        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def quadrant(self, point):
        """
        :param point    : a tuple or list containing the coordinates of a point
        :return         : the location of the point relative to the center of the environment
        """

        # new vector with respect to the center point
        v_wr_c = np.array(point) - np.array(self.center)

        # center
        if v_wr_c[0] == 0 and v_wr_c[1] == 0:
            return 'c'

        # 0 degree position:
        elif v_wr_c[0] > 0 and v_wr_c[1] == 0:
            return 0

        # quadrant 1
        elif v_wr_c[0] > 0 and v_wr_c[1] > 0:
            return 1

        # 90 degree position:
        elif v_wr_c[0] == 0 and v_wr_c[1] > 0:
            return 90

        # quadrant 2
        elif v_wr_c[0] < 0 < v_wr_c[1]:
            return 2

        # 180 degree position:
        elif v_wr_c[0] < 0 and v_wr_c[1] == 0:
            return 180

        # quadrant 3
        elif v_wr_c[0] < 0 and v_wr_c[1] < 0:
            return 3

        # 270 degree position:
        elif v_wr_c[0] == 0 and v_wr_c[1] < 0:
            return 270

        # quadrant 4
        elif v_wr_c[0] > 0 > v_wr_c[1]:
            return 4

    def find_angle_from_center(self, point):
        """
        :param point    : a tuple or list containing the coordinates of a point
        :return         : the angle of that point relative to the reference axis
        """

        # edge case for the center
        if point == self.center:
            return 999

        # calculate the position of the point for a few corner cases
        position = Environment.quadrant(self, point)

        if position == 0 or position == 90 or position == 180 or position == 270:
            return np.radians(position)

        else:
            # vector from center point to edge of the graph
            reference_vector = np.array([2 * self.center[0], self.center[1]]) - np.array(self.center)

            # calculate new vector with respect to the center point
            v_wr_c = np.array(point) - np.array(self.center)

            # calculate the angle
            angle = Environment.angle_between(reference_vector, v_wr_c)

            # since the angle is solved using cosine, must use conjugate of points in the 3rd and 4th quadrant
            if position == 3 or position == 4 or position == '270':
                return math.radians(360) - angle

            else:
                return angle


class Voxel:
    # each voxel represents a 1x1x1 3D environment space
    def __init__(self, bottom_corner, voxel_type, identity=None):
        self.bottom_corner = bottom_corner  # lower left corner of the voxel
        self.voxel_type = voxel_type        # this can be 'free space' or 'obstacle' etc
        self.identity = identity            # the identity ex. 'tree'

    @staticmethod
    def create_voxels(known_voxels, specs):
        # remove empty voxel types for efficiency
        Voxel.delete_empty_keys(known_voxels)

        # create all of the Voxel objects and store them in a voxels list
        voxel_corners = []
        types = []
        expanded_voxels = []

        for key, values in known_voxels.items():
            for value in values:
                voxel_corners.append(value)
                types.append(key)

        for z in range(specs['z_max'] + 1):
            for y in range(specs['y_max'] + 1):
                for x in range(specs['x_max'] + 1):

                    point = [x, y, z]
                    if [x, y, z] in voxel_corners:
                        expanded_voxels.append(Voxel(bottom_corner=point, voxel_type=types[voxel_corners.index(point)]))
                    else:
                        expanded_voxels.append(Voxel(bottom_corner=point, voxel_type='free space'))

        return expanded_voxels

    @staticmethod
    def delete_empty_keys(dict_obj):
        empty_keys = []
        for dictKey in dict_obj:
            if not dict_obj[dictKey]:
                empty_keys.append(dictKey)

        for empty_key in empty_keys:
            del dict_obj[empty_key]

    @staticmethod
    def explode(data):
        size = np.array(data.shape) * 2
        data_e = np.zeros(size - 1, dtype=data.dtype)
        data_e[::2, ::2, ::2] = data
        return data_e

    @staticmethod
    def draw_voxels(a, b, c, color='#FFD65DC0'):

        # prepare some coordinates
        max_dim = max(a, b, c)
        x, y, z = np.indices((max_dim, max_dim, max_dim))

        # draw cuboids in the top left and bottom right corners, and a link between them
        cube = (x < a) & (y < b) & (z < c)

        # combine the objects into a single boolean array
        voxels = cube

        # set the colors of each object
        colors = np.empty(voxels.shape, dtype=object)
        colors[cube] = color

        # and plot everything
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(voxels, facecolors=colors, edgecolor='k')

        plt.title('3D Voxel Environment')

        plt.show()
