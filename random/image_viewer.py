import os
import random
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

root = tk.Tk()
root.withdraw()


def get_files_by_extension(directory):
    extensions = set()
    file_list = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            extension = os.path.splitext(filename)[-1][1:].lower()
            if extension in extensions:
                file_list[extension].append(os.path.join(root, filename))
            else:
                extensions.add(extension)
                file_list[extension] = [os.path.join(root, filename)]
    return file_list


def random_filename(extension):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(12)) + '.' + extension


def move_file_to_folder(file_path, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = os.path.basename(file_path)
    new_file_name = random_filename(os.path.splitext(file_name)[-1][1:])
    new_file_path = os.path.join(folder_path, new_file_name)
    os.rename(file_path, new_file_path)
    return new_file_path


def display_image(image_path):
    img = Image.open(image_path)
    img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(image=photo)
    label.image = photo
    label.pack(fill='both', expand=True)
    return label


def undo_move_file(original_path, new_path):
    os.rename(new_path, original_path)


def main():
    directory = filedialog.askdirectory(initialdir='/Users/wouter/tmp/.000')
    image_files = get_files_by_extension(directory)
    if 'jpg' in image_files:
        file_list = image_files['jpg'] + image_files.get('png', []) + image_files.get('gif', [])
    elif 'png' in image_files:
        file_list = image_files['png'] + image_files.get('jpg', []) + image_files.get('gif', [])
    elif 'gif' in image_files:
        file_list = image_files['gif'] + image_files.get('jpg', []) + image_files.get('png', [])
    else:
        print("No image files found!")
        return

    index = 0
    while index < len(file_list):
        image_path = file_list[index]
        label = display_image(image_path)
        root.bind('<s>',
                  lambda event, image_path=image_path: move_file_to_folder(image_path, os.path.join(directory, 'stom')))
        root.bind('<d>',
                  lambda event, image_path=image_path: move_file_to_folder(image_path, os.path.join(directory, 'mooi')))
        root.bind('<w>',
                  lambda event, original_path=image_path, new_path=label: undo_move_file(original_path, new_path))
        root.bind('<Right>', lambda event: label.pack_forget() or root.quit())
        root.bind('<Escape>', lambda event: root.quit())
        root.mainloop()
        index += 1


if __name__ == '__main__':
    main()
