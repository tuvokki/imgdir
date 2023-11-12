import click
import os
import random
import shutil
import string

@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('destination', type=click.Path(file_okay=False, dir_okay=True))
def organize_files(source, destination):
    # Doelmap maken als deze niet bestaat
    os.makedirs(destination, exist_ok=True)

    # Functie om een willekeurige bestandsnaam te genereren
    def generate_random_filename():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(10))

    # Doelsubmappen maken
    for subfolder in ['done', 'movs', 'gifs']:
        os.makedirs(os.path.join(destination, subfolder), exist_ok=True)

    # Door de bronmap bladeren
    for root, dirs, files in os.walk(source):
        for filename in files:
            src_path = os.path.join(root, filename)
            # Bepalen van de bestemming op basis van de mapstructuur
            if 'done' in root:
                dst_folder = 'done'
            elif 'movs' in root:
                dst_folder = 'movs'
            elif 'gifs' in root:
                dst_folder = 'gifs'
            else:
                # Overslaan van bestanden die niet in een van de bovengenoemde mappen staan
                continue

            # Genereren van een willekeurige bestandsnaam en kopie naar doelmap
            random_filename = generate_random_filename()
            ext = os.path.splitext(filename)[1]  # Originele bestandsextensie behouden
            random_filename_with_ext = random_filename + ext
            dst_path = os.path.join(destination, dst_folder, random_filename_with_ext)
            shutil.copy(src_path, dst_path)

    # Door de bronmap bladeren om dump-bestanden te verwijderen
    for root, dirs, files in os.walk(source):
        for filename in files:
            src_path = os.path.join(root, filename)
            if 'dump' in root:
                os.remove(src_path)

if __name__ == '__main__':
    organize_files()
