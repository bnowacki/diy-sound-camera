
import json
from beamform import cacht, rg  # cached results and grid from beamform.py
import numpy as np

output_json_path = "./output/drone_coordinates.json"

def get_coordinates(cacht, grid):
    coordinates = []

    for frame in cacht.result(1):
        prob_map = np.array(frame[0]).reshape(grid.shape)

        # position where probabiliti is maximal
        max_idx = np.unravel_index(np.argmax(prob_map), prob_map.shape)

        # map index to pixel coordinates
        x_coordinate = int(max_idx[0])
        y_coordinate = int(max_idx[1])

        # append the coordinates for this frame
        coordinates.append({"x": x_coordinate, "y": y_coordinate})

    return coordinates


print("Extracting coordinates...")
coordinates = get_coordinates(cacht, rg)

print(f"Saving 2D coordinates to {output_json_path}...")
with open(output_json_path, "w") as json_file:
    json.dump(coordinates, json_file, indent=4)

print(f"2D coordinates saved successfully to {output_json_path}")
