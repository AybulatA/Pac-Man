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
                if r > 50 or b > 50 or g > 50:
                    t = False
                if t:
                    print('passed')
                    pixels[i, j] = 255, 255, 255, 255

        im.save(n)
