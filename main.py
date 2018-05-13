#!/usr/bin/env python3
from logzero import logger
from cowboy import helpers, lib

"""
Cowboy (working title) main entry point
"""


def main(image):
    """
    Setup the program, download and save the image for the day,
    if all went well start the display
    """
    if not helpers.setup(image):
        exit(1)

    if not helpers.expired():
        lib.start_display()
        return

    response = lib.fetch(image)

    if not lib.save(response.visually_similar_images):
        logger.error('Not enough images saved! Check the download errors.')
        exit(1)

    lib.start_display()


if __name__ == "__main__":

    args = helpers.parse_arguments()

    main(args.image)
