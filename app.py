from flask import Flask, render_template, Response, request, redirect, url_for
import librosa
import librosa.display
import numpy as np

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(["mp3", "wav"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def hello():
    y, sr = librosa.load(librosa.util.example_audio_file())
    return "Hello World!"


if __name__ == "__main__":
    app.run()
