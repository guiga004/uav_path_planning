"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import math
import numpy as np
from tsp_algorithms.tsp_algorithms import exact_tsp

def get_uav_paths(environment, number_of_uavs):
    """
    :param environment      : an instance of the Environment class
    :param number_of_uavs   : the number of uavs (k)
    :return                 : a dictionary containing all of the routes, and the splitting points of the environment
    """
    # these should correspond for each uav
    rotated_points = []
    angles = []

    # this will hold the points that each uav will visit
    uav_paths = {}

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

    optimal_split = round(len(environment.cities) / (len(angles)-1))

    # sort the cities by their angle
    for city in environment.cities:
        city.append(environment.find_angle_from_center(city))

    environment.cities = sorted(environment.cities, key=lambda e: e[2], reverse=False)

    # calculate the angle of each point and assign them to a respective drone
    for city in environment.cities:

        city_angle = city[2]

        # don't care about the center since we are starting at the center
        if city_angle != 999:

            for i, angle in enumerate(angles):

                # assign points by iterating counter-clockwise through environment
                if city_angle < angle != 0:

                    # create a key in the dictionary if not yet created+
                    if f'{i}' not in uav_paths.keys():
                        uav_paths.update({f'{i}': [city[:2]]})

                    else:

                        if len(uav_paths[f'{i}']) < optimal_split or angle == angles[-1]:
                            uav_paths[f'{i}'].append(city[:2])

                        else:

                            if f'{i+1}' not in uav_paths.keys():
                                uav_paths.update({f'{i+1}': [city[:2]]})
                            else:
                                uav_paths[f'{i+1}'].append(city[:2])

                    break

    for key in uav_paths:
        uav_paths[key].insert(0, environment.center)    # make the center point the starting point
        uav_paths[key] = exact_tsp(uav_paths[key])      # run tsp on each route
        uav_paths[key].append(uav_paths[key][0])        # have each uav travel back to the center point

    return uav_paths, rotated_points

def get_path_length(path):
    """
    :param path : a list of points
    :return     : the path length
    """
    path_length = 0

    for v in range(len(path) - 1):
        x = path[v][0]
        y = path[v][1]
        dx = path[v + 1][0] - x
        dy = path[v + 1][1] - y

        path_length += math.hypot(dx, dy)

    return path_length

def calculate_route_data(uav_paths):
    """
    :param uav_paths   : a dictionary containing all UAV routes
    :return:           : a dictionary containing stats for the UAV with the max path length
    """

    # these variables will store the max path and the UAV associated with it
    max_uav = None
    max_path = 0

    for uav, path in uav_paths.items():

        path_length = get_path_length(path)

        if path_length > max_path:
            max_uav = uav
            max_path = path_length

    return max_path
