import math

def partitioning(a1, a2, x, y):
    '''
    :param a1: width of sub partition
    :param a2: height of sub partition
    :param x: width of environment
    :param y: height of environment
    :return:
    '''

    P = []
    i = 0

    for k1 in range(1, math.ceil(x/a1)):
        for k2 in range(1, math.ceil(y/a2)):
            i = i+1
            P.append([[(k1-1)*a1, k1*a1], [(k2-1)*a2, k2*a2]])

    for k in range(1, math.ceil(y/a2)):
        i = i+1
        P.append([[x-a1, x], [(k-1)*a2, k*a2]])

    for k in range(1, math.ceil(x/a1)):
        i = i+1
        P.append([[(k-1)*a1, k*a1], [y-a2, y]])

    i = i+1
    P.append([[x-a1, x], [y-a2, y]])

    return P


P = partitioning(3, 3, 10, 11)