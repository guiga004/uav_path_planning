"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import math
from tools.environment import Environment
import testing_grounds as tg
import tools.guiga_algorithms as gumo
import matplotlib.pyplot as plt
from tsp_algorithms.tsp_algorithms import exact_tsp
from tools.draw import Draw

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


def uav_can_cover(path_length, B_min, uA_max, e):
    """
    :param path_length: the max path length calculated from each drone
    :param B_min:       the energy depletion rate for the UAV
    :param uA_max:      the max speed of the UAV
    :param e:           the max energy of a UAV
    :return:            boolean: true if the uav can cover this partition size
    """
    return (path_length * B_min) / uA_max <= e


'''
Adapted from:
ALGORITHM 2 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
'''


def partition_feasibility_check(e, uA_max, B_min, environment, n, m=1):
    """
    :param e            : maximum energy of UAV
    :param uA_max       : maximum speed of UAV
    :param B_min        : energy depletion rate of UAV
    :param environment  : an instance of an Environment class (small sub partition)
    :param n            : number of UAVs
    :param m            : number of UGVs
    :return             : False if not feasible, path data if feasible
    """

    # this will split up the uav routes
    uav_paths, split = gumo.get_uav_paths(environment=environment, number_of_uavs=n)
    max_path = gumo.calculate_route_data(uav_paths)

    # determine if the maximum path length is feasible
    if uav_can_cover(max_path, B_min, uA_max, e):
        return True, max_path, (uav_paths, split)
    else:
        return False, None


def find_feasible_partitions(x_bar, y_bar, specs):
    # calculate all possible combinations of partition sizes
    partition_sizes = []
    feasible = []

    for y in range(1, y_bar + 1):

        for x in range(1, x_bar + 1):

            if y == 1 and x == 1:
                continue

            partition_sizes.append([x, y])

    for partition_size in partition_sizes:

        small_x = partition_size[0]
        small_y = partition_size[1]

        # create a new environment class based on the partition size
        environment = Environment(width=small_x, height=small_y)

        # check to see if the partition is feasible
        max_path = partition_feasibility_check(specs['e'], specs['uA_max'], specs['B-'], environment, specs['n'])

        if max_path[0]:
            feasible.append([environment, max_path[1], max_path[2]])

    return feasible


'''
Adapted from:
ALGORITHM 3 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
Persistent surveillance with energy-constrained uavs and mobile charging stations.
arXiv preprint arXiv:1908.05727,2019.
'''


def uav_ugv_trajectory_generation(x_bar, y_bar, specs=None, draw=True, draw_ugv=True, draw_uav=True):
    picasso = None
    feasible = find_feasible_partitions(x_bar, y_bar, specs)

    # these will get updated iteratively
    min_env = None
    min_partitions = None
    min_drones = None
    min_time = math.inf

    # iterate through the feasible partitions and find the one with the lease time
    for partition in feasible:

        a1 = partition[0].width
        a2 = partition[0].height

        partitions = partitioning(a1, a2, x_bar, y_bar)
        partition_midpoints = []

        # calculate all of the midpoints of the partitions
        for part in partitions:
            bottom_corner = (part[0][0], part[1][0])
            width_x = part[0][1] - part[0][0]
            height_y = part[1][1] - part[1][0]
            partition_midpoints.append((bottom_corner[0] + width_x / 2, bottom_corner[1] + height_y / 2))

        ugv_length = gumo.get_path_length(partition_midpoints)

        ugv_time = ugv_length / specs['uG_max']
        uav_time = partition[1] / specs['uA_max']
        uav_ugv_time = ugv_time + uav_time

        print(f'\nenvironment size : {x_bar}x{y_bar}')
        print(f'partition size   : {a1}x{a2}')
        print(f'ugv time         : {ugv_time}')
        print(f'uav time         : {uav_time}')
        print(f'total time       : {uav_ugv_time}\n')

        if uav_ugv_time < min_time:
            min_env = partition[0]
            min_drones = partition[2]
            min_partitions = partitions
            min_midpoints = partition_midpoints
            min_time = uav_ugv_time

    print('*** WINNER ****')
    print(f'environment size : {x_bar}x{y_bar}')
    print(f"number of UAVs   : {specs['n']}")
    print(f'partition size   : {min_env.width}x{min_env.height}')
    print(f'total time       : {min_time}')

    if draw:
        picasso = Draw()

        colors = []
        for _ in range(len(min_partitions)):
            colors.append(tg.generate_new_color(colors, pastel_factor=0.9))

    for partition in min_partitions:

        edge_color = 'black'
        order = partition[2]
        opacity = partition[3]
        line_width = 3

        bottom_corner = (partition[0][0], partition[1][0])
        width_x = partition[0][1] - partition[0][0]
        height_y = partition[1][1] - partition[1][0]

        if draw:
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

    if draw_ugv:
        min_midpoints = exact_tsp(min_midpoints)  # run tsp on the ugv route
        min_midpoints.append(min_midpoints[0])  # have the ugv complete the route
        picasso.draw_path(min_midpoints, 'white', width=0.15)

    if draw_uav:

        for i, key in enumerate(min_drones[0]):
            path = min_drones[0][key]
            picasso.draw_path(path=path, color='black')

    return picasso
