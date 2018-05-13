import config
import io
import os

from logzero import logger
from google.cloud import vision
from google.cloud.vision import types
from urllib import request
from cowboy import helpers


def start_display():
    """
    Launch command-line tool fbi to display images
    :return:
    """
    logger.debug('Launching display')
    os.system("sudo killall -9 fbi")
    os.system("sudo fbi -a -t 5 --noverbose -l " + helpers.images_dir() + 'list.txt')
    return


def fetch(img):
    """
    Returns web annotations given the path to an image
    :param img:
    :return:
    """
    logger.debug('Querying google...')

    # setup client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = helpers.app_dir() + config.GOOGLE_CONFIG_FILE
    client = vision.ImageAnnotatorClient()

    # setup image parameter
    if img.startswith('http'):
        image = types.Image()
        image.source.image_uri = img
    else:
        with io.open(img, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

    # perform request
    result = client.annotate_image({
        'image': image,
        'features': [{'type': vision.enums.Feature.Type.WEB_DETECTION, 'max_results': config.NUM_RESULTS}]
    })

    return result.web_detection


def save(images):
    """
    Download and save each image
    :param images:
    :return:
    """
    i = 0
    images_dir = helpers.images_dir()
    file_list = []

    for img in images:
        r = _download_image(img.url)

        if r is not False:
            i += 1
            file_list.append(_save_image(r, i, images_dir))

    _save_image_list(images_dir, file_list)

    return i >= config.MIN_SAVED


def _download_image(url):
    """
    Download from an url
    :param url:
    :return:
    """
    logger.debug('Downloading image ' + str(url))

    try:
        req = request.urlopen(url)
    except request.URLError as e:
        logger.warning('Image download failed: ' + str(e.reason))
        pass
        return False

    c_type = req.info()['Content-Type']
    ext = c_type.split("/")[1]

    if ext not in ['jpeg', 'jpg', 'png', 'gif', 'tif', 'tiff', 'bmp']:
        logger.warning('Image skipped, wrong content-type (' + str(c_type) + ') or extension (' + str(ext) + ')')
        return False

    return req


def _save_image(req, index, images_dir):
    """
    Saves image based on dict from _download_image
    :param req:
    :return:
    """
    ext = req.info()['Content-Type'].split("/")[1]
    path = images_dir + str(index) + "." + ext

    with open(path, 'wb') as output:
        output.write(req.read())

    return path


def _save_image_list(images_dir, list):
    """
    Write array to line-break separated text file; list of local images
    :param images_dir:
    :param list:
    :return:
    """
    with open(images_dir + 'list.txt', 'w') as txt:
        for i in list:
            txt.write("{}\n".format(i))
