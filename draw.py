import math
import matplotlib.pyplot as plt

class Draw:
    """
    This class contains methods for environment visualization
    """

    def __init__(self, environment=None):

        self.env_fig = plt.figure()
        self.draw = self.env_fig.gca()
        self.title = ''

        self.environment = environment

    def draw_environment(self, title):
        """
        :param title        : title of the figure
        :return             : N/A
        """
        self.title = title

        width = self.environment.width
        height = self.environment.height

        for w in range(width + 1):


            if w == 0 or w == width:
                line = plt.Line2D((w, w), (0, height), lw=3, color='black')
                self.draw.add_line(line)

            else:
                line = plt.Line2D((w, w), (0, height), lw=1, color='dimgrey')
                self.draw.add_line(line)

            for h in range(height + 1):

                if h == 0 or h == height:
                    line = plt.Line2D((0, width), (h, h), lw=3, color='black')
                    self.draw.add_line(line)

                else:
                    line = plt.Line2D((0, width), (h, h), lw=1, color='dimgrey')

                    self.draw.add_line(line)

        # draw the center marker
        rectangle = plt.Rectangle((self.environment.center[0]-0.2, self.environment.center[1]-0.2), .4, .4, fc='r')
        self.draw.add_patch(rectangle)

    def draw_cities(self):
        """
        :return : N/A
        """

        for city in self.environment.cities:
            # plot all of the cities (as dots)
            circle = plt.Circle((city[0], city[1]), radius=0.1, fc='lightskyblue', ec='black')
            self.draw.add_patch(circle)

    def draw_split(self, points):
        """
        :param points   : list of split points that will partition the environment
        :return         : N/A
        """
        for point in points:

            line = plt.Line2D((self.environment.center[0], point[0]), (self.environment.center[1], point[1]), lw=3,
                              color='green')
            self.draw.add_line(line)

    def draw_path(self, path, color, draw=True):
        """
        :param path : this is list calculated by a tsp solver
        :return     : path length
        """

        # this will be calculated iteratively
        path_length = 0

        # these will control the logic of the color gradient of the arrows
        # currently there are 10 shades of red
        count = 0
        back = False

        for v in range(len(path) - 1):
            x = path[v][0]
            y = path[v][1]
            dx = path[v + 1][0] - x
            dy = path[v + 1][1] - y

            # iteratively calculate path length
            path_length += math.hypot(dx, dy)

            if draw:
                # create an arrow
                arrow = plt.arrow(x, y, dx, dy, width=0.09, facecolor=color, edgecolor='black', zorder=10)
                self.draw.add_patch(arrow)

        return path_length

    def show_fig(self):
        """
        :return : N/A
        """
        # this will plot everything
        plt.axis('scaled')
        plt.title(label=self.title)
        plt.grid(b=True)
        plt.show()

        # close the figure so other figures can be created
        plt.close(self.env_fig)



