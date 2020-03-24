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
    y, sr = librosa.load(UPLOAD_FOLDER + "/" + filename)
    D = np.abs(librosa.stft(y))
    pngImageB64String = plot_image(D)
    return render_template("template.html", name=filename, url=pngImageB64String)
    # return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.listdir())
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # return redirect(url_for("plotView", filename=filename))
            return redirect(url_for("uploaded_file", filename=filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """


def plot_image(D):
    # Generate plot
    fig = plt.figure()
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


@app.route("/plot")
def plotView(filename):
    y, sr = librosa.load(filename)
    D = np.abs(librosa.stft(y))
    pngImageB64String = plot_image(D)
    return render_template("template.html", name=filename, url=pngImageB64String)


if __name__ == "__main__":
    app.run()
