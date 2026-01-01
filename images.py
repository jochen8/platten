#

from PIL import Image, ImageDraw #, ImageOps

# Create a blank white image
slab_width, slab_height = 21, 21
line_width = 3

def make_image_slab_type_1():
    image = Image.new("RGB", (slab_width, slab_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a line
    draw.line((0, 10, 5, 10), fill="black", width=line_width)
    draw.line((5, 10, 10, 15), fill="black", width=line_width)
    draw.line((10, 15, 10, 20), fill="black", width=line_width)
    #draw.line((0, 20, 9, 11), fill="red", width=linewidth)
    #draw.line((11, 11, 20, 20), fill="red", width=linewidth)

    # Save as PNG
    image.save("slab_type_1.png")

def make_image_slab_type_2():
    image = Image.new("RGB", (slab_width, slab_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a line
    draw.line((10, 0, 10, 20), fill="black", width=line_width)

    # Save as PNG
    image.save("slab_type_2.png")


def make_image_slab_type_3():
    image = Image.new("RGB", (slab_width, slab_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a line
    draw.line((10, 10, 10, 20), fill="black", width=line_width)

    # Save as PNG
    image.save("slab_type_3.png")


def make_image_slab_type_5():
    image = Image.new("RGB", (slab_width, slab_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a line
    draw.line((10, 0, 10, 20), fill="black", width=line_width)
    draw.line((10, 10, 20, 10), fill="black", width=line_width)

    # Save as PNG
    image.save("slab_type_5.png")


def make_garden_image(garden, image_filename):
    base_image = Image.new("RGB", (slab_width * 3, slab_height * 3), "white")

    for iy in range(3):
        for ix in range(3):
            slab = garden.slab[ix][iy]
            if slab.typ == 0:
                continue
            else:

                print(slab.typ, ix, iy, slab.angle, ix * 21, 62 - iy * 21)
                # Open the image you want to insert (overlay)
                overlay = Image.open(f"slab_type_{slab.typ}.png").convert("RGBA")

                # Rotate overlay if needed
                overlay = overlay.rotate(slab.angle)
                #overlay = ImageOps.mirror(overlay)

                # Paste overlay onto base at position (x=ix, y=iy)
                base_image.paste(overlay, (ix * 21, 42 - iy * 21), overlay)  # third arg keeps transparency

    # Save the result
    base_image.save(image_filename, format="PNG")
    print(72*'-')
    garden.print()
    print(72*'-')


def make_garden_image_from_result(results2):
    #print('results2', results2)

    for ir in range(len(results2)):
        base_image = Image.new("RGB", (slab_width * 3 + 2, slab_height * 3 + 2), "white")
        draw = ImageDraw.Draw(base_image)
        draw.line((0, 21, 64, 21), fill="grey", width=1)
        draw.line((0, 43, 64, 43), fill="grey", width=1)
        draw.line((21, 0, 21, 64), fill="grey", width=1)
        draw.line((43, 0, 43, 64), fill="grey", width=1)
        result = results2[ir]
        cost = result[0]
        for wp in result[1:]:
            if wp.typ == 0:
                continue
            else:
                iy, ix = divmod(wp.n, 3)
                #print(wp.typ, wp.n, wp.angle, ix * 21, 62 - iy * 21)
                # Open the image you want to insert (overlay)
                overlay = Image.open(f"slab_type_{wp.typ}.png").convert("RGBA")

                # Rotate overlay if needed
                overlay = overlay.rotate(wp.angle)
                #overlay = ImageOps.mirror(overlay)

                # Paste overlay onto base at position (x=ix, y=iy)
                base_image.paste(overlay, (ix * 22, 44 - iy * 22), overlay)  # third arg keeps transparency

        # Save the result
        image_filename = f'result_images/result_image_{cost:02d}_{ir:03d}.png'
        base_image.save(image_filename, format="PNG")


if __name__ == "__main__0":
    make_image_slab_type_1()
    make_image_slab_type_2()
    make_image_slab_type_3()
    make_image_slab_type_5()


if __name__ == "__main__":
    class R:
        def __init__(self, type, n, angle):
            self.typ = type
            self.n = n
            self.angle = angle

    results = [
        [R(1, 1, 180),
        R(2, 2, 90),
        R(3, 4, 0),
        ]]
    make_garden_image_from_result(results)