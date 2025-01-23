import numpy as np
import math
import matplotlib.pyplot as plt
import os

def euclidean_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def calculate_statistics(centers_image, centers_sound):
    x_diff = np.array([abs(centers_image[i][0] - centers_sound[i][0]) for i in range(len(centers_image))])
    y_diff = np.array([abs(centers_image[i][1] - centers_sound[i][1]) for i in range(len(centers_image))])
    euclidean_diff = np.array([euclidean_distance(centers_image[i], centers_sound[i]) for i in range(len(centers_image))])

    stats = {
        'x_distance_mean': np.mean(x_diff),
        'x_distance_std': np.std(x_diff),
        'x_distance_min': np.min(x_diff),
        'x_distance_max': np.max(x_diff),

        'y_distance_mean': np.mean(y_diff),
        'y_distance_std': np.std(y_diff),
        'y_distance_min': np.min(y_diff),
        'y_distance_max': np.max(y_diff),

        'distance_mean': np.mean(euclidean_diff),
        'distance_std': np.std(euclidean_diff),
        'distance_min': np.min(euclidean_diff),
        'distance_max': np.max(euclidean_diff),
    }

    return stats

def plot_statistics(x_diff, y_diff, euclidean_diff):
    time = np.arange(len(x_diff))

    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(time, x_diff)
    plt.xlabel("Time (frames)")
    plt.ylabel("X Difference (px)")

    plt.subplot(3, 1, 2)
    plt.plot(time, y_diff)
    plt.xlabel("Time (frames)")
    plt.ylabel("Y Difference (px)")

    plt.subplot(3, 1, 3)
    plt.plot(time, euclidean_diff)
    plt.xlabel("Time (frames)")
    plt.ylabel("Euclidean Distance(px)")

    plt.tight_layout()

    os.makedirs("./output/images", exist_ok=True)
    plt.savefig("./output/images/statistics_plot.png")
    plt.close()

def plot_drone_positions(centers_image, centers_sound):
    plt.figure(figsize=(10, 6))

    image_x = [center[0] for center in centers_image]
    image_y = [center[1] for center in centers_image]

    sound_x = [center[0] for center in centers_sound]
    sound_y = [center[1] for center in centers_sound]

    norm = plt.Normalize(0, len(centers_image) - 1)
    cmap = plt.get_cmap('Greens')
    image_colors = [cmap(norm(i)) for i in range(len(centers_image))]

    cmap = plt.get_cmap('Reds')
    sound_colors = [cmap(norm(i)) for i in range(len(centers_sound))]

    for i in range(1, len(centers_image)):
        plt.plot([image_x[i-1], image_x[i]], [image_y[i-1], image_y[i]], color=image_colors[i], lw=2)
        
        plt.plot([sound_x[i-1], sound_x[i]], [sound_y[i-1], sound_y[i]], color=sound_colors[i], lw=2)


    plt.gca().invert_yaxis()

    plt.xlabel("X Position (px)")
    plt.ylabel("Y Position (px)")
    plt.title("Drone Positions Based on Centers (Image vs Sound)")

    plt.tight_layout()

    os.makedirs("./output/images", exist_ok=True)
    plt.savefig("./output/images/drone_positions.png")
    plt.close()


def save_statistics(stats):
    os.makedirs("./output/measurements", exist_ok=True)
    with open("./output/measurements/statistics.txt", "w") as f:
        f.write("Statistics for center differences:\n\n")
        
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

def main():
    centers_image = np.load("./output/ceiling/Drone_2_96000Hz_24bit_40-50s/video_centers.npy")
    centers_sound = np.load("./output/ceiling/Drone_2_96000Hz_24bit_40-50s/frames_max_key_centers.npy")

    min_length = min(len(centers_image), len(centers_sound))
    centers_image = centers_image[:min_length]
    centers_sound = centers_sound[:min_length]

    stats = calculate_statistics(centers_image, centers_sound)

    print("Statistics for center differences:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    x_diff = np.array([abs(centers_image[i][0] - centers_sound[i][0]) for i in range(min_length)])
    y_diff = np.array([abs(centers_image[i][1] - centers_sound[i][1]) for i in range(min_length)])
    euclidean_diff = np.array([euclidean_distance(centers_image[i], centers_sound[i]) for i in range(min_length)])

    plot_statistics(x_diff, y_diff, euclidean_diff)
    plot_drone_positions(centers_image, centers_sound)
    save_statistics(stats)

if __name__ == "__main__":
    main()
