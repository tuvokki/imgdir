import os
import random
import shutil
import click


@click.command()
@click.argument('dir_path')
@click.option('--num-files', default=100, help='Number of files to keep.')
def keep_random_files(dir_path, num_files):
    """
    Keep a specified number of random files in a directory and delete the rest.
    """
    # Get all files in the directory
    files = os.listdir(dir_path)
    num_files_total = len(files)
    click.echo(f'The directory contains: {num_files_total}')
    if num_files_total <= num_files:
        click.echo('The directory contains fewer than the requested number of files. Nothing will be deleted.')
        return

    # Shuffle the list of files
    random.shuffle(files)

    # Keep the first n files and delete the rest
    files_to_keep = files[:num_files]
    for file in files:
        if file not in files_to_keep:
            file_path = os.path.join(dir_path, file)
            os.remove(file_path)
            click.echo(f'{file_path} has been deleted.')

    click.echo(f'{num_files} random files have been kept in {dir_path}.')

if __name__ == '__main__':
    keep_random_files()