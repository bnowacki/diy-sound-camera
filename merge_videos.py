from moviepy.editor import VideoFileClip, CompositeVideoClip

print("=== Merging videos ===")

BACKGROUND_VIDEO = "./input_data/sawtooth-short_10_28.mp4"
OVERLAY_VIDEO = "./output/frames.mp4"

# Load the background video
background = VideoFileClip(BACKGROUND_VIDEO)

# Load the overlay video
overlay = VideoFileClip(OVERLAY_VIDEO).set_opacity(0.5)  # Resize overlay if needed

# Position the overlay (e.g., top-left corner)
overlay = overlay.set_position(("center", "center"))

# Combine the two videos
composite = CompositeVideoClip([background, overlay])

# Set the duration to match the background video
composite = composite.set_duration(background.duration)

# Write the output video
composite.write_videofile("./output/merged.mp4", codec="libx264")
