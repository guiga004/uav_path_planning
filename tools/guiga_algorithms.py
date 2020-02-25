import numpy as np

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

