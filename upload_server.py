import os
import hashlib
from flask import Flask, request, render_template_string

import config


app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DigiFrame Upload</title>
</head>
<body style="font-family: sans-serif; padding: 20px;">
    <h2>Upload to DigiFrame</h2>

    <form method="post" enctype="multipart/form-data">
        <input type="file" name="images" accept="image/*" multiple required>
        <br><br>
        <button type="submit">Upload</button>
    </form>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}

    <h3>Images on Frame</h3>

    <p>{{ existing_images|length }} image(s)</p>

    <ul>
    {% for filename in existing_images %}
        <li>{{ filename }}</li>
    {% endfor %}
    </ul>

</body>
</html>
"""


def allowed_file(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in config.ALLOWED_EXTENSIONS


def file_hash(path):
    hasher = hashlib.sha256()

    with open(path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


@app.route("/", methods=["GET", "POST"])
def upload():
    message = ""

    if request.method == "POST":
        files = request.files.getlist("images")
        uploaded = []
        duplicates = 0

        for file in files:
            if not file or not file.filename:
                continue

            if not allowed_file(file.filename):
                continue

            filename = os.path.basename(file.filename)
            path = os.path.join(config.IMAGE_FOLDER, filename)

            file.stream.seek(0)

            incoming_data = file.read()
            incoming_hash = hashlib.sha256(incoming_data).hexdigest()

            file.stream.seek(0)

            duplicate = False

            for existing_name in os.listdir(config.IMAGE_FOLDER):
                existing_path = os.path.join(config.IMAGE_FOLDER, existing_name)

                if not os.path.isfile(existing_path):
                    continue

                if file_hash(existing_path) == incoming_hash:
                    duplicate = True
                    break

            if duplicate:
                duplicates += 1
                continue

            file.save(path)
            uploaded.append(filename)

        if uploaded or duplicates:
            parts = []

            if uploaded:
                parts.append(f"Uploaded {len(uploaded)} image(s).")

            if duplicates:
                parts.append(f"Skipped {duplicates} duplicate(s).")

            message = " ".join(parts)
        else:
            message = "No valid images uploaded."

    existing_images = sorted(
        filename
        for filename in os.listdir(config.IMAGE_FOLDER)
        if allowed_file(filename)
    )

    return render_template_string(
        PAGE,
        message=message,
        existing_images=existing_images
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
