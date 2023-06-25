#!/Users/wouter/projects/imgdir/.venv/bin/python
import functools
import os
import random
import shutil
from glob import glob
from pathlib import Path
import tkinter
from tkinter import filedialog
import argparse

# pip install pillow
from PIL import Image, ImageTk

import config
from constants import ARROWS


class Window(tkinter.Frame):
    def __init__(self, master=None):
        parser = argparse.ArgumentParser()
        parser.add_argument("--dir", help="Initial directory")
        parser.add_argument("--done", action=argparse.BooleanOptionalAction)
        parser.add_argument("--random", action=argparse.BooleanOptionalAction)
        args = parser.parse_args()

        tkinter.Frame.__init__(self, master)
        self.figure_dir = os.path.join(Path.home(), 'Pictures', 'Figures')
        if args.dir:
            self.initial_dir = os.path.join(args.dir)
        else:
            self.initial_dir = os.path.join(Path.home(), 'tmp')
        self.is_done = args.done
        self.is_random = args.random
        self.master = master
        if self.is_done:
            self.master.bind("<Key>", self.simple_key_pressed)
        else:
            self.master.bind("<Key>", self.key_pressed)
        self.var = tkinter.StringVar()
        self.var.set(f'no images')
        self.pack(fill=tkinter.BOTH, expand=1)
        self.screen_padding = 10
        self._geom = '200x200+0+0'
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
        self.last_action = None

    def load_snake(self, file_name=None):
        try:
            image = Image.open(file_name)
        except AttributeError:
            return None

        title = Path(file_name).name
        ripname = Path(file_name).parent.name
        if Path(file_name).parent.name is 'done':
            title = '+' + title
            ripname = Path(file_name).parent.parent.name
        if len(title) > 60:
            title = f"{title[0:60]}..."
        title += f" ({self.img_loaded + 1}/{len(self.image_list)})"
        if self.img_loaded + 1 == len(self.image_list):
            title += " ✔"

        self.master.wm_title(f"{title}  --  {ripname}")

        ratio = min(self.master.winfo_width() / image.size[0], self.master.winfo_height() / image.size[1])
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))

        try:
            image = image.resize(new_size)
            render = ImageTk.PhotoImage(image)
            img = tkinter.Label(self, image=render)
            img.image = render

            x = (self.master.winfo_width() - image.size[0]) / 2
            y = (self.master.winfo_height() - image.size[1]) / 2
            img.place(x=x, y=y)

            if self.showing:
                self.showing.destroy()
            self.showing = img
        except OSError as e:
            print(f'Image {file_name} could not be loaded. {e}')
            pass
        root.focus_force()

    def simple_key_pressed(self, event):
        key_pressed = ARROWS.get(event.keycode, "UNKNOWN")
        if config.DEBUG:
            print(f'Arrow pressed {event.keycode}: {key_pressed}')

        if key_pressed == 'LEFT':
            self.img_loaded -= 1
            self.reverse_next = True
        elif key_pressed == 'QUIT':
            exit(0)
        else:
            self.img_loaded += 1
            self.reverse_next = False

        if self.img_loaded < 0:
            self.img_loaded = 0
        elif self.img_loaded > len(self.image_list) - 1:
            self.img_loaded = len(self.image_list) - 1

        self.load_snake(self.image_list[self.img_loaded])

    def key_pressed(self, event):
        key_pressed = ARROWS.get(event.keycode, "UNKNOWN")
        if config.DEBUG:
            print(f'Arrow pressed {event.keycode}: {key_pressed}')
        if key_pressed == 'QUIT':
            exit(0)
        if key_pressed == 'UNDO':
            if self.last_action['type'] == 'done':
                self.img_loaded = self.img_loaded - 1
                self.image_list[self.img_loaded] = shutil.move(self.image_list[self.img_loaded], self.base_dir)
            if self.last_action['type'] == 'dump':
                self.img_loaded = self.img_loaded - 1
                self.image_list.insert(self.img_loaded, shutil.move(
                    os.path.join(self.dump_folder, os.path.basename(self.last_action['file'])), self.base_dir))
        if key_pressed == 'RIGHT':
            if config.SORT_MODE:
                copy_file = self.image_list[self.img_loaded]
                if not self.done_folder in copy_file:
                    self.last_action = {'type': 'done', 'file': copy_file, 'to': self.done_folder}
                    self.image_list[self.img_loaded] = shutil.move(copy_file, self.done_folder)
                    if config.DEBUG:
                        print(f"Copied: {copy_file}.")
            self.img_loaded += 1
            self.reverse_next = False
        elif key_pressed == 'LEFT':
            self.img_loaded -= 1
            self.reverse_next = True
        elif key_pressed == 'DELETE':
            delete_file = self.image_list[self.img_loaded]
            if config.SORT_MODE:
                try:
                    self.last_action = {'type': 'dump', 'file': delete_file, 'to': self.dump_folder}
                    shutil.move(delete_file, self.dump_folder)
                except shutil.Error:
                    shutil.rmtree(delete_file)
                if config.DEBUG:
                    print(f"Deleted: {delete_file}.")
                del self.image_list[self.img_loaded]
            else:
                try:
                    self.last_action = {'type': 'del', 'file': delete_file, 'to': None}
                    os.remove(delete_file)
                    if config.DEBUG:
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
            if not config.BROWSE_MODE:
                figure_file = self.image_list[self.img_loaded]
                try:
                    shutil.move(figure_file, self.figure_dir)
                except shutil.Error:
                    print(f"Error moving {figure_file} to {self.figure_dir}.")
                if config.DEBUG:
                    print(f"Moved {figure_file} to {self.figure_dir}.")
                del self.image_list[self.img_loaded]
            else:
                self.img_loaded += 1
                self.reverse_next = False

        if len(self.image_list) == self.img_loaded:
            Path(f"{Path(self.base_dir).parent}/zz/").mkdir(parents=True, exist_ok=True)
            os.rename(self.base_dir, f"{Path(self.base_dir).parent}/zz/{Path(self.base_dir).name}")
            self.img_loaded = 0
            next_dir = sorted(d for d in Path(self.base_dir).parent.iterdir() if d.is_dir())[0]
            if next_dir == Path(self.base_dir).parent.joinpath("zz"):
                return
            self.base_dir = next_dir
            self.prepare_folder()
            return

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

    def sort_files_by_type(self):
        movs = glob(f'{self.base_dir}/*.mp4')
        for filename in movs:
            shutil.move(filename, self.film_folder)
            if config.DEBUG:
                print(f"Crapped: {filename}.")

        movs = glob(f'{self.base_dir}/*.webm')
        for filename in movs:
            shutil.move(filename, self.film_folder)
            if config.DEBUG:
                print(f"Crapped: {filename}.")

        gifs = glob(f'{self.base_dir}/*.gif')
        for filename in gifs:
            shutil.move(filename, self.gifs_folder)
            if config.DEBUG:
                print(f"Crapped: {filename}.")

    def done_files(self) -> list:
        file_list = [glob(f'{self.done_folder}/*.{t}') for t in self.type_list]
        flat_list = sorted(item for sublist in file_list for item in sublist)
        return flat_list

    def open_folder(self):
        if not self.initial_dir:
            self.initial_dir = Path.home()
        self.base_dir = filedialog.askdirectory(parent=root,
                                                initialdir=self.initial_dir,
                                                title="Please select a folder:")
        self.prepare_folder()

    def prepare_folder(self):
        def list_sorter(a, b):
            if os.path.basename(a) < os.path.basename(b):
                return -1
            if os.path.basename(a) > os.path.basename(b):
                return 1
            else:
                return 0

        if not self.base_dir:
            # end program when no directory is selected
            print('No dir selected, bye.')
            exit(0)

        self.image_list = []
        file_list = [glob(f'{self.base_dir}/*.{t}') for t in self.type_list]
        flat_list = sorted(item for sublist in file_list for item in sublist)
        self.var.set(f'{len(flat_list)} images')

        if self.is_done:
            # only done files in all subdirs
            self.initial_dir = Path(self.base_dir)

            self.image_list = sorted(flat_list, key=functools.cmp_to_key(list_sorter))
            if self.is_random:
                random.shuffle(self.image_list)

            self.img_loaded = 0
        else:
            self.initial_dir = Path(self.base_dir).parents[0]

            self.dump_folder = os.path.join(self.base_dir, 'dump')
            self.done_folder = os.path.join(self.base_dir, 'done')
            self.film_folder = os.path.join(self.base_dir, 'movs')
            self.gifs_folder = os.path.join(self.base_dir, 'gifs')
            self.image_list = []

            if config.SORT_MODE:
                self.mk_dump_dirs()
                self.sort_files_by_type()

            done_files = self.done_files()

            flat_list.extend(done_files)
            self.image_list = sorted(flat_list, key=functools.cmp_to_key(list_sorter))

            self.img_loaded = len(done_files)

        if len(self.image_list) > 0:
            self.load_snake(self.image_list[self.img_loaded])


root = tkinter.Tk()
app = Window(root)
root.mainloop()
