#!/usr/bin/env python
# Website scraper for extacting & saving homepage screenshot and favicon

""" TODOs
        * Command-line arguments
        * Migrate from urllib to requests
        * Fix exception for vogue.com
        * Apply fix to PhantomJS source code:
            https://github.com/ariya/phantomjs/issues/10389
"""

import logging
import sys
import urllib

from selenium import webdriver

DEBUG=False
WINDOW_SIZE=(1024, 768)

def run(url, screenshot_dest, favicon_dest):
    if not url:
        logging.error("URL is blank. Quitting")
        sys.exit(-1)
    logging.info("Running crawler on %s", url)
    dcap = {'acceptSslCerts':True}
    br = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
    br.set_window_size(WINDOW_SIZE[0], WINDOW_SIZE[1])
    br.get(url)
    favicon_src = 'http://www.google.com/s2/favicons?domain=' + url
    logging.debug("Favicvon HREF for %s: %s", url, favicon_src)
    logging.info("Saving favicon of homepage for %s", url)
    urllib.urlretrieve(favicon_src, favicon_dest)
    logging.info("Saving screenshot of homepage for %s", url)
    br.save_screenshot(screenshot_dest)
    br.quit()

def ensure_utf8():
    reload(sys)
    sys.setdefaultencoding('utf8')

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

if __name__ == '__main__':
    ensure_utf8()
    setup_logging()
    url = "https://www.google.com"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    run(url, screenshot_dest='screenshot.png', favicon_dest='favicon.png')


