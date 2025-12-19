#
# -------------
# | 6 | 7 | 8 |
# -------------
# | 3 | 4 | 5 |
# -------------
# | 0 | 1 | 2 |
# -------------
#
# calc_cost
# t1 t2 t3 t3 t5
# n1 n2 n3 n4 n5
# a1 a2 a3 a3 a4
#
#

import os
import time
from PIL import Image, ImageDraw #, ImageOps


slab_width, slab_height = 21, 21
line_width = 3


def make_garden_image_from_garden(garden, directory, image_number):
    base_image = Image.new("RGB", (slab_width * 3 + 4, slab_height * 3 + 4), "white")
    draw = ImageDraw.Draw(base_image)
    draw.line((0, 0, 66, 0), fill="grey", width=1)
    draw.line((0, 22, 66, 22), fill="grey", width=1)
    draw.line((0, 44, 66, 44), fill="grey", width=1)
    draw.line((0, 66, 66, 66), fill="grey", width=1)
    draw.line((0, 0, 0, 66), fill="grey", width=1)
    draw.line((22, 0, 22, 66), fill="grey", width=1)
    draw.line((44, 0, 44, 66), fill="grey", width=1)
    draw.line((66, 0, 66, 66), fill="grey", width=1)
    cost = garden.calculate_cost()
    for n in range(9):
        slab = garden.slabs[n]
        if slab.type == 0:
            continue
        else:
            iy, ix = divmod(n, 3)
            #print(wp.typ, wp.n, wp.angle, ix * 21, 62 - iy * 21)
            # Open the image you want to insert (overlay)
            overlay = Image.open(f"slab_type_{slab.type}.png").convert("RGBA")

            # Rotate overlay if needed
            overlay = overlay.rotate(slab.angle)
            #overlay = ImageOps.mirror(overlay)

            # Paste overlay onto base at position (x=ix, y=iy)
            base_image.paste(overlay, (ix * 22 + 1, 45 - iy * 22), overlay)  # third arg keeps transparency

    # Save the result
    image_filename = f'{directory}/valid_garden_{cost:02d}_{image_number:02d}.png'
    base_image.save(image_filename, format="PNG")



class Slab:
    def __init__(self, slab_type=0, angle=0, east=0, north=0, west=0, south=0):
        self.type = slab_type
        self.angle = angle
        self.east = east
        self.north = north
        self.west = west
        self.south = south



class Garden:
    def __init__(self):
        free = Slab(slab_type=0)
        #  6  7  8
        #  3  4  5
        #  0  1  2
        self.slabs = {n: free for n in range(9)}


    def put_slab(self, slab_type, position, angle):
        connections = {
            0: (0, 0, 0, 0),
            1: (0, 0, 1, 1),
            2: (0, 1, 0, 1),
            3: (0, 0, 0, 1),
            5: (1, 1, 0, 1),
        }[slab_type]

        east, north, west, south = connections[-angle//90:] + connections[:-angle//90]
        self.slabs[position] = Slab(slab_type, angle, east, north, west, south)


    def calculate_cost(self):
        cost = 0
        for n in (0, 3, 6):
            if self.slabs[n].type > 0:
                cost += 12
        for n in (1, 2, 4):
            if self.slabs[n].type > 0:
                cost += 15
        for n in (5, 7, 8):
            if self.slabs[n].type > 0:
                cost += 18
        return cost


    def test_outer(self):
        t = [
            self.slabs[2].east,  self.slabs[5].east,  self.slabs[8].east,
            self.slabs[6].north, self.slabs[7].north, self.slabs[8].north,
            self.slabs[0].west,  self.slabs[3].west,  self.slabs[6].west,
            self.slabs[0].south, self.slabs[1].south, self.slabs[2].south,
            ]
        t = t.count(1)
        return t == 1


    def test_inner(self):
        t = self.slabs[0].east  == self.slabs[1].west and \
            self.slabs[1].east  == self.slabs[2].west and \
            self.slabs[3].east  == self.slabs[4].west and \
            self.slabs[4].east  == self.slabs[5].west and \
            self.slabs[6].east  == self.slabs[7].west and \
            self.slabs[7].east  == self.slabs[8].west and \
            self.slabs[0].north == self.slabs[3].south and \
            self.slabs[1].north == self.slabs[4].south and \
            self.slabs[2].north == self.slabs[5].south and \
            self.slabs[3].north == self.slabs[6].south and \
            self.slabs[4].north == self.slabs[7].south and \
            self.slabs[5].north == self.slabs[8].south
        #  6  7  8
        #  3  4  5
        #  0  1  2
        return t



def fill_and_test_garden(g, n1, a1, n2, a2, n3, a3, n4, a4, n5, a5):
    g.put_slab(1, n1, a1)
    g.put_slab(2, n2, a2)
    g.put_slab(3, n3, a3)
    g.put_slab(3, n4, a4)
    g.put_slab(5, n5, a5)
    return g.test_outer() and g.test_inner()



if __name__ == '__main__':
    valid_gardens = []
    n_all = 0
    n_valid = 0
    t0: float = time.time()
    for n1 in range(9):
        for n2 in range(9):
            for n3 in range(9):
                for n4 in range(9):
                    if n3 >= n4:
                        continue
                    for n5 in range(9):
                        n1_n5 = sorted([n1, n2, n3, n4, n5])
                        if n1_n5 != sorted(list(set(n1_n5))):  # duplicates exist
                            continue

                        #if len(set([n1, n2, n3, n4, n5])) != 5:  # duplicates exist
                        #    continue

                        for a1 in (0, 90, 180, 270):
                            for a2 in (0, 90):  # 180, 270 are duplicate
                                for a3 in (0, 90, 180, 270):
                                    for a4 in (0, 90, 180, 270):
                                        for a5 in (0, 90, 180, 270):
                                            n_all += 1
                                            garden = Garden()
                                            if fill_and_test_garden(garden, n1, a1, n2, a2,
                                                                    n3, a3, n4, a4, n5, a5):
                                                n_valid += 1
                                                valid_gardens.append(garden)

    print('n_all:', n_all)
    print('n_valid:', n_valid, len(valid_gardens))
    print(time.time() - t0)

    image_directory = 'images_valid_garden'
    if len(valid_gardens) > 0 and not os.path.exists(image_directory):
        os.mkdir(image_directory)
    nn = {n: 0 for n in range(66, 84+1, 3)}
    for garden in valid_gardens:
        cost = garden.calculate_cost()
        nn[cost] += 1
        #make_garden_image_from_garden(garden, image_directory, nn[cost])

    print(time.time() - t0)
