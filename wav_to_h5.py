from scipy.io import wavfile
import tables

print("Converting WAV to H5...")


WAV = "./input_data/audio.wav"

print("Loading wav file: ", WAV)

# read data from wav
fs, data = wavfile.read(WAV)

# ouput
folder = "./output/"
name = "audio.h5"

print("Saving h5 file: ", folder + name)

# save_to acoular h5 format
acoularh5 = tables.open_file(folder + name, mode="w")
acoularh5.create_earray(
    "/",
    "time_data",
    atom=None,
    title="",
    filters=None,
    expectedrows=100000,
    chunkshape=[256, 64],
    byteorder=None,
    createparents=False,
    obj=data,
)
acoularh5.set_node_attr("/time_data", "sample_freq", fs)
acoularh5.close()

print("H5 file saved to: ", folder + name)
