"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import time
from environment import Environment
from draw import Draw
from tsp_algorithms import exact_tsp
import guiga_algorithms as gumo

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
        uav_routes, split = gumo.get_uav_routes(environment=land, number_of_uavs=k)
        gumo.get_route_data(uav_routes)

        colors = ['blue', 'maroon', 'yellow', 'gray', 'green']

        for i, key in enumerate(uav_routes):

            path = uav_routes[key]
            picasso.draw_path(path=path, color=colors[i])

        print("--- %s seconds ---" % (time.time() - start_time))

        # this will visualize how the environment was split
        picasso.draw_split(split)

    picasso.show_fig()