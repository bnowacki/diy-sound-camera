import json
from beamform import cacht, rg  # cached results and grid from beamform.py
import numpy as np

output_json_path = "./output/drone_coordinates.json"

def extract_coordinates(cacht, grid, p_x=0, p_y=0, scale_factor=1.0):
    """
    Extracts the coordinates with the highest probability and applies translation and scaling.

    Parameters:
    - cacht: Cached results from Acoular.
    - grid: RectGrid object used for beamforming.
    - p_x: Horizontal translation in pixels (default: 0).
    - p_y: Vertical translation in pixels (default: 0).
    - scale_factor: Scaling factor for the coordinates (default: 1.0).

    Returns:
    - List of adjusted coordinates as dictionaries with 'x' and 'y' keys.
    """
    coordinates = []

    for frame in cacht.result(1):
        prob_map = np.array(frame[0]).reshape(grid.shape)

        # position where probabiliti is maximal
        max_idx = np.unravel_index(np.argmax(prob_map), prob_map.shape)

        # map index to pixel coordinates
        x_coord = int(max_idx[0])
        y_coord = int(max_idx[1])

        # scaling and translation
        adjusted_x = int((x_coord * scale_factor) + p_x)
        adjusted_y = int((y_coord * scale_factor) + p_y)

        coordinates.append({"x": adjusted_x, "y": adjusted_y})

    return coordinates

# parameters for alignment
p_x = 96      # horizontal shift in pixels
p_y = 29      # vertical shift in pixels
scale_factor = 1.44  # scaling factor

print("Extracting 2D coordinates...")
coordinates = extract_coordinates(cacht, rg, p_x=p_x, p_y=p_y, scale_factor=scale_factor)

print(f"Saving 2D coordinates to {output_json_path}...")
with open(output_json_path, "w") as json_file:
    json.dump(coordinates, json_file, indent=4)

print(f"2D coordinates saved successfully to {output_json_path}")
