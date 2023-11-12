from pathlib import Path
import random


class ImageProcessor:
    def randomize_subdirectory_names(self, directory):
        directory_path = Path(directory)
        subdirectories = [subdir for subdir in directory_path.iterdir() if subdir.is_dir()]
        randomized_names = random.sample(subdirectories, len(subdirectories))
        new_names = []

        for subdir, new_name in zip(subdirectories, randomized_names):
            new_path = subdir.with_name(new_name.name)
            subdir.rename(new_path)
            new_names.append(new_name.name)

        return new_names

    def get_character_from_keypress(self, event):
        character = event.char
        if character.isalpha():
            return character
        return "UNKNOWN"

    def extract_string2(self, input_string):
        parts = input_string.split('_')
        if len(parts) > 1:
            string2 = parts[1].split('-')[0]
            return string2
        else:
            return None