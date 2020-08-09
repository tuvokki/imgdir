import os
import shutil
from glob import glob
from pathlib import Path
from tkinter import *
# pip install pillow
from tkinter import filedialog

from PIL import Image, ImageTk

import config

ARROWS = {
    8124162: 'LEFT',
    8189699: 'RIGHT',
    8320768: 'UP',
    8255233: 'DOWN',
    7730984: 'DELETE',
    3342463: 'DELETE',
    2031727: 'OPEN',
    32: 'FIGURE'
}


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.figure_dir = os.path.join(Path.home(), 'Pictures', 'Figures', 'new')
        self.initial_dir = os.path.join(Path.home(), 'Pictures', 'wallpaper', 'new')
        self.master = master
        self.master.bind("<Key>", self.key_pressed)
        self.var = StringVar()
        self.var.set(f'no images')
        self.pack(fill=BOTH, expand=1)
        self.screen_padding = 10
        self._geom = '200x200+0+0'
        self.img_loaded = 0
        self.showing = None
        self.image_list = []
        self.img_loaded = 0
        self.reverse_next = False
        self.type_list = ['jpg', 'jpeg', 'png']
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.master.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.master.wm_title("Img dir")
        self.master.update()
        # Ask the user to select a folder.
        self.open_folder()

    def load_snake(self, file_name=None):
        try:
            image = Image.open(file_name)
        except AttributeError:
            return None

        title = file_name.split('/')[-1]
        if len(title) > 60:
            title = f"{title[0:60]}..."
        title += f" ({self.img_loaded + 1}/{len(self.image_list)})"
        if self.img_loaded + 1 == len(self.image_list):
            title += " ✔"

        self.master.wm_title(title)

        ratio = min(self.master.winfo_width() / image.width, self.master.winfo_height() / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))

        try:
            image = image.resize(new_size)
            render = ImageTk.PhotoImage(image)
            img = Label(self, image=render)
            img.image = render

            x = (self.master.winfo_width() - image.width) / 2
            y = (self.master.winfo_height() - image.height) / 2
            img.place(x=x, y=y)

            if self.showing:
                self.showing.destroy()
            self.showing = img
        except OSError as e:
            print(f'Image {file_name} could not be loaded. {e}')
            pass
        root.focus_force()

    def key_pressed(self, event):
        key_pressed = ARROWS.get(event.keycode, "UNKNOWN")
        print(f'Arrow pressed {event.keycode}: {key_pressed}')
        if key_pressed == 'RIGHT':
            if config.SORT_MODE:
                copy_file = self.image_list[self.img_loaded]
                shutil.copy(copy_file, self.done_folder)
                print(f"Copied: {copy_file}.")
                # del self.image_list[self.img_loaded]
            self.img_loaded += 1
            self.reverse_next = False
        elif key_pressed == 'LEFT':
            self.img_loaded -= 1
            self.reverse_next = True
        elif key_pressed == 'DELETE':
            delete_file = self.image_list[self.img_loaded]
            if config.SORT_MODE:
                try:
                    shutil.move(delete_file, self.dump_folder)
                except shutil.Error:
                    shutil.rmtree(delete_file)
                print(f"Deleted: {delete_file}.")
                del self.image_list[self.img_loaded]
            else:
                try:
                    os.remove(delete_file)
                    print(f"Deleted: {delete_file}.")
                except OSError as e:
                    # TODO: als image niet geladen kan worden delete / kopieer naar 'trash'
                    print(f"Error: {e.filename} - {e.strerror}.")
                finally:
                    del self.image_list[self.img_loaded]
            if self.reverse_next:
                self.img_loaded -= 1
        elif key_pressed == 'UP':
            self.img_loaded = 0
        elif key_pressed == 'DOWN':
            self.img_loaded = len(self.image_list) - 1
        elif key_pressed == 'OPEN':
            self.open_folder()
        elif key_pressed == 'FIGURE':
            figure_file = self.image_list[self.img_loaded]
            try:
                shutil.move(figure_file, self.figure_dir)
            except shutil.Error as e:
                print(f"Error moving {figure_file} to {self.figure_dir}. {e}")
            print(f"Moved {figure_file} to {self.figure_dir}.")
            del self.image_list[self.img_loaded]

        # Make sure to always have a valid image to load
        # TODO: exit sequence if image_list is empty
        if self.img_loaded < 0:
            self.img_loaded = 0
        elif self.img_loaded > len(self.image_list) - 1:
            self.img_loaded = len(self.image_list) - 1

        self.load_snake(self.image_list[self.img_loaded])

    def mk_dump_dirs(self):
        Path(self.dump_folder).mkdir(parents=True, exist_ok=True)
        Path(self.done_folder).mkdir(parents=True, exist_ok=True)
        Path(self.film_folder).mkdir(parents=True, exist_ok=True)
        Path(self.gifs_folder).mkdir(parents=True, exist_ok=True)

    def clean_crap(self, base_dir):
        movs = glob(f'{base_dir}/*.mp4')
        for filename in movs:
            shutil.move(filename, self.film_folder)
            print(f"Crapped: {filename}.")

        movs = glob(f'{base_dir}/*.webm')
        for filename in movs:
            shutil.move(filename, self.film_folder)
            print(f"Crapped: {filename}.")

        gifs = glob(f'{base_dir}/*.gif')
        for filename in gifs:
            shutil.move(filename, self.gifs_folder)
            print(f"Crapped: {filename}.")

    def check_done(self) -> str:
        # files = glob(f'{self.done_folder}/*')
        # latest_file = max(files, key=os.path.getctime)
        file_list = [glob(f'{self.done_folder}/*.{t}') for t in self.type_list]
        flat_list = sorted(item for sublist in file_list for item in sublist)
        if len(flat_list) > 0:
            return f"{flat_list[len(flat_list) - 1]}"
        else:
            return ""

    def open_folder(self):
        if not self.initial_dir:
            self.initial_dir = Path.home()
        base_dir = filedialog.askdirectory(parent=root,
                                           initialdir=self.initial_dir,
                                           title="Please select a folder:")

        if base_dir:
            # sub_dirs = set([os.path.dirname(p) for p in glob(f"{base_dir}/*/*")])
            self.dump_folder = os.path.join(base_dir, 'dump')
            self.done_folder = os.path.join(base_dir, 'done')
            self.film_folder = os.path.join(base_dir, 'movs')
            self.gifs_folder = os.path.join(base_dir, 'gifs')
            self.image_list = []

            self.mk_dump_dirs()
            self.clean_crap(base_dir)
            file_list = [glob(f'{base_dir}/*.{t}') for t in self.type_list]
            flat_list = sorted(item for sublist in file_list for item in sublist)

            self.var.set(f'{len(flat_list)} images')

            for filename in flat_list:
                self.image_list.append(filename)

            last_loaded = self.check_done()
            if len(last_loaded) > 0:
                self.img_loaded = self.image_list.index(last_loaded.replace('/done', ''))
            else:
                self.img_loaded = 0
            if len(self.image_list) > 0:
                self.load_snake(self.image_list[self.img_loaded])
        else:
            # end program when no directory is selected
            print('No dir selected, bye.')
            exit(0)


root = Tk()
app = Window(root)
root.mainloop()
