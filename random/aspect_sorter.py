import os
import click
from PIL import Image


@click.command()
@click.option('--dir', type=click.Path(exists=True), required=True, help='Path to directory containing images')
def split_images_by_aspect_ratio(dir):
    desktop_dir = os.path.join(dir, 'desktop')
    dump_dir = os.path.join(dir, 'dump')

    # Maak de mappen aan als deze nog niet bestaan
    if not os.path.exists(desktop_dir):
        os.makedirs(desktop_dir)
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    # Loop door alle bestanden in de opgegeven directory
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)

        try:
            with Image.open(file_path) as img:
                # Check of de breedte groter is dan de hoogte
                if img.width > img.height:
                    new_file_path = os.path.join(desktop_dir, filename)
                else:
                    new_file_path = os.path.join(dump_dir, filename)

                # Verplaats de afbeelding naar de juiste map
                os.rename(file_path, new_file_path)
        except:
            click.echo(f"{filename} is geen geldig beeldbestand.")
            continue


if __name__ == '__main__':
    split_images_by_aspect_ratio()
