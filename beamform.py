import acoular as ac
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("\n=== Beginning beamforming ===\n")

# Setup microphones

r = 0.131  # microphones are set up in a regular octagon with a side equal 10cm

print("Microphones radius: ", r)

mg = ac.MicGeom()
mg.mpos_tot = np.array(
    [
        (
            r * np.sin(2 * np.pi * i + np.pi / 4),
            r * np.cos(2 * np.pi * i + np.pi / 4),
            0,
        )
        for i in np.linspace(0.0, 1.0, 8, False)
    ],
).T
# Shift positions counter-clockwise by one step
mg.mpos_tot = np.roll(mg.mpos_tot, shift=1, axis=1)

# Load sound file


datafile = "./output/audio.h5"

print("Loading audio data from: ", datafile)

# We start with making the data from the HDF5 file available and create and instance of TimeSamples
ts = ac.TimeSamples(name=datafile)
print("Number of channels: ", ts.numchannels)
print("Number of time data samples: ", ts.numsamples)
print("Sample freq: ", ts.sample_freq)
print("Length in seconds: ", ts.numsamples / ts.sample_freq)

# we create a RectGrid object, which provides possible source positions in a regular, two-dimensional grid with rectangular shape:
rg = ac.RectGrid(x_min=-0.4, x_max=0.4, y_min=-0.4, y_max=0.4, z=0.4, increment=0.005)
print("Rect size: ", rg.size)

# The sound propagation model (including the source model and transfer path) is contained in a SteeringVector object,
# which is given the focus grid and microphone arrangement to calculate the steering vector, which also contains a weighting of the transfer functions from grid points to microphone positions:
st = ac.SteeringVector(grid=rg, mics=mg)


# Fixed focus time domain beamforming

FPS = 30
frames_count = int(ts.numsamples / ts.sample_freq * FPS)
print("Frames to be generated: ", frames_count)


fi = ac.FiltFiltOctave(source=ts, band=1000, fraction="Third octave")
bt = ac.BeamformerTimeSq(source=fi, steer=st, r_diag=True)
avgt = ac.Average(source=bt, naverage=int(ts.sample_freq / FPS))
cacht = ac.Cache(source=avgt)  # cache to prevent recalculation


# Create figure for animation
fig, ax = plt.subplots(figsize=(8, 8))

# Remove margins and axes
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


def init():
    ax.clear()
    ax.axis("off")


i = 0

print()


# Animation function
def update(frame):
    global i
    i += 1
    print(f"\rFrame {i}/{frames_count}", end="", flush=True)
    res = np.array(frame[0]).reshape(rg.shape)
    mx = ac.L_p(res.max())
    ax.clear()  # Clear previous plot
    ax.imshow(
        ac.L_p(np.transpose(res)),
        vmax=mx,
        vmin=mx - 3,
        cmap="turbo",
        interpolation="nearest",
        extent=rg.extend(),
        origin="lower",
    )


# Prepare frames
frames = list(cacht.result(1))

ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, repeat=False)

# Save as video
ani.save("./output/frames.mp4", writer="ffmpeg", fps=FPS)  # Adjust FPS as needed

print("Video saved as './output/frames.mp4'")

print("\n=== Beginning done ===\n")
