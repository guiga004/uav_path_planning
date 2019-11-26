"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""

import math
import tsp
import numpy as np
import time
import matplotlib.pyplot as plt
import copy

# these are the files containing TSP algorithms
import Ants_python as ant
import tsp_genetic as gene


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
        self.get_cities()

    # this will collect a list of cities
    def get_cities(self):

        # calculate city coordinates if not yet calculated
        if not self.cities:

            for w in range(self.width):

                for h in range(self.height):
                    # these will calculate the cities' coordinates
                    city_w = w + 0.5
                    city_h = h + 0.5

                    # add each new city to the list of cities
                    self.cities.append([city_w, city_h])

        return self.cities

    # https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    @staticmethod
    def angle_between(v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """

        def unit_vector(vector):
            """ Returns the unit vector of the vector.  """
            return vector / np.linalg.norm(vector)

        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def quadrant(self, point):
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

        print('point', point)

        if tuple(point) == self.center:
            return 'center'

        # calculate the position of the point for a few corner cases
        position = Environment.quadrant(self, point)

        if position == 0 or position == 90 or position == 180:
            return np.radians(position)

        else:
            # vector from center point to edge of the graph
            center_vector = np.array([2 * self.center[0], self.center[1]]) - np.array(self.center)

            # calculate new vector with respect to the center point
            v_wr_c = np.array(point) - np.array(self.center)

            # calculate the angle
            angle = Environment.angle_between(center_vector, v_wr_c)

            if position == 3 or position == 4 or position == '270':
                return math.radians(360) - angle

            else:
                return angle

class Draw:
    """
    This class contains methods for environment visualization
    """

    def __init__(self, environment=None):

        self.env_fig = plt.figure()
        self.draw = self.env_fig.gca()
        self.title = ''

        self.environment = environment

    def draw_environment(self, title):
        """
        :param title        : title of the figure
        :return             : N/A
        """
        self.title = title
        width = self.environment.width
        height = self.environment.height

        for w in range(width + 1):

            if w == 0 or w == width:
                line = plt.Line2D((w, w), (0, height), lw=3, color='black')
                self.draw.add_line(line)

            else:
                line = plt.Line2D((w, w), (0, height), lw=1, color='dimgrey')
                self.draw.add_line(line)

            for h in range(height + 1):

                if h == 0 or h == height:
                    line = plt.Line2D((0, width), (h, h), lw=3, color='black')
                    self.draw.add_line(line)

                else:
                    line = plt.Line2D((0, width), (h, h), lw=1, color='dimgrey')
                    self.draw.add_line(line)

        # draw the center marker
        rectangle = plt.Rectangle((self.environment.center[0]-0.2, self.environment.center[1]-0.2), .4, .4, fc='r')
        plt.gca().add_patch(rectangle)

    def draw_cities(self):
        """
        :param cities : this is a list based off the grid
        :return       : N/A
        """

        for city in self.environment.cities:
            # plot all of the cities (as dots)
            circle = plt.Circle((city[0], city[1]), radius=0.1, fc='lightskyblue', ec='black')
            self.draw.add_patch(circle)

    def draw_split(self, points):

        for point in points:
            line = plt.Line2D((self.environment.center[0], point[0]), (self.environment.center[1], point[1]), lw=3,
                              color='green')
            self.draw.add_line(line)

    def draw_path(self, path, color):
        """
        :param path : this is list calculated by a tsp solver
        :return     : path length
        """

        # this will be calculated iteratively
        path_length = 0

        # these will control the logic of the color gradient of the arrows
        # currently there are 10 shades of red
        count = 0
        back = False

        for v in range(len(path) - 1):
            x = path[v][0]
            y = path[v][1]
            dx = path[v + 1][0] - x
            dy = path[v + 1][1] - y

            # iteratively calculate path length
            path_length += math.hypot(dx, dy)

            # create an arrow
            arrow = plt.arrow(x, y, dx, dy, width=0.045, facecolor=color, edgecolor='black', zorder=10)
            self.draw.add_patch(arrow)

        return path_length

    def show_fig(self):

        # this will plot everything
        plt.axis('scaled')
        plt.title(label=self.title)
        plt.grid(b=True)
        plt.show()

        # close the figure so other figures can be created
        plt.close(self.env_fig)


def ant_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm
    """

    # ant algorithm configuration
    max_it = 100
    num_ants = 10
    decay = 0.1
    c_heur = 2.5
    c_local_phero = 0.1
    c_greed = 0.9

    best = ant.search(cities, max_it, num_ants, decay, c_heur, c_local_phero, c_greed)

    ant_route = [cities[i] for i in best['vector']]

    return ant_route

def genetic_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm
    """
    citylist = []

    for city in cities:
        citylist.append(gene.City(x=city[0], y=city[1]))

    # geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
    node_path = gene.geneticAlgorithm(population=citylist, popSize=100, eliteSize=20, mutationRate=0.01,
                                      generations=500)

    path = []
    # the path is actually made up of "Node" objects
    # so extract the information into a list
    for node in node_path:
        path.append((node.x, node.y))

    return path

def python_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm

    * this uses the python tsp package - exact algorithm
    """
    path = tsp.tsp(cities)[1]

    python_route = [cities[i] for i in path]

    return python_route

def get_uav_routes(environment, number_of_uavs):
    # these should correspond for each uav
    rotated_points = []
    angles = []

    # this will hold the points for each uav
    uav_routes = {}

    for num in range(number_of_uavs):

        # create a rotation matrix to find the initial paths of all of the uavs
        # increase the angle each iteration
        angle = 360 / number_of_uavs
        theta = np.radians(num * angle)

        # this will hold all of the angles that split up the environment
        angles.append(theta)
        c, s = np.cos(theta), np.sin(theta)

        # create a rotation matrix
        R = np.array(((c, -s), (s, c)))

        # this will calculate the new point for each drone's boundary
        # this is only for visualization purposes
        vec = np.array([(environment.width/2)+np.hypot(environment.width/2, environment.height/2), environment.height/2]) - environment.center
        rot_point = R @ vec
        rotated_point = rot_point + environment.center
        rotated_points.append(list(rotated_point))

    # append 2*pi to include the points belonging to the last drone
    angles.append(np.radians(360))
    print(f'angles: {angles}')

    # calculate the angle of each point and assign them to a respective drone
    for city in environment.cities:

        city_angle = environment.find_angle_from_center(city)
        print('city:', city_angle)

        if city_angle != 'center':

            for i, angle in enumerate(angles):

                if city_angle <= angle != 0:

                    if f'{i}' not in uav_routes.keys():
                        uav_routes.update({f'{i}': [city]})

                    else:
                        uav_routes[f'{i}'].append(city)

                    break

    return uav_routes, rotated_points


if __name__ == "__main__":
    # defining the dimensions of the environment
    m = 5  # width
    n = 5  # height
    k = 1  # number of uavs

    land = Environment(width=m, height=n)
    cities = land.get_cities()

    picasso = Draw(environment=land)
    picasso.draw_environment(title='Python TSP Algorithm Path')
    picasso.draw_cities()

    # this will split up the uav routes
    uav_routes, split = get_uav_routes(environment=land, number_of_uavs=k)

    for key in uav_routes:

        path = uav_routes[key]

        # make the center point the starting point
        path.insert(0, land.center)

        print(path)

        # run tsp on each sub path
        path = python_tsp(path)

        # have the uav travel back to the center path
        path.append(path[0])
        print(path)
        path_length = picasso.draw_path(path, np.random.rand(3,))

    picasso.draw_split(split)

    picasso.show_fig()
