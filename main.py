"""
author : Mohammed Guiga
email  : guiga004@umn.edu
"""
import time
from tools.environment import Environment
from tools.draw import Draw
import tools.guiga_algorithms as gumo

if __name__ == "__main__":

    m = 10  # width
    n = 10  # height
    k = 3  # number of uavs

    land = Environment(width=m, length=n)

    picasso = Draw(environment=land)
    picasso.draw_environment(title='Path Planning with Multiple Drones')
    picasso.draw_cities()

    # only run the following code if number of UAVs is greater than 0
    if k > 0:

        start_time = time.time()

        # this will split up the uav routes
        uav_paths, split = gumo.get_uav_paths(environment=land, number_of_uavs=k)
        print(gumo.calculate_route_data(uav_paths))

        colors = ['blue', 'maroon', 'yellow', 'gray', 'green']

        for i, key in enumerate(uav_paths):

            path = uav_paths[key]
            picasso.draw_path(path=path, color=colors[i])

        print("\n--- run time: %s seconds ---" % (time.time() - start_time))

        # this will visualize how the environment was split
        picasso.draw_split(split)

    picasso.show_fig()
