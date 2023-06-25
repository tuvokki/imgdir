import os
import random
import json
import string

import click
import tkinter as tk
from tkinter import filedialog

allowed_extensions = [
    '.jpg',
    '.jpeg',
    '.png',
    '.mp4',
    '.avi',
    '.mov',
]


def move_files_to_subdirs(directory):
    extensions = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.startswith('.'):
                extension = os.path.splitext(file)[1]
                extensions.add(extension)

    for extension in extensions:
        extension_dir = os.path.join(directory, extension[1:])
        if not os.path.exists(extension_dir):
            os.makedirs(extension_dir)

    new_names = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.startswith('.'):
                src = os.path.join(root, file)
                extension = os.path.splitext(file)[1]
                dst = os.path.join(directory, extension[1:], ''.join(
                    random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12)) + extension)
                os.rename(src, dst)
                new_names.setdefault(extension, []).append(os.path.basename(dst))
    return new_names


def get_files_by_extension(directory):
    """
    Return a dictionary with extensions as keys and sets of file paths as values.
    """
    file_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            if extension not in allowed_extensions:
                continue
            if extension not in file_dict:
                file_dict[extension] = set()
            file_dict[extension].add(file_path)
    return file_dict


def randomize_filenames(files_by_extension):
    for extension in files_by_extension:
        random.shuffle(files_by_extension[extension])
        for i, file_path in enumerate(files_by_extension[extension]):
            extension_prefix = f"{extension}_"
            new_filename = f"{extension_prefix}{i}.{extension}"
            try:
                os.rename(file_path, os.path.join(os.path.dirname(file_path), new_filename))
                files_by_extension[extension][i] = os.path.join(os.path.dirname(file_path), new_filename)
            except FileNotFoundError:
                print(f"File {new_filename} not found")


def get_image_data(image_path):
    from PIL import Image
    with Image.open(image_path) as img:
        width, height = img.size
        resolution = img.info.get('dpi')
        mode = img.mode
        return {"width": width, "height": height, "resolution": resolution, "mode": mode}


def get_video_data(video_path):
    import cv2
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    encoder = cap.get(cv2.CAP_PROP_FOURCC)
    cap.release()
    return {"fps": fps, "frame_count": frame_count, "encoder": encoder}


@click.command()
def main():
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory(title="Select a directory", initialdir='../../tmp/rips')

    # files_by_extension = get_files_by_extension(directory_path)
    files_by_extension = move_files_to_subdirs(directory_path)
    randomize_filenames(files_by_extension)

    image_data = {}
    video_data = {}

    for image_path in files_by_extension.get("jpg", []) + files_by_extension.get("jpeg", []) + files_by_extension.get(
            "png", []):
        image_data[image_path] = get_image_data(image_path)

    for video_path in files_by_extension.get("mp4", []) + files_by_extension.get("avi", []) + files_by_extension.get(
            "mov", []):
        video_data[video_path] = get_video_data(video_path)

    data = []
    for extension in files_by_extension:
        for file_path in files_by_extension[extension]:
            data.append({
                "filename": os.path.basename(file_path),
                "type": extension,
                "size": os.path.getsize(file_path),
                **image_data.get(file_path, {}),
                **video_data.get(file_path, {})
            })

    # with open(os.path.join(dire