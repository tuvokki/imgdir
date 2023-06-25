import os
import shutil
import click
import random
import string


@click.command()
@click.argument('directory')
def rename_files(directory):
    """Rename all files in DIRECTORY to random names."""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            ext = os.path.splitext(filename)[1]
            new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ext
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
            click.echo(f"{filename} renamed to {new_name}")




@click.command()
@click.argument('source')
@click.argument('destination')
def move_files(source, destination):
    """
    This script moves all files from subdirectories in the source directory to the destination directory,
    and deletes the empty subdirectories afterwards.
    """
    for root, dirs, files in os.walk(source):
        for filename in files:
            filepath = os.path.join(root, filename)
            shutil.move(filepath, destination)

    for root, dirs, files in os.walk(source, topdown=False):
        for dir in dirs:
            dirpath = os.path.join(root, dir)
            if not os.listdir(dirpath):
                os.rmdir(dirpath)

    click.echo("Done.")


if __name__ == '__main__':
    move_files()

# if __name__ == '__main__':
#     rename_files()
