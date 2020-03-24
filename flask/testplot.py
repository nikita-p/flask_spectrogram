import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

y, sr = librosa.load('static/Honesty.mp3')
D = np.abs(librosa.stft(y))


librosa.display.specshow(
    librosa.amplitude_to_db(D, ref=np.max), y_axis="log", x_axis="time"
)
plt.title("Power spectrogram")
plt.colorbar(format="%+2.0f dB")
plt.tight_layout()
plt.show()
