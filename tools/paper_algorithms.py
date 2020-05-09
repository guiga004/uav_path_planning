"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import math
import random
from tools.environment import Environment
import tools.guiga_algorithms as gumo
import matplotlib.pyplot as plt
from tsp_algorithms.tsp_algorithms import exact_tsp
from tools.draw import Draw


def get_random_color(pastel_factor=0.5):
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1, c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color, c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color

'''
Taken from:
ALGORITHM 1 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.
Persistent surveillance with energy-constrained uavs and mobile charging stations.
arXiv preprint arXiv:1908.05727,2019.
'''


def partitioning(a1, a2, x, y):
    """
    :param a1: width of sub partition
    :param a2: height of sub partition
    :param x: width of environment
    :param y: height of environment
    :return: P, list containing bounds for sub partitions the numbers at the end are for plotting purposes
    """

    P = []

    for k1 in range(1, math.ceil(x / a1)):
        for k2 in range(1, math.ceil(y / a2)):
            P.append([[(k1 - 1) * a1, k1 * a1], [(k2 - 1) * a2, k2 * a2], 9, 0.8])

    for k in range(1, math.ceil(y / a2)):
        P.append([[x - a1, x], [(k - 1) * a2, k * a2], 6, 1])

    for k in range(1, math.ceil(x / a1)):
        P.append([[(k - 1) * a1, k * a1], [y - a2, y], 3, 0.8])

    P.append([[x - a1, x], [y - a2, y], 0, 1])

    return P


def uav_can_cover(path_length, b_min, ua_max, e):
    """
    :param path_length: the max path length calculated from each drone
    :param b_min:       the energy depletion rate for the UAV
    :param ua_max:      the max speed of the UAV
    :param e:           the max energy of a UAV
    :return:            boolean: true if the uav can cover this partition size
    """

    return e - ((path_length * b_min) / ua_max) > 0


'''
Adapted from:
ALGORITHM 2 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
'''


def partition_feasibility_check(e, ua_max, b_min, environment, n, m=1):
    """
    :param e            : maximum energy of UAV
    :param ua_max       : maximum speed of UAV
    :param b_min        : energy depletion rate of UAV
    :param environment  : an instance of an Environment class (small sub partition)
    :param n            : number of UAVs
    :param m            : number of UGVs
    :return             : False if not feasible, path data if feasible
    """

    # this will calculate the maximum path that a uav will travel
    uav_paths, split = gumo.get_uav_paths(environment=environment, number_of_uavs=n)
    max_path = gumo.calculate_route_data(uav_paths)

    # determine if the maximum path length is feasible
    if uav_can_cover(max_path, b_min, ua_max, e):
        return True, max_path, (uav_paths, split)
    else:
        return False, None


def find_feasible_partitions(x_bar, y_bar, specs):
    # calculate all possible combinations of partition sizes
    partition_sizes = []
    feasible = []

    for y in range(1, y_bar + 1):

        for x in range(1, x_bar + 1):

            if x * y >= 100 or x * y == 1:
                continue

            # create a new environment class based on the partition size
            environment = Environment(width=x, length=y)

            # check to see if the partition is feasible
            max_path = partition_feasibility_check(specs['e'], specs['uA_max'], specs['B-'], environment, specs['n'])

            if max_path[0]:
                feasible.append([environment, max_path[1], max_path[2]])

    return feasible


def find_min_partitions(x_bar, y_bar, specs, obstacles):
    feasible = find_feasible_partitions(x_bar, y_bar, specs)

    # these will get updated iteratively
    min_env = None
    min_partitions = None
    min_drones = None
    min_time = math.inf

    # iterate through the feasible partitions and find the one with the least time
    for partition in feasible:

        a1 = partition[0].width
        a2 = partition[0].length

        partitions = partitioning(a1, a2, x_bar, y_bar)
        partition_midpoints = []

        # calculate all of the midpoints of the partitions
        for part in partitions:
            bottom_corner = (part[0][0], part[1][0])
            width_x = part[0][1] - part[0][0]
            height_y = part[1][1] - part[1][0]
            point = [bottom_corner[0] + width_x / 2, bottom_corner[1] + height_y / 2]

            partition_midpoints.append(point)

        # run TSP on every UGV path possibility
        ugv_path = exact_tsp(partition_midpoints)
        ugv_path.append(ugv_path[0])
        ugv_length = gumo.get_path_length(ugv_path)

        ugv_length = gumo.get_path_length(partition_midpoints)

        ugv_time = ugv_length / specs['uG_max']
        uav_time = (partition[1] / specs['uA_max']) * len(partitions)
        uav_ugv_time = ugv_time + uav_time

        print(f'\npartition size   : {a1}x{a2}')
        print(f'ugv time         : {ugv_time}')
        print(f'uav time         : {uav_time}')
        print(f'total time       : {uav_ugv_time}\n')

        if uav_ugv_time < min_time:
            min_env = partition[0]
            min_drones = partition[2]
            min_partitions = partitions
            min_ugv = partition_midpoints
            min_midpoints = ugv_path
            min_time = uav_ugv_time

    print('*** WINNER ****')
    print(f"number of UAVs   : {specs['n']}")
    print(f'partition size   : {min_env.width}x{min_env.length}')
    print(f'total time       : {min_time}')

    return min_env, min_drones, min_partitions, min_ugv, min_midpoints, min_time


'''
Adapted from:
ALGORITHM 3 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
Persistent surveillance with energy-constrained uavs and mobile charging stations.
arXiv preprint arXiv:1908.05727,2019.
'''


def uav_ugv_trajectory_generation(x_bar, y_bar, specs=None, obstacles=[]):

    minima = find_min_partitions(x_bar, y_bar, specs, obstacles)
    min_drones = minima[1]
    min_partitions = minima[2]
    min_midpoints = minima[4]

    picasso = Draw()
    picasso.title = "2D Top View"

    colors = []
    for _ in range(len(min_partitions)):
        colors.append(generate_new_color(colors, pastel_factor=0.9))

    first_color = colors[0]

    for partition in min_partitions:
        edge_color = 'black'
        order = partition[2]
        opacity = partition[3]
        line_width = 3

        bottom_corner = (partition[0][0], partition[1][0])
        width_x = partition[0][1] - partition[0][0]
        height_y = partition[1][1] - partition[1][0]

        rectangle = plt.Rectangle \
                (
                xy=bottom_corner,
                width=width_x,
                height=height_y,
                fill=True,
                color=colors.pop(),
                ec=edge_color,
                lw=line_width,
                zorder=order,
                alpha=opacity,
            )
        picasso.draw.add_patch(rectangle)

    picasso.draw_path(min_midpoints, 'white', width=0.15)

    uav_colors = [first_color]

    for _ in range(len(min_drones[0]) + 1):
        uav_colors.append(generate_new_color(colors, pastel_factor=0.3))

    for i, key in enumerate(min_drones[0]):
        path = min_drones[0][key]
        picasso.draw_path(path=path, color=uav_colors[i + 1])

    if obstacles:

        for obstacle in obstacles:
            circle = plt.Circle(obstacle[0], obstacle[1], facecolor='black', zorder=99)
            picasso.draw.add_patch(circle)

    return picasso
