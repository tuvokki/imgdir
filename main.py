from glob import glob
import os
from pathlib import Path
from tkinter import *

# pip install pillow
from tkinter import filedialog

from PIL import Image, ImageTk

# ARROWS = (8320768, 8124162, 8255233, 8189699)
ARROWS = {
    8124162: 'LEFT',
    8189699: 'RIGHT',
    8320768: 'UP',
    8255233: 'DOWN',
    7730984: 'DELETE',
}


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.bind("<Escape>", self.toggle_geom)
        self.master.bind("<Key>", self.key_pressed)
        self.pack(fill=BOTH, expand=1)
        self.screen_padding = 10
        self._geom = '200x200+0+0'
        self.img_loaded = 0

        self.screen_width = master.winfo_screenwidth() - 10 * self.screen_padding
        self.screen_height = master.winfo_screenheight() - 10 * self.screen_padding
        root.geometry(f"{self.screen_width}x{self.screen_height}+{3 * self.screen_padding}+{3 * self.screen_padding}")

        # Build a list of tuples for each file type the file dialog should display
        my_filetypes = [('all files', '.*'), ('text files', '.txt')]

        # Ask the user to select a folder.
        answer = filedialog.askdirectory(parent=root,
                                         initialdir=Path.home(),
                                         title="Please select a folder:")
        # TODO: answer can be None
        self.image_list = []
        type_list = ['jpg', 'jpeg', 'png']
        file_list = [glob(f'{answer}/*.{t}') for t in type_list]
        flat_list = [item for sublist in file_list for item in sublist]

        for filename in flat_list:
            im = Image.open(filename)
            self.image_list.append(im)
        self.load_snake(self.image_list[self.img_loaded])

    def load_snake(self, image=None):
        if not image:
            load = Image.open("Aztec_Xuicoatl.jpg")
        else:
            load = image
        newsize = (self.screen_width - self.screen_padding, self.screen_height - self.screen_padding)
        try:
            load = load.resize(newsize)
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=self.screen_padding, y=self.screen_padding)
        except OSError as e:
            print(f'Image {image.filename} could not be loaded.')
            pass
        root.focus_force()

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

    def key_pressed(self, event):
        print(f'Arrow pressed {event.keycode}: {ARROWS.get(event.keycode,"UNKNOWN")}')
        if ARROWS.get(event.keycode,"UNKNOWN") == 'RIGHT':
            self.img_loaded += 1
        elif ARROWS.get(event.keycode,"UNKNOWN") == 'LEFT':
            self.img_loaded -= 1
        if ARROWS.get(event.keycode, "UNKNOWN") == 'DELETE':
            try:
                delete_file = self.image_list[self.img_loaded].filename
                os.remove(delete_file)
                print(f"Deleted: {delete_file}.")
            except OSError as e:
                # TODO: als image niet geladen kan worden delete / kopieer naar 'trash'
                print(f"Error: {e.filename} - {e.strerror}.")
            finally:
                del self.image_list[self.img_loaded]
                self.img_loaded += 1

        # Make sure to always have a valid image to load
        # TODO: exit sequence if image_list is empty
        if self.img_loaded < 0:
            self.img_loaded = 0
        elif self.img_loaded >= len(self.image_list)-1:
            self.img_loaded = len(self.image_list)-1

        self.load_snake(self.image_list[self.img_loaded])


root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.mainloop()
