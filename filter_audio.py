# doesn't work

from scipy.signal import butter, sosfilt
from scipy.io import wavfile
import numpy as np

# Load the audio file
fs, data = wavfile.read("audio.wav")

# Ensure the audio has 8 channels
if len(data.shape) == 1:
    raise ValueError("The audio file is not multi-channel.")

num_channels = data.shape[1]  # Number of channels


# Define a band-pass filter centered around 270 Hz
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    sos = butter(order, [lowcut, highcut], btype="band", fs=fs, output="sos")
    return sosfilt(sos, data)


# Filter each channel
lowcut = 260  # Lower bound of the band
highcut = 280  # Upper bound of the band
filtered_data = np.zeros_like(data)

for channel in range(num_channels):
    filtered_data[:, channel] = bandpass_filter(data[:, channel], lowcut, highcut, fs)

# Save the filtered audio
wavfile.write("filtered_audio.wav", fs, filtered_data.astype(np.int16))
