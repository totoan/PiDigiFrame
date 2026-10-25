import os
import hashlib
from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for

import config


app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DigiFrame Upload</title>
    <style>
    body {font-family: sans-serif; padding: 16px; background: #111; color: white;}
    button {padding: 10px 16px; font-size: 16px;}
    .gallery {display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;}
    .image-card {background: #222; padding: 8px; border-radius: 8px;}
    .image-card img {width: 100%; height: 180px; object-fit: cover; border-radius: 5px;}
    .image-card button {width: 100%; margin-top: 6px;}
</style>
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

    <div class="gallery">
    {% for filename in existing_images %}
        <div class="image-card">

            <img
                src="/images/{{ filename }}"
                alt="{{ filename }}"
            >

            <form
                action="{{ url_for('delete_image', filename=filename) }}"
                method="POST"
            >
                <button type="submit">Delete</button>
            </form>

        </div>
    {% endfor %}
    </div>

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


@app.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(config.IMAGE_FOLDER, filename)


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_image(filename):
    filename = os.path.basename(filename)
    path = os.path.join(config.IMAGE_FOLDER, filename)

    if os.path.isfile(path):
        os.remove(path)

    return redirect(url_for("upload"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
