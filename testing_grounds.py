import random
from draw import Draw
import paper_algorithms as pa
import matplotlib.pyplot as plt
from environment import Environment

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


if __name__ == "__main__":
    '''
    The environment is assumed to have dimensions xmax = 1584 and ymax = 1056, which
    imply ¯x = 48 and ¯y = 32, as depicted in Fig. 4. We assume
    the UGV transport rate uG max = 5, and the charging and depletion rates 
    for the UAVs are β+ = β− = 0.5.
    '''

    hardware_specs = \
        {
            'uG_max': 5,   # the max speed of a UGV
            'uA_max': 1,     # the max speed of a UAV
            'd': 2,          # square detection footprint a dxd square that the UAV can detect
            'e': 5,          # maximum energy of UAV
            'B+': 0.5,       # energy increase rate when charging
            'B-': 0.5,       # energy decrease rate when flying
            'n': 3           # number of UAVs
        }

    pic = pa.uav_ugv_trajectory_generation(x_bar=10, y_bar=10, specs=hardware_specs)

    pic.show_fig()


