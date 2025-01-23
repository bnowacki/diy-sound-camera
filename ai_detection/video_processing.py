import cv2
import numpy as np
import os
import math

VIDEO_IMAGE = "/ceiling/Drone_2_96000Hz_24bit_40-50s/video.mp4"
VIDEO_SOUND = "/ceiling/Drone_2_96000Hz_24bit_40-50s/frames_max_key.mp4"
CONTOUR_MIN_AREA = 300 # Area of object to detect (px)

def euclidean_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Nie udało się otworzyć wideo: {input_path}")
        return [], []

    # Setup output video writer
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    backSub = cv2.createBackgroundSubtractorMOG2()

    prev_motion_center = None
    motion_distances = []
    motion_centers = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        closest_motion_center = None
        min_motion_dist = float('inf')

        # Wykrywanie ruchu
        fg_mask = backSub.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            if cv2.contourArea(cnt) > CONTOUR_MIN_AREA:
                x, y, w, h = cv2.boundingRect(cnt)
                center = (x + w // 2, y + h // 2)
                
                if prev_motion_center is None:
                    closest_motion_center = center
                    break
                
                dist = euclidean_distance(center, prev_motion_center)
                if dist < min_motion_dist:
                    min_motion_dist = dist
                    closest_motion_center = center
        
        if closest_motion_center:
            prev_motion_center = closest_motion_center
            motion_centers.append(closest_motion_center)

            cv2.circle(frame, closest_motion_center, 5, (0, 255, 0), -1) 
            cv2.putText(frame, f"Motion: {closest_motion_center}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        

        elif prev_motion_center:
            motion_centers.append(prev_motion_center)
            motion_distances.append(min_motion_dist)

        out.write(frame)
    
    cap.release()
    out.release()
    
    # Save the motion data to a file
    np.save(output_path.replace('.mp4', '_centers.npy'), motion_centers)

    return motion_centers, motion_distances

if __name__ == "__main__":
    # Set up the paths
    input_video_image = "./videos" + VIDEO_IMAGE
    input_video_sound = "./videos" + VIDEO_SOUND

    output_video_image = "./output" + VIDEO_IMAGE
    output_video_sound = "./output" + VIDEO_SOUND

    os.makedirs(os.path.dirname(output_video_image), exist_ok=True)
    os.makedirs(os.path.dirname(output_video_sound), exist_ok=True)

    # Process both videos
    centers_image, dist_image = process_video(input_video_image, output_video_image)
    centers_sound, dist_sound = process_video(input_video_sound, output_video_sound)

    print(f"Video processing completed. Motion data saved.")
