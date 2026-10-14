# PiDigiFrame

A self-contained Raspberry Pi digital picture frame with randomized slideshow playback, battery monitoring, brightness control, and wireless image upload from a phone or computer.

![PiDigiFrame](docs/images/Frame-Front.jpg) ![PiDigiFrameBack](docs/images//Frame-Back.jpg)

## Overview

PiDigiFrame is a standalone digital picture frame built around a Raspberry Pi 3A+ and touchscreen display.

The project was designed to behave like a dedicated appliance rather than a general-purpose Raspberry Pi. Once powered on, the system automatically launches into a fullscreen photo slideshow and requires no keyboard, mouse, or desktop interaction during normal use.

Photos can be uploaded remotely through a lightweight web interface, allowing new images to be added from a phone or computer without removing the storage device or directly interacting with the Raspberry Pi.

## Features

- Fullscreen randomized photo slideshow
- Automatic image rescanning without restarting the application
- Wireless image upload through a local web interface
- SHA-256 duplicate-image detection
- PiSugar battery percentage display
- On-screen display brightness controls
- Automatic application startup
- Standalone Raspberry Pi appliance design
- Custom 3D-printed enclosure and stand

## Hardware

The frame is built around:

- Raspberry Pi 3A+
- Raspberry Pi Official 7-inch touchscreen display
- PiSugar 3 Plus 5000 mAh battery
- 64 GB microSD storage
- Custom 3D-printed enclosure and stand

Additional hardware information is available in [`docs/hardware.md`](docs/hardware.md).

## Software

The application is written in Python and uses Tkinter for the fullscreen slideshow interface.

Pillow is used for image loading and scaling, while a lightweight Flask server provides remote image uploads over the local network.

The slideshow application automatically scans the image directory, randomizes playback, scales images while preserving their aspect ratio, and periodically checks for newly uploaded photos.

The upload server supports multiple files at once and compares SHA-256 hashes to prevent duplicate images from being stored.

## Controls

The primary display remains dedicated to photos, with minimal controls overlaid on the screen.

- **SET** opens the brightness controls.
- Battery percentage is displayed in the upper-right corner.
- Brightness can be adjusted directly from the touchscreen.
- Images advance automatically according to the configured slideshow interval.

## Remote Image Upload

The included Flask server provides a simple browser-based upload interface.

Devices on the same local network can access the frame's upload page and send one or more images directly to the slideshow library.

Before saving an image, the server compares its SHA-256 hash against existing files. Duplicate images are skipped automatically.

## Project Structure

```text
PiDigiFrame/
├── app.py              # Main slideshow application
├── config.py           # Application configuration
├── upload_server.py    # Local web upload server
├── assets/             # Project photos and screenshots
├── cad/
│   ├── source/         # Editable CAD source files
│   └── exports/        # Printable models
└── docs/
    └── hardware.md     # Hardware and enclosure documentation
```

The slideshow photo directory itself is intentionally excluded from Git to prevent personal photographs from being included in the repository.

## Current Status

**Functional / Version 1 complete**

The frame is operational as a standalone appliance with slideshow playback, remote uploads, duplicate detection, battery monitoring, and display controls.

Future development may include additional slideshow organization and image-category features.

## Technologies

- Python
- Tkinter
- Flask
- Pillow
- Raspberry Pi OS
- Raspberry Pi
- FreeCAD
- 3D printing