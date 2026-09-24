import os
import random
import subprocess
import tkinter as tk

from PIL import Image, ImageTk

import config


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


class DigiFrameApp:
    def __init__(self, root):
        self.root = root

        self.root.configure(cursor="none")
        self.root.configure(bg=config.BACKGROUND_COLOR)
        self.root.attributes("-fullscreen", True)

        self.image_label = tk.Label(
            self.root,
            bg=config.BACKGROUND_COLOR
        )
        self.image_label.pack(fill="both", expand=True)

        self.image_paths = self.load_image_paths()

        self.current_index = 0

        if config.RANDOMIZE:
            random.shuffle(self.image_paths)

        self.settings_button = tk.Label(
            self.root,
            text="SET",
            fg="white",
            bg=config.BACKGROUND_COLOR,
            font=("Arial", 10)
        )

        self.settings_button.place(
            relx=0.02,
            rely=0.02,
            anchor="nw"
        )

        self.settings_button.bind(
            "<Button-1>",
            lambda event: self.open_settings()
        )

        self.battery_label = tk.Label(
            self.root,
            text="--%",
            fg="white",
            bg=config.BACKGROUND_COLOR,
            font=("Arial", 10)
        )

        self.battery_label.place(
            relx=0.98,
            rely=0.02,
            anchor="ne"
        )

        if not self.image_paths:
            self.show_message("No images found.")
            return
        else:
            self.show_current_image()
            self.root.after(
                config.SLIDE_INTERVAL,
                self.next_image
            )

        self.update_battery()

        self.settings_button.lift()
        self.battery_label.lift()

        self.root.bind("<Escape>", self.exit_fullscreen)


    def update_battery(self):
        raw_percent = get_battery_percent()

        try:
            percent =round(float(raw_percent))
            self.battery_label.configure(text=f"{percent}%")

        except (ValueError, TypeError):
            self.battery_label.configure(text="--%")

        self.root.after(
            60000,
            self.update_battery
        )


    def open_settings(self):
        # Don't open a second copy
        if hasattr(self, "settings_frame") and self.settings_frame.winfo_exists():
            return

        current = get_brightness_percent()

        if current is None:
            current = config.DEFAULT_BRIGHTNESS

        self.brightness_value = tk.IntVar(value=current)

        self.settings_frame = tk.Frame(
            self.root,
            bg="#111111",
            bd=2,
            relief="solid"
        )

        self.settings_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=220,
            height=180
        )

        tk.Label(
            self.settings_frame,
            text="Brightness",
            fg="white",
            bg="#111111",
            font=("Arial", 14)
        ).pack(pady=(15, 5))

        self.brightness_label = tk.Label(
            self.settings_frame,
            text=f"{current}%",
            fg="white",
            bg="#111111",
            font=("Arial", 12)
        )
        self.brightness_label.pack(pady=5)

        controls = tk.Frame(
            self.settings_frame,
            bg="#111111"
        )
        controls.pack(pady=10)

        minus_button = tk.Button(
            controls,
            text="-",
            fg="white",
            bg="#333333",
            activeforeground="white",
            activebackground="#444444",
            font=("Arial", 16),
            relief="flat",
            bd=0,
            highlightthickness=0,
            command=lambda: self.change_brightness(-config.BRIGHTNESS_STEP)
        )
        minus_button.pack(side="left", padx=10)

        plus_button = tk.Button(
            controls,
            text="+",
            fg="white",
            bg="#333333",
            activeforeground="white",
            activebackground="#444444",
            font=("Arial", 16),
            relief="flat",
            bd=0,
            highlightthickness=0,
            command=lambda: self.change_brightness(config.BRIGHTNESS_STEP)
        )
        plus_button.pack(side="left", padx=10)

        close_button = tk.Button(
            self.settings_frame,
            text="Close",
            fg="white",
            bg="#333333",
            activeforeground="white",
            activebackground="#444444",
            font=("Arial", 10),
            relief="flat",
            bd=0,
            highlightthickness=0,
            command=self.close_settings
        )
        close_button.pack(pady=8)

        self.settings_frame.lift()


    def close_settings(self):
        if hasattr(self, "settings_frame"):
            self.settings_frame.destroy()


    def change_brightness(self, amount):
        new_value = self.brightness_value.get() + amount
        new_value = max(1, min(100, new_value))

        if set_brightness_percent(new_value):
            self.brightness_value.set(new_value)
            self.brightness_label.configure(
                text=f"{new_value}%"
            )


    def load_image_paths(self):
        paths = []

        for filename in os.listdir(config.IMAGE_FOLDER):
            if filename.lower().endswith(IMAGE_EXTENSIONS):
                paths.append(os.path.join(config.IMAGE_FOLDER, filename))

        return paths


    def show_current_image(self):
        path = self.image_paths[self.current_index]

        image = Image.open(path)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        image.thumbnail(
            (screen_width, screen_height),
            Image.Resampling.LANCZOS
        )    

        canvas = Image.new(
            "RGB",
            (screen_width, screen_height),
            config.BACKGROUND_COLOR
        )

        x = (screen_width - image.width) // 2
        y = (screen_height - image.height) // 2

        canvas.paste(image, (x, y))

        self.tk_image = ImageTk.PhotoImage(canvas)

        self.image_label.configure(image=self.tk_image)

        self.settings_button.lift()
        self.battery_label.lift()

        if hasattr(self, "settings_frame") and self.settings_frame.winfo_exists():
            self.settings_frame.lift()


    def next_image(self):
        self.current_index += 1

        if self.current_index >= len(self.image_paths):
            self.current_index = 0

            if config.RANDOMIZE:
                random.shuffle(self.image_paths)

        self.show_current_image()

        self.root.after(
            config.SLIDE_INTERVAL,
            self.next_image
        )


    def show_message(self, text):
        self.image_label.configure(
            text=text,
            fg="white",
            font=("Arial", 24)
        )


    def exit_fullscreen(self, event=None):
        self.root.destroy()


def get_battery_percent():
    try:
        result = subprocess.run(
            ["sh", "-c", 'echo "get battery" | nc -q 0 127.0.0.1 8423'],
            capture_output=True,
            text=True,
            timeout=2
        )

        output = result.stdout.strip()
        output = output.replace("battery:", "").strip()
        output = output.replace("%", "").strip()

        return output

    except Exception:
        return ""


def get_brightness_percent():
    try:
        with open(config.BACKLIGHT_PATH, "r") as file:
            value = int(file.read().strip())

        return round((value / config.MAX_BRIGHTNESS) * 100)

    except Exception:
        return None


def set_brightness_percent(percent):
    percent = max(1, min(100, percent))
    value = round((percent / 100) * config.MAX_BRIGHTNESS)

    try:
        result = subprocess.run(
            [
                "sudo",
                "-n",
                "/usr/bin/tee",
                config.BACKLIGHT_PATH
            ],
            input=str(value),
            text=True,
            capture_output=True,
            timeout=2
        )

        if result.returncode != 0:
            print(f"Brightness command failed: {result.stderr}")
            return False

        return True

    except Exception as e:
        print(f"Brightness error: {e}")
        return False


if __name__ == "__main__":
    root = tk.Tk()
    app = DigiFrameApp(root)
    root.mainloop()
