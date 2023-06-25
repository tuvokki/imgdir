import shutil

import cv2
import os
import click
import json


@click.command()
@click.option('--input-dir', '-i', required=True, help='Input directory containing images')
@click.option('--output-file', '-o', required=True, help='Output JSON file path')
def extract_face_features(input_dir, output_file):
    results_dir = os.path.join(input_dir, "../..", 'results')
    if os.path.isdir(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    data = {}
    for subdir, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_path = os.path.join(subdir, file)
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if len(faces) == 0:
                    continue
                faces_data = []
                for (x, y, w, h) in faces:
                    faces_data.append({'x': x, 'y': y, 'width': w, 'height': h})
                    # Draw bounding box on the image
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # result = {'file': filename, 'faces': faces_data}
                    # results.append(result)

                    roi = gray[y:y + h, x:x + w]
                    features = {"age": 0, "ethnicity": "", "pose": ""}
                    # Hier kan je code plaatsen om de gezichtskenmerken uit de ROI te halen.
                    # Bijvoorbeeld: features["age"] = get_age(roi)
                    # Bijvoorbeeld: features["ethnicity"] = get_ethnicity(roi)
                    # Bijvoorbeeld: features["pose"] = get_pose(roi)
                    data[image_path] = features

                    # Save the image with bounding boxes
                    result_path = os.path.join(results_dir, subdir, file)
                    os.makedirs(os.path.dirname(result_path), exist_ok=True)
                    cv2.imwrite(result_path, image)
                features
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Gezichtskenmerken zijn opgeslagen in {output_file}")


if __name__ == '__main__':
    extract_face_features()
