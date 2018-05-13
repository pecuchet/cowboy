import os
import imghdr
import argparse
import config
import os.path
import time

from logzero import logger
from pathlib import Path
from urllib import request


def setup(image):
    """
    Assure everything is done for the program to run well
    :param image:
    :return:
    """
    google_json = app_dir() + config.GOOGLE_CONFIG_FILE

    # check if given image exists and is of the right type
    if check_image(image):
        logger.debug("Input image file OK (" + image + ")")
    else:
        return 0

    # check if we have config.json file
    if Path(google_json).is_file():
        logger.debug("Google config file found")
    else:
        logger.error('Google config file not found')

    # all done
    logger.debug('Program setup done')

    return 1


def expired():
    """
    Check if we need to download a new series of images
    :return:
    """
    img_list = images_dir() + "list.txt"
    m_time = os.path.getmtime(img_list)
    now = time.time()

    logger.debug("Images last download time: %s" % time.ctime(m_time))

    return m_time >= now + 86400


def app_dir():
    """
    Get our app's root directory
    :return:
    """
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"


def images_dir():
    """
    Get our app's root directory
    :return:
    """
    return app_dir() + "images/"


def check_image(path):
    """
    Check if local or remote image is exists, is accessible and of right format
    :param path:
    :return:
    """

    if not path.startswith('http'):
        # check if local image exists
        if not Path(path).is_file():
            logger.error('Given image file not found')
            return False
        extension = imghdr.what(path)

    else:
        # check if remote image exists
        logger.debug('Checking remote image existence...')
        try:
            req = request.urlopen(path)
            extension = req.info()['Content-Type'].split("/")[1]
        except request.URLError as e:
            logger.error('Remote image file not found')
            return False

    # check if image is of right type
    if extension not in ['jpeg', 'jpg', 'png', 'gif']:
        logger.error('The image should be a jpg, png or gif')
        return False

    return True


def parse_arguments():
    """
    Get command line arguments
    :return:
    """
    parser = argparse.ArgumentParser(description=config.DESCRIPTION)

    # Required image file path
    parser.add_argument("image", help="Required image to perform the similar image request on")

    # Optional request schedule, defaults to ``1d`
    # parser.add_argument("-s", "--schedule", action="store", dest="req_schedule")

    # Optional request time, defaults to ``08:30`
    # parser.add_argument("-t", "--time", action="store", dest="req_time")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="{name} (version {version})".format(version=config.VERSION, name=config.NAME))

    return parser.parse_args()
