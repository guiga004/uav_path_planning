"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import math

'''
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

    for k1 in range(1, math.ceil(x/a1)):
        for k2 in range(1, math.ceil(y/a2)):
            P.append([[(k1-1)*a1, k1*a1], [(k2-1)*a2, k2*a2], 9, 0.8])

    for k in range(1, math.ceil(y/a2)):
        P.append([[x-a1, x], [(k-1)*a2, k*a2], 6, 1])

    for k in range(1, math.ceil(x/a1)):
        P.append([[(k-1)*a1, k*a1], [y-a2, y], 3, 0.8])

    P.append([[x-a1, x], [y-a2, y], 0, 1])

    return P

def get_vehicle_velocity(uA_max, uG_max, v, vnext, is_uav=True, is_flying=True, is_moving=False):
    """
    :param is_uav:      boolean, true: vehicle is a UAV
    :param is_flying:   boolean, true: UAV is flying
    :param is_moving:   boolean, true: UGV is moving
    :param uA_max:      max speed of UAV
    :param uG_max:      max speed of UGV
    :param v:           current node
    :param vnext:       next node
    :return:            speed of vehicle
    """
    if is_flying and is_uav:
        x = v[0]
        y = v[1]
        dx = vnext[0] - x
        dy = vnext[1] - y
        return uA_max * math.hypot(dx, dy)

    else:

        if is_moving:
            x = v[0]
            y = v[1]
            dx = vnext[0] - x
            dy = vnext[1] - y
            return uG_max * math.hypot(dx, dy)

        else:
            return 0


def uav_can_cover(path_length, B_min, uA_max, e):
    """
    :param path_length: the max path length calculated from each drone
    :param B_min:       the energy depletion rate for the UAV
    :param uA_max:      the max speed of the UAV
    :param e:           the max energy of a UAV
    :return:            boolean: true if the uav can cover this partition size
    """
    return (path_length*B_min)/uA_max <= e


'''
ALGORITHM 2 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
Persistent surveillance with energy-constrained uavs and mobile charging stations.
arXiv preprint arXiv:1908.05727,2019.
'''
def partition_feasibility_check(e, uA_max, uG_max, B_min, a1, a2, n, m=1):
    """
    :param e:       maximum energy of UAV
    :param uA_max:  maximum speed of UAV
    :param uG_max:  maximum speed of UGV
    :param B_min:   energy depletion rate of UAV
    :param a1:      width of sub partition
    :param a2:      height of sub partition
    :param n:       number of UAVs
    :param m:       number of UGVs
    :return:
    """
    for k in range(1, n/m):

        v = None
        v_next = None

        # find all vertices that the UAV will cover

        # iterate through all vertices and calculate UAV velocity
        for j in range():
            get_vehicle_velocity(uA_max=uA_max, uG_max=uG_max, v=v, vnext=v_next)

    # find the maximum path length
    max_path_length = None

    # determine if the maximum path length is feasible
    if uav_can_cover(max_path_length, B_min, uA_max, e):
        return "some stuff, probably a list with some relevant info"
    else:
        return False

'''
ALGORITHM 3 from  S.Seyedi, Y.Yazicioglu, and D.Aksaray.    
Persistent surveillance with energy-constrained uavs and mobile charging stations.
arXiv preprint arXiv:1908.05727,2019.
'''
# def uav_ugv_trajectory_generation(a1, a2, x, y, specs=None, draw=True):
#
#     picasso = None
#     partitions = pa.partitioning(a1, a2, x, y)
#     partition_midpoints = []
#
#     if draw:
#         picasso = Draw()
#
#
#         colors = []
#         for i in range(len(partitions)):
#             colors.append(generate_new_color(colors, pastel_factor=0.9))
#
#     for partition in partitions:
#
#         bottom_corner = (partition[0][0], partition[1][0])
#         width_x = partition[0][1] - partition[0][0]
#         height_y = partition[1][1] - partition[1][0]
#         partition_midpoints.append((bottom_corner[0] + width_x/2, bottom_corner[1] + height_y/2))
#
#         edge_color = 'black'
#         order = partition[2]
#         opacity = partition[3]
#         line_width = 3
#
#         if draw:
#             rectangle = plt.Rectangle\
#                 (
#                     xy=bottom_corner,
#                     width=width_x,
#                     height=height_y,
#                     fill=True,
#                     color=colors.pop(),
#                     ec=edge_color,
#                     lw=line_width,
#                     zorder=order,
#                     alpha=opacity,
#                 )
#             picasso.draw.add_patch(rectangle)
#
#
#     return picasso, partition_midpoints
