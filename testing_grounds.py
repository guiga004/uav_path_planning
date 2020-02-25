import random
from draw import Draw
from tsp_algorithms import exact_tsp
import paper_algorithms as pa
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


def uav_ugv_trajectory_generation(a1, a2, x, y, specs=None, draw=True):

    picasso = None
    partitions = pa.partitioning(a1, a2, x, y)
    partition_midpoints = []

    if draw:
        picasso = Draw()


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
        opacity = partition[3]
        line_width = 3

        if draw:
            rectangle = plt.Rectangle\
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


    return picasso, partition_midpoints


if __name__ == "__main__":

    '''
    The environment is assumed to have dimensions xmax = 1584 and ymax = 1056, which
    imply ¯x = 48 and ¯y = 32, as depicted in Fig. 4. We assume
    the UGV transport rate uG max = 5, and the charging and depletion rates 
    for the UAVs are β+ = β− = 0.5.
    '''

    # this dictionary of specifications will be used to find the optimal partition
    hardware_specs = \
        {
            'x_max': 165,   # this will be normalized by the square detection footprint (d)
            'y_max': 165,   # the y dimensioned length of the environment
            'uG_max': 5,    # the max speed of a UGV
            'uA_max': 5,    # the max speed of a UAV
            'd': 33,        # square detection footprint a dxd square that the UAV can detect
            'e': 100,       # maximum energy of UAV
            'B+': 0.5,      # energy increase rate when charging
            'B-': 0.5,      # energy decrease rate when flying
        }

    x_bar = hardware_specs['x_max'] // hardware_specs['d']
    y_bar = hardware_specs['y_max'] // hardware_specs['d']

    # print out all possible combinations of partition sizes

    partition_sizes = []

    for y in range(1, y_bar+1):

        for x in range(1, x_bar+1):
            partition_sizes.append([x, y])

    for partition_size in partition_sizes:

        # print(partition_size)

        small_x = partition_size[0]
        small_y = partition_size[1]

        test, ugv_points = uav_ugv_trajectory_generation(small_x, small_y, x_bar, y_bar, specs=hardware_specs, draw=False)

        # run tsp for the ugv route
        ugv_path = exact_tsp(ugv_points)

        # have the ugv

        ugv_path.append(ugv_path[0])

        total_path_length = Draw.draw_path(None, path=ugv_path, color='white', draw=False)

        print(f'size: {small_x, small_y} ; path length: {total_path_length}')
