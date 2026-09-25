## Restart command: ~/digiframe/restart_app.sh

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SLIDE_INTERVAL = 20000
FADE_INTERVAL = 700
BACKGROUND_COLOR = "black"
RANDOMIZE = True

BACKLIGHT_PATH = "/sys/class/backlight/10-0045/brightness"
MAX_BRIGHTNESS = 255
BRIGHTNESS_STEP = 10
DEFAULT_BRIGHTNESS = 70