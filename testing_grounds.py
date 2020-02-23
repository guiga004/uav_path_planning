import random
import math
from draw import Draw
from tsp_algorithms import exact_tsp
import matplotlib.pyplot as plt


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
            P.append([[(k1-1)*a1, k1*a1], [(k2-1)*a2, k2*a2], 9])

    for k in range(1, math.ceil(y/a2)):
        i = i+1
        P.append([[x-a1, x], [(k-1)*a2, k*a2], 6])

    for k in range(1, math.ceil(x/a1)):
        i = i+1
        P.append([[(k-1)*a1, k*a1], [y-a2, y], 3])

    i = i+1
    P.append([[x-a1, x], [y-a2, y], 0])

    return P


def draw_everything(a1, a2, x, y, hardware_specs=None):

    picasso = Draw()
    partition_midpoints = []

    partitions = partitioning(a1, a2, x, y)

    colors = []
    for i in range(len(partitions)):
        colors.append(generate_new_color(colors, pastel_factor=0.9))

    for partition in partitions:

        bottom_corner = (partition[0][0], partition[1][0])
        width_x = partition[0][1] - partition[0][0]
        height_y = partition[1][1] - partition[1][0]
        partition_midpoints.append((bottom_corner[0] + width_x/2, bottom_corner[1] + height_y/2))


        edge_color = 'black'
        order = partition[2]
        line_width = 3

        rectangle = plt.Rectangle\
            (
                xy=bottom_corner,
                width=width_x,
                height=height_y,
                fill=True,
                color=colors.pop(),
                ec=edge_color,
                lw=line_width,
                zorder=order
            )
        picasso.draw.add_patch(rectangle)

    return picasso, partition_midpoints


if __name__ == "__main__":

    big_x = 11
    big_y = 9
    # small_x = 3
    # small_y = 3

    # print out all possible combinations of partition sizes

    partition_sizes = []

    for y in range(3, 4):

        for x in range(3, 4):
            partition_sizes.append([x, y])

    for partition_size in partition_sizes:

        # print(partition_size)

        small_x = partition_size[0]
        small_y = partition_size[0]

        test, ugv_points = draw_everything(small_x, small_y, big_x, big_y)

        # run tsp for the ugv route
        ugv_path = exact_tsp(ugv_points)

        # have the ugv

        ugv_path.append(ugv_path[0])

        total_path_length = test.draw_path(path=ugv_path, color='white')

        test.show_fig()



