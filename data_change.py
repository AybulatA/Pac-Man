from PIL import Image
import os


ways = ['frightened(first)', 'frightened(second)', 'half_frightened(first)', 'half_frightened(second)']
names = ['Ghost']
for name in names:
    for action in ways:
        na = action + '.png'
        n = 'D:\Python\Gits\Pac-Man\data\ '.strip() + name + '\ '.strip() + na
        fullname = os.path.join(name, n)

        im = Image.open(r"{}".format(n))
        pixels = im.load()
        x, y = im.size

        for i in range(x):
            for j in range(y):
                t = True
                print(pixels[i, j])
                r, g, b, p = pixels[i, j]
                if r > 20 or b > 20 or g > 20:
                    t = False
                if t:
                    print('passed')
                    pixels[i, j] = 0, 0, 0, 255

        im.save(n)
