import click
import os
import shutil
import random
import string

@click.command()
@click.option('-s', '--source-dir', required=True, type=click.Path(exists=True), help='Source directory containing the "done" directories')
@click.option('-o', '--output-dir', required=True, type=click.Path(), help='Output directory to collect the files')
@click.option('--randomize', is_flag=True, help='Randomize the resulting filenames')
def collect_files(source_dir, output_dir, randomize):
    """
    Collect files from all "done" directories to the output directory with an incrementing number prefix
    or randomize the resulting filenames.
    """
    click.echo(f'Collecting files from "done" directories in: {source_dir}')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if randomize:
        click.echo('Randomizing the resulting filenames.')
    else:
        click.echo('Using incremental numbering for the resulting filenames.')

    # Counter for the incrementing number prefix
    counter = 1

    # Collect files from all "done" directories
    for root, dirs, files in os.walk(source_dir):
        if 'done' in dirs:
            done_dir = os.path.join(root, 'done')
            click.echo(f'Processing "{done_dir}" directory...')
            if randomize:
                collect_files_from_done_directory_random(done_dir, output_dir)
            else:
                collect_files_from_done_directory(done_dir, output_dir, counter)
                counter += 1

    click.echo('File collection completed.')


def collect_files_from_done_directory(done_dir, output_dir, counter):
    """
    Collect files from a "done" directory to the output directory with an incrementing number prefix.

    Args:
        done_dir (str): Path of the "done" directory.
        output_dir (str): Path of the output directory.
        counter (int): Counter for the incrementing number prefix.
    """
    # Get the list of files in the "done" directory
    files = os.listdir(done_dir)

    # Copy each file to the output directory with the incrementing number prefix
    for file in files:
        file_path = os.path.join(done_dir, file)
        output_file_path = os.path.join(output_dir, f'{counter}_{file}')
        shutil.copy2(file_path, output_file_path)
        click.echo(f'Copied: {file_path} -> {output_file_path}')


def collect_files_from_done_directory_random(done_dir, output_dir):
    """
    Collect files from a "done" directory to the output directory with randomized filenames.

    Args:
        done_dir (str): Path of the "done" directory.
        output_dir (str): Path of the output directory.
    """
    # Get the list of files in the "done" directory
    files = os.listdir(done_dir)

    # Copy each file to the output directory with a randomized filename
    for file in files:
        file_path = os.path.join(done_dir, file)
        file_extension = os.path.splitext(file)[1]
        random_filename = generate_random_filename(file_extension)
        output_file_path = os.path.join(output_dir, random_filename)
        shutil.copy2(file_path, output_file_path)
        click.echo(f'Copied: {file_path} -> {output_file_path}')


def generate_random_filename(extension):
    """
    Generate a random filename with the given extension.

    Args:
        extension (str): File extension.

    Returns:
        str: Random filename.
    """
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f'{random_string}{extension}'


if __name__ == '__main__':
    collect_files()
