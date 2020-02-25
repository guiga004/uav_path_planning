"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import time
from environment import Environment
from draw import Draw
from tsp_algorithms import exact_tsp
from guiga_algorithms import get_uav_routes

if __name__ == "__main__":

    m = 2  # width
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

        colors = ['blue', 'maroon', 'yellow', 'gray', 'green']

        for i, key in enumerate(uav_routes):

            path = uav_routes[key]

            # make the center point the starting point
            path.insert(0, land.center)

            # run tsp on each sub path
            path = exact_tsp(path)

            # have each uav travel back to the center point
            path.append(path[0])

            total_path_length += picasso.draw_path(path=path, color=colors[i])

        print("--- %s seconds ---" % (time.time() - start_time))
        print("Total Length", total_path_length)

        # this will visualize how the environment was split
        picasso.draw_split(split)

    picasso.show_fig()