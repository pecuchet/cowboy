NAME = "COWBOY (working title)"
AUTHOR = "Tessa Groenewoud <tessa@tessagroenewoud.nl> & Arnaud Coolsaet <arnaud@arnaudcoolsaet.eu>"
VERSION = "1.0.0"
LICENSE = "GPL-3.0"
DESCRIPTION = "Similar images project by Tessa Groenewoud & Arnaud Coolsaet: " + NAME

# google json authentication file (relative to the root of project)
# use [google's console](https://console.cloud.google.com/apis/credentials) to generate the json
GOOGLE_CONFIG_FILE = 'config-google.json'

# number of visually similar images to retrieve from google
NUM_RESULTS = 30

# minimum amount of images which should have been retrieved to launch display
MIN_SAVED = 25

# slide show delay, seconds to display image
IMG_DELAY = 5
