import math
import numpy as np

class Environment:
    """
    This defines an environment, an m x n sized grid
    """

    def __init__(self, width, height):
        """
        :param width  : in arbitrary units
        :param height : in arbitrary units
        """
        self.width = width
        self.height = height

        self.center = (width / 2, height / 2)

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

                for h in range(self.height):
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
        elif v_wr_c[0] < 0 and v_wr_c[1] > 0:
            return 2

        # 180 degree position:
        elif v_wr_c[0] < 0 and v_wr_c[1] == 0:
            return 180

        # quadrant 3
        elif v_wr_c[0] < 0 and v_wr_c[1] < 0:
            return 3

        # 270 degree position:
        elif v_wr_c[0] == 0 and v_wr_c[1] < 0:
            return '270'

        # quadrant 4
        elif v_wr_c[0] > 0 and v_wr_c[1] < 0:
            return 4

    def find_angle_from_center(self, point):
        """
        :param point    : a tuple or list containing the coordinates of a point
        :return         : the angle of that point relative to the reference axis
        """

        # edge case for the center
        if tuple(point) == self.center:
            return 'center'

        # calculate the position of the point for a few corner cases
        position = Environment.quadrant(self, point)

        if position == 0 or position == 90 or position == 180:
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
