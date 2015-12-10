#!/usr/bin/env python
# Image processer for favicon + screenshot combination

""" TODOs
    * Class-based?
    * primary_colors() NOT working on ICO -> PNG
    * Crashes on:
        http://www.pornhub.com
        http://www.cnn.com
"""
import colorsys
import logging
import sys

import scipy
import scipy.cluster
import scipy.misc

from PIL import Image

DEBUG=False
RESIZE_SHAPE=(500, 500)

def primary_colors(filename, num_colors=5, resize=True, resize_scale=0.8):
    image = Image.open(filename)
    print image.size
    if resize:
        image.resize(map(lambda x: int(x * resize_scale), image.size))
    data = list(image.getdata())
    width, height = image.size
    pixels = [data[i * width : (i + 1) * width] for i in xrange(height)]
    ar = scipy.misc.fromimage(image).astype(float)
    shape = ar.shape
    if len(shape) > 2:
            ar = ar.reshape(scipy.product(shape[:2]), shape[2])
            if ar.shape[1] == 4:
                ar = [it[:-1] for it in ar]
    whitened_ar = scipy.cluster.vq.whiten(ar)
    centroids, _ = scipy.cluster.vq.kmeans(ar, num_colors)
    primary_rgb_colors = centroids.astype(int)
    return ["%0.2X%0.2X%0.2X" %(r, g, b) for (r, g, b) in primary_rgb_colors]


def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
    return colorsys.rgb_to_hsv(r, g, b)

def process(favicon_loc, screenshot_loc):
    logging.info("Processing tuple: %s %s", favicon_loc, screenshot_loc)
    favicon_colors = []
    screenshot_colors = []
    try:
        favicon_colors = primary_colors(favicon_loc)
        favicon_colors.sort(key=get_hsv)
    except:
        logging.warn("Could not generate primary colors for Favicon at %s", favicon_loc)

    try:
        screenshot_colors = primary_colors(screenshot_loc, num_colors=5, resize=True)
        screenshot_colors.sort(key=get_hsv)
    except:
        logging.warn("Could not generate primary colors for Screenshot at %s", favicon_loc)

    # TODO Move out to formatter, DB, etc.
    """
        <div class="site-data hidden">
            <h1 class="title">Template</h1>
            <!-- Data goes here -->
        </div>
    """
    print "<div class=\"site-data\">\n    <h1 class=\"title\">NAME</h1>"
    print "    <div class=\"favicon color-data cf\">"
    for hex_color in favicon_colors:
        print "        <div class=\"color-box\" style=\"background-color: #%s\"></div>" % hex_color
    print "    </div>\n    <div class=\"site color-data\">"
    for hex_color in screenshot_colors:
        print "        <div class=\"color-box\" style=\"background-color: #%s\"></div>" % hex_color
    print "    </div>"
    print "</div>"

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

if __name__ == '__main__':
    setup_logging()
    favicon_loc = 'favicon.png'
    screenshot_loc = 'screenshot.png'
    process(favicon_loc, screenshot_loc)


