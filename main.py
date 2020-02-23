"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""

import numpy as np
import time
import copy
from environment import Environment
from draw import Draw
from tsp_algorithms import ant_tsp, genetic_tsp, exact_tsp


def get_uav_routes(environment, number_of_uavs):
    """
    :param environment      : an instance of the Environment class
    :param number_of_uavs   : the number of uavs (k)
    :return                 : a dictionary containing all of the routes, and the splitting points of the environment
    """
    # these should correspond for each uav
    rotated_points = []
    angles = []

    # this will hold the points that each uav will visit
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

    # this will allow a more fair split
    optimal_split = round(len(environment.cities) / (len(angles)-1))

    # sort the cities by their angle
    for city in environment.cities:
        angle = environment.find_angle_from_center(city)

        if angle != 'center':
            city.append(angle)

        else:
            city.append(999)

    print(environment.cities)

    environment.cities = sorted(environment.cities, key=lambda e: e[2], reverse=False)

    for city in environment.cities:

        # the city angle is now stored with each city, so grab it
        city_angle = city[2]

        # don't care about the center since we are starting at the center
        if city_angle != 999:

            for i, angle in enumerate(angles):

                # assign points by iterating counter-clockwise through environment
                if city_angle <= angle != 0:

                    # create a key in the dictionary if not yet created
                    if f'{i}' not in uav_routes.keys():
                        uav_routes.update({f'{i}': [city[:2]]})

                    else:
                        uav_routes[f'{i}'].append(city[:2])

                    break

    return uav_routes, rotated_points


if __name__ == "__main__":
    m = 3  # width
    n = 3  # height
    k = 3  # number of uavs

    land = Environment(width=m, height=n)
    cities = land.get_cities

    picasso = Draw(environment=land)
    picasso.draw_environment(title='Path Planning with Multiple Drones')
    picasso.draw_cities()

    # only run the following code if number of UAVs is greater than 0
    if k > 0:

        total_path_length = 0
        start_time = time.time()

        # this will split up the uav routes
        uav_routes, split = get_uav_routes(environment=land, number_of_uavs=k)

        colors = ['blue', 'maroon', 'yellow', 'gray', 'green', 'pink']

        for i, key in enumerate(uav_routes):

            path = uav_routes[key]

            # make the center point the starting point
            path.insert(0, land.center)

            # run tsp on each sub path
            path = exact_tsp(path)

            # have each uav travel back to the center point
            path.append(path[0])

            total_path_length += picasso.draw_path(path=path, color=colors[i%len(colors)])

        print("--- %s seconds ---" % (time.time() - start_time))
        print("Total Length", total_path_length)

        # this will visualize how the environment was split
        picasso.draw_split(split)

    picasso.show_fig()
