import os
from PIL import Image
import click

@click.command()
@click.option('--dir', type=click.Path(exists=True), help='Path to directory containing images.')
def resize_images(dir):
    """
    This script resizes all images in the specified directory and subdirectories to 224x224 with 80% compression.
    """
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            if filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".png"):
                im = Image.open(filepath)
                click.echo(f'Resizing: {filepath}')
                im_resized = im.resize((224, 224))
                if im.format is 'PNG' and im.mode is not 'RGBA':
                    click.echo(f'Converting: {filepath} to RGBA')
                    # Convert the image to RGBA mode
                    im_converted = im_resized.convert('RGBA')
                    # Save the converted image
                    im_converted.save(filepath, optimize=True, quality=80)
                else:
                    # Save the resized image
                    im_resized.save(filepath, optimize=True, quality=80)

if __name__ == '__main__':
    resize_images()
