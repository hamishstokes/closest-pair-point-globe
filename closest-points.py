__author__ = 'Hamish Stokes'
import math
import operator


class City:
    def __init__(self, in_list):
        self.name = in_list[0]
        self.latitude = float(in_list[1])
        self.longitude = float(in_list[2])


def distance_city_object(city1, city2, co, si, aco):
    theta = city1.longitude - city2.longitude
    lat1d = city1.latitude * 0.017453292519943295
    lat2d = city2.latitude * 0.017453292519943295
    dist = si(lat1d) * si(lat2d) + co(lat1d) \
                                   * co(lat2d) * co(theta * 0.017453292519943295)
    if dist > 1:
        return 0
    elif dist < -1:
        dist = math.pi
    else:
        dist = aco(dist)

    dist *= 6370.693485653058
    return (city1, city2), dist




def closest_pair_brute(short_list, num, co, si, aco):
    return min((distance_city_object(short_list[i], short_list[j], co, si, aco) for i in range(num - 1) for j in range(i + 1, num)),
               key=operator.itemgetter(1))


def recur(mark, count):
    co = math.cos
    si = math.sin
    aco = math.acos
    x_sorted = sorted(mark, key=operator.attrgetter("longitude"))
    y_sorted = sorted(mark, key=operator.attrgetter("latitude"))
    pair, min = minimum_distance(x_sorted, y_sorted, count, co, si, aco)
    alpha = sorted(pair, key=operator.attrgetter("name"))
    print("Closest pair:", alpha[0].name, alpha[1].name)
    print("Distance:", round(min, 1))
    return


def minimum_distance(x_sort, y_sort, count, co, si, aco):
    num = count
    half = count // 2
    if num <= 3:
        return closest_pair_brute(x_sort, num, co, si, aco)
    left = x_sort[:half]
    right = x_sort[half:]
    middle = left[-1].longitude

    nl = filter(lambda x: x.longitude <= middle, y_sort)
    nr = filter(lambda x: x.longitude > middle, y_sort)

    pairl, dl = minimum_distance(left, nl, half, co, si, aco)
    if num % 2 == 0:
        pairr, dr = minimum_distance(right, nr, half, co, si, aco)
    else:
        pairr, dr = minimum_distance(right, nr, half + 1, co, si, aco)

    if dl < dr:
        dm, pairm = (dl, pairl)
    else:
        dm, pairm = (dr, pairr)

    dist_from_pole = dm / 10001 * 90
    close = []
    append = close.append
    numclose = 0
    for p in y_sort:
        if p.longitude < dist_from_pole or p.longitude > dist_from_pole or 90 - dist_from_pole < p.latitude or \
                                -90 + dist_from_pole > p.latitude:
            append(p)
            numclose += 1

    if numclose > 1:
        for i in range(numclose - 1):
            for j in range(i + 1, min(i + 7, numclose)):
                curpair, curdm = distance_city_object(close[i], close[j], co, si, aco)
                if curdm < dm:
                    pairm, dm = curpair, curdm
    return pairm, dm


def main():
    inp = input
    n = inp()
    iters = 1
    while n[0] != '0':
        count = int(n)
        city_list = [City(inp().rsplit(' ', 2)) for x in range(count)]
        print("Scenario {}:".format(iters))
        recur(city_list, count)
        n = inp()
        iters += 1

main()

