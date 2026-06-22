import sys
from PIL import Image
# usage: pngcrop.py <file> <y0frac> <y1frac> <outname>
f, y0, y1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
im = Image.open(f)
W, H = im.size
c = im.crop((0, int(H*y0), W, int(H*y1)))
# upscale a touch if narrow region for readability is not needed; cap width 1900
if c.size[0] > 1900:
    c = c.resize((1900, int(c.size[1]*1900/c.size[0])))
c.save(f"build/zoom/{out}.png")
print(out, c.size, f"(src {W}x{H}, y {int(H*y0)}-{int(H*y1)})")
