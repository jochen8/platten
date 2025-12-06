#
#
# 9*8*7*6*5 * 4 ** 5 = 15_120 * 1024 = 15_482_880

import time

def rotate_list_slicing(lst, offset):
    n = len(lst)
    # Berechnet den tatsächlichen Offset, um Rundungen zu vermeiden
    offset = offset % n
    # Erstellt die neue Liste durch die Kombination von zwei Slices
    return lst[offset:] + lst[:offset]


class WegPlatte:
    def __init__(self, typ=0, east=0, north=0, west=0, south=0, angle=0):
        self.typ = typ
        self.east = east
        self.north = north
        self.west = west
        self.south = south
        self.angle = angle


free = WegPlatte(typ=0, east=0, north=0, west=0, south=0, angle=0)

class Garden:
    def __init__(self):
        #  3,1  3,2  3,3  -  2,0  2,1  2,2
        #  2,1  2,2  2,3  -  1,0  1,1  1,2
        #  1,1  1,2  1,3  -  0,0  0,1  0,2
        self.slab = [[free, free, free],
                     [free, free, free],
                     [free, free, free]]
        self.result = []


    def put_slab(self, wp, x, y, angle):
        z = wp.east, wp.north, wp.west, wp.south
        east, north, west, south = z[-angle//90:] + z[:-angle//90]
        self.slab[x][y] = WegPlatte(wp.typ, east, north, west, south, angle)


    def put_slab_n(self, wp, n, angle):
        y, x = divmod(n, 3)
        z = wp.east, wp.north, wp.west, wp.south
        east, north, west, south = z[-angle//90:] + z[:-angle//90]
        self.slab[x][y] = WegPlatte(wp.typ, east, north, west, south, angle)

    def print(self):
        for iy in range(3):
            for ix in range(3):
                print(self.slab[ix][iy].typ,self.slab[ix][iy].angle, end=' - ')
        print(self.calc_cost())


    def test_outer(self):
        x = self.slab
        c = [
            x[0][0].south,x[1][0].south,x[2][0].south,
            x[2][0].east,x[2][1].east,x[2][2].east,
            x[2][2].north,x[1][2].north,x[0][2].north,
            x[0][2].west,x[0][1].west,x[0][0].west,
            ]
        # print(c)
        c = c.count(1)
        # print(c)
        return c == 1


    def test_inner(self):
        x = self.slab
        c = x[0][0].east  == x[1][0].west and \
            x[1][0].east  == x[2][0].west and \
            x[0][1].east  == x[1][1].west and \
            x[1][1].east  == x[2][1].west and \
            x[0][2].east  == x[1][2].west and \
            x[1][2].east  == x[2][2].west and \
            x[0][0].north == x[0][1].south and \
            x[0][1].north == x[0][2].south and \
            x[1][0].north == x[1][1].south and \
            x[1][1].north == x[1][2].south and \
            x[2][0].north == x[2][1].south and \
            x[2][1].north == x[2][2].south

        return c


    def clear(self):
        self.slab = [[free, free, free], [free, free, free], [free, free, free]]

    def calc_cost(self):
        cost = 0
        for ix, iy in ((0,0),(0,1),(0,2)):
            if self.slab[ix][iy].typ != 0:
                cost += 12
        for ix, iy in ((1,0),(1,1),(2,0)):
            if self.slab[ix][iy].typ != 0:
                cost += 15
        for ix, iy in ((2,1),(1,2),(2,2)):
            if self.slab[ix][iy].typ != 0:
                cost += 18
        return cost


def calc(cost=66):
    i = 0
    for i12 in range(3 + 1):
        for i15 in range(3 + 1):
            for i18 in range(3 + 1):
                # print(i12, i15, i18)
                if i12 * 12 + i15 * 15 + i18 * 18 == cost and i12 + i15 + i18 == 5:
                    i += 1
                    print(f'cost = {cost}, no {i} --- {i12}, {i15}, {i18} --- {i12} * 12 + {i15} * 15 + {i18} * 18 == {cost}')
    if i == 0:
        print(f'cost = {cost}, ---')


def put_slabs(g, i1, i2, i3, i4, i5):
    g.clear()
    nn2 = 0
    for a1 in (0, 90, 180, 270):
        for a2 in (0, 90): # 180, 270 are duplicate
            for a3 in (0, 90, 180, 270):
                for a4 in (0, 90, 180, 270):
                    for a5 in (0, 90, 180, 270):
                        y, x = divmod(i1, 3)
                        g.put_slab(wp1, x, y, a1)
                        y, x = divmod(i2, 3)
                        g.put_slab(wp2, x, y, a2)
                        y, x = divmod(i3, 3)
                        g.put_slab(wp3, x, y, a3)
                        y, x = divmod(i4, 3)
                        g.put_slab(wp4, x, y, a4)
                        y, x = divmod(i5, 3)
                        g.put_slab(wp5, x, y, a5)
                        nn2 += 1
                        if g.test_outer() and g.test_inner():
                            #g.pr int()
                            res = f'{g.calc_cost()}'
                            for iy in range(3):
                                for ix in range(3):
                                    res += f' - {g.slab[ix][iy].typ} {g.slab[ix][iy].angle}'
                            g.result.append(res)

    return nn2


if __name__ == '__main__0':
    calc(60)
    for cost in (66, 69, 72, 75, 78, 81, 84):
        calc(cost)

wp1 = WegPlatte(1,0, 0, 1, 1, 0)
wp2 = WegPlatte(2,0, 1, 0, 1, 0)
wp3 = WegPlatte(3,0, 0, 0, 1, 0)
wp4 = WegPlatte(3,0, 0, 0, 1, 0)
wp5 = WegPlatte(5,1, 1, 0, 1, 0)


if __name__ =='__main__0':
    g = Garden()
    g.put_slab(wp1, 2, 1, 270)
    g.put_slab(wp2, 2, 2, 0)
    g.put_slab(wp3, 1, 2, 0)
    g.put_slab(wp4, 1, 0, 180)
    g.put_slab(wp5, 1, 1, 0)
    for yi in range(3):
        for xi in range(3):
            print(xi, yi,
                  g.slab[xi][yi].east,
                  g.slab[xi][yi].north,
                  g.slab[xi][yi].west,
                  g.slab[xi][yi].south,
                  )
    print(g.test_outer())
    print(g.test_inner())


def print_cost_count():
    cost_count = {}
    for cost in res:
        cost = int(cost.split(' ')[0])
        cost_count[cost] = cost_count.get(cost, 0) + 1
    for cost in sorted(cost_count.keys()):
        print(cost, cost_count[cost])


if __name__ == '__main__':
    g = Garden()
    nn = 0
    t0 = time.time()
    for i1 in range(9):
        for i2 in range(9):
            for i3 in range(9):
                for i4 in range(9):
                    for i5 in range(9):
                        ii = i1, i2, i3, i4, i5
                        collision = False
                        for ix in range(9):
                            if ii.count(ix) > 1:
                                collision = True
                        if collision:
                            continue
                        nn += put_slabs(g, i1, i2, i3, i4, i5)
    print(nn)
    res = set(g.result)
    res = sorted(list(res))
    for x in res:
        print(x)

    print_cost_count()

    print(time.time() - t0)

