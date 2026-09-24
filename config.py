## Kill command: pkill -f "python3 app.py"
## Restart command: DISPLAY=:0 python3 /home/glass/digiframe/app.py > /home/glass/digiframe/app.log 2>&1 &

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
SLIDE_INTERVAL = 20000
FADE_INTERVAL = 700
BACKGROUND_COLOR = "black"
RANDOMIZE = True

BACKLIGHT_PATH = "/sys/class/backlight/10-0045/brightness"
MAX_BRIGHTNESS = 255
BRIGHTNESS_STEP = 10
DEFAULT_BRIGHTNESS = 70