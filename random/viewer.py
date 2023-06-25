import os
import click

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.bind('<Key>', self.key_pressed)
        self.images = []
        self.current_image = 0
        self.history = []
        directory_path = filedialog.askdirectory(title="Select a directory", initialdir='../../tmp/.000')
        self.load_images(directory_path)

    def load_images(self, directory='.'):
        self.images = []
        self.current_image = 0
        self.history = []
        self.directory = directory
        for filename in os.listdir(directory):
            if filename.endswith('.gif') or filename.endswith('.png') or filename.endswith('.jpg'):
                self.images.append(Image.open(os.path.join(directory, filename)))
        if self.images:
            self.show_image()

    def show_image(self):
        image = self.images[self.current_image].resize(
            (self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.master, image=photo)
        self.label.image = photo
        self.label.pack()

    def next_image(self):
        if self.current_image < len(self.images) - 1:
            self.current_image += 1
            self.show_image()

    def prev_image(self):
        if self.current_image > 0:
            self.current_image -= 1
            self.show_image()

    def move_file(self, folder_name):
        if self.images:
            image_path = os.path.join(self.directory, os.listdir(self.directory)[self.current_image])
            folder_path = os.path.join(self.directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            os.rename(image_path, os.path.join(folder_path, os.path.basename(image_path)))
            self.history.append((image_path, folder_path))

    def undo_move(self):
        if self.history:
            image_path, folder_path = self.history.pop()
            os.rename(os.path.join(folder_path, os.path.basename(image_path)), image_path)

    def key_pressed(self, event):
        if event.char == 'd':
            self.move_file('mooi')
            self.next_image()
        elif event.char == 's':
            self.move_file('stom')
            self.next_image()
        elif event.char == 'a':
            self.prev_image()
        elif event.char == 'w':
            self.undo_move()


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
