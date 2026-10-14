# Hardware

## System Overview

PiDigiFrame is designed as a self-contained, portable digital picture frame built around a Raspberry Pi 3A+.

The Raspberry Pi, display, battery system, and supporting hardware are integrated into a custom 3D-printed enclosure so the finished system can operate as a standalone appliance without an external computer.

## Major Components

- **Raspberry Pi 3A+**  
  Main computing platform responsible for slideshow playback, touchscreen controls, and the local image-upload server.

- **Raspberry Pi Official 7-inch Touchscreen Display**  
  Primary display and user interface for the frame.

- **PiSugar 3 Plus – 5000 mAh**  
  Provides battery power and battery-status information to the Raspberry Pi.

- **64 GB microSD Card**  
  Stores Raspberry Pi OS, the DigiFrame application, and the local image library.

- **Custom 3D-Printed Enclosure**  
  Houses the display, Raspberry Pi, battery system, and supporting components.

- **Custom 3D-Printed Stand**  
  Supports the completed frame in its intended display orientation.

## Design Goals

The hardware was designed around several primary goals:

- Operate as a dedicated appliance rather than a visible Raspberry Pi development system
- Require minimal external wiring during normal use
- Remain portable through integrated battery power
- Allow access to the touchscreen without exposing the internal electronics
- Provide a clean enclosure suitable for everyday display
- Keep the Raspberry Pi and supporting components serviceable if future changes are required

## Enclosure

The enclosure and stand were designed specifically for the DigiFrame hardware.

The design accommodates the touchscreen display while providing internal space for the Raspberry Pi 3A+, PiSugar battery system, wiring, and mounting hardware.

CAD source files and printable exports are available in the [`cad/`](../cad/) directory.

## Power

Portable power is supplied by the PiSugar 3 Plus 5000 mAh battery system.

The DigiFrame application queries the PiSugar service locally and displays the current battery percentage directly on the slideshow interface.

This allows the device to remain visually minimal while still exposing useful battery information during normal operation.

## Display and Brightness Control

The touchscreen serves both as the image display and the limited user interface.

Display brightness is adjusted directly through the Raspberry Pi backlight interface. The application exposes simple on-screen increase and decrease controls while constraining brightness to a usable range.

This avoids requiring access to the Raspberry Pi desktop or command line for routine brightness changes.

## Operating Configuration

The system runs Raspberry Pi OS and is configured to launch the DigiFrame software automatically.

During normal use, the Raspberry Pi desktop is not part of the user experience. The device boots directly into the fullscreen application and functions as a dedicated picture frame.