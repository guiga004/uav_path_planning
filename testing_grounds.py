import math
from draw import Draw
from tsp_algorithms import exact_tsp
import matplotlib.pyplot as plt

def partitioning(a1, a2, x, y):
    '''
    :param a1: width of sub partition
    :param a2: height of sub partition
    :param x: width of environment
    :param y: height of environment
    :return:
    '''

    P = []
    i = 0

    for k1 in range(1, math.ceil(x/a1)):
        for k2 in range(1, math.ceil(y/a2)):
            i = i+1
            P.append([[(k1-1)*a1, k1*a1], [(k2-1)*a2, k2*a2]])

    for k in range(1, math.ceil(y/a2)):
        i = i+1
        P.append([[x-a1, x], [(k-1)*a2, k*a2]])

    for k in range(1, math.ceil(x/a1)):
        i = i+1
        P.append([[(k-1)*a1, k*a1], [y-a2, y]])

    i = i+1
    P.append([[x-a1, x], [y-a2, y]])

    return P



def draw_everything(a1, a2, x, y, hardware_specs=None):

    picasso = Draw()
    partition_midpoints = []

    partitions = partitioning(a1, a2, x, y)

    for partition in partitions:
        bottom_corner = (partition[0][0], partition[1][0])
        width_x = partition[0][1] - partition[0][0]
        height_y = partition[1][1] - partition[1][0]
        partition_midpoints.append((bottom_corner[0] + width_x/2, bottom_corner[1] + height_y/2))

        rectangle = plt.Rectangle(xy=bottom_corner, width=width_x, height=height_y, fill=False, color='white', ec='black', lw=4)
        picasso.draw.add_patch(rectangle)

    return picasso, partition_midpoints


if __name__ == "__main__":

    big_x = 11
    big_y = 9
    small_x = 3
    small_y = 3

    test, ugv_points = draw_everything(big_x, big_y, small_x, small_y)

    # run tsp for the ugv route
    ugv_path = exact_tsp(ugv_points)

    # have the ugv

    ugv_path.append(ugv_path[0])

    total_path_length = test.draw_path(path=ugv_path, color='red')


    test.show_fig()

    # print out all possible combinations of partition sizes

    for y in range(1, big_y):

        for x in range(1, big_x):

            print(f'partition size: {x} x {y}')