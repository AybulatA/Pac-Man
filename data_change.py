from PIL import Image
import os


ways = ['sound_on', 'sound_off']
names = ['game']
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
                if r < 200 or b < 200 or g < 200:
                    t = False
                if t:
                    print('passed')
                    pixels[i, j] = 255, 255, 255, 255

        im.save(n)
