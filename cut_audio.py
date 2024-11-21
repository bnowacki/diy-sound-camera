from scipy.io import wavfile
import numpy as np

# Load the audio file
input_file = "sawtooth.wav"
output_file = "audio.wav"
fs, data = wavfile.read(input_file)

# Determine the start and end sample indices
start_time = 10  # seconds
end_time = 28  # seconds
start_sample = int(start_time * fs)
end_sample = int(end_time * fs)

# Trim the audio data
trimmed_data = data[start_sample:end_sample]

# Save the trimmed audio
wavfile.write(output_file, fs, trimmed_data)
