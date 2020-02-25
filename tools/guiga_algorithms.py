"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import numpy as np
import time
from environment import Environment
from draw import Draw
from tsp_algorithms import exact_tsp


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

    optimal_split = round(len(environment.cities) / (len(angles)-1))

    print(f'angles: {angles}')
    print(f'cities: {environment.cities}')
    print(f'optimal_split: {optimal_split}')

    # sort the cities by their angle
    for city in environment.cities:
        city.append(environment.find_angle_from_center(city))

    print(f'cities: {environment.cities}')

    environment.cities = sorted(environment.cities, key=lambda e: e[2], reverse=False)

    print(f'cities: {environment.cities}')

    # calculate the angle of each point and assign them to a respective drone
    for city in environment.cities:

        city_angle = city[2]

        # don't care about the center since we are starting at the center
        if city_angle != 'center':

            for i, angle in enumerate(angles):

                # assign points by iterating counter-clockwise through environment
                if city_angle < angle != 0:

                    # create a key in the dictionary if not yet created+
                    if f'{i}' not in uav_routes.keys():
                        uav_routes.update({f'{i}': [city[:2]]})

                    else:

                        if len(uav_routes[f'{i}']) < optimal_split or angle == angles[-1]:
                            uav_routes[f'{i}'].append(city[:2])

                        else:

                            if f'{i+1}' not in uav_routes.keys():
                                uav_routes.update({f'{i+1}': [city[:2]]})
                            else:
                                uav_routes[f'{i+1}'].append(city[:2])


                    break

    return uav_routes, rotated_points

