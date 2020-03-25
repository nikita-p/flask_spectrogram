from flask import Flask, render_template, Response, request, redirect, url_for
import io
import os
import base64
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from flask import send_from_directory
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pydub import AudioSegment
from tempfile import mktemp

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(["mp3", "wav"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/page")
def hello():
    return "Hello World!"


@app.route("/<filename>")
def uploaded_file(filename):
    path_to_file = UPLOAD_FOLDER + "/" + filename
    print("My path:", path_to_file)
    print("Folders:", os.listdir())
    print("F static:", os.listdir("./static"))
    if path_to_file[-3:].lower() == "mp3":
        mp3_audio = AudioSegment.from_mp3(path_to_file)
        os.remove(path_to_file)
        wname = path_to_file + ".wav"
    if path_to_file[-3:].lower() == "wav":
        wname = path_to_file
    print("W  path:", wname)
    mp3_audio.export(wname, format="wav")
    y, sr = librosa.load(wname)
    os.remove(wname)
    D = np.abs(librosa.stft(y))
    pngImageB64String = plot_image(D)
    return render_template("template.html", name=filename, url=pngImageB64String)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(os.listdir())
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # return redirect(url_for("plotView", filename=filename))
            return redirect(url_for("uploaded_file", filename=filename))
    return render_template("template_start.html")


def plot_image(D):
    # Generate plot
    fig = plt.figure(figsize=(8, 4.5))
    librosa.display.specshow(
        librosa.amplitude_to_db(D, ref=np.max), y_axis="log", x_axis="time"
    )
    plt.title("Power spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode("utf8")
    return pngImageB64String


@app.route("/example")
def plotView():
    path_to_file = "static/example37646823.mp3"
    print("Folders:", os.listdir())
    print("F static:", os.listdir("./static"))
    mp3_audio = AudioSegment.from_file(path_to_file, format="mp3")
    wname = path_to_file + ".wav"
    print("W  path:", wname)
    mp3_audio.export(wname, format="wav")
    y, sr = librosa.load(wname)
    os.remove(wname)
    D = np.abs(librosa.stft(y))
    pngImageB64String = plot_image(D)
    return render_template("template.html", name="Example.mp3", url=pngImageB64String)


if __name__ == "__main__":
    app.run()
