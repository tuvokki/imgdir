import os
import shutil
import random
import click
from PIL import Image


@click.command()
@click.option('--dir', type=click.Path(exists=True), required=True, help='Path to directory containing images')
@click.option('--train', default=0.7, help='Proportion of images to be used for training')
@click.option('--test', default=0.2, help='Proportion of images to be used for testing')
@click.option('--validation', default=0.1, help='Proportion of images to be used for validation')
def split_images_for_ml(dir, train, test, validation):
    # Check of de train-, test- en validation-waarden kloppen
    if round(train + test + validation) != 1:
        raise ValueError("The sum of train, test, and validation must equal 1.")

    # Maak de mappen aan voor train, test, validation en prediction
    train_dir = os.path.join(dir, 'train')
    test_dir = os.path.join(dir, 'test')
    validation_dir = os.path.join(dir, 'validation')
    prediction_dir = os.path.join(dir, 'prediction')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(validation_dir):
        os.makedirs(validation_dir)
    if not os.path.exists(prediction_dir):
        os.makedirs(prediction_dir)

    # Loop door alle afbeeldingen in de mappen 'mooi' en 'stom'
    for folder in ['mooi', 'stom']:
        folder_path = os.path.join(dir, folder)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                # Open de afbeelding en optimaliseer de grootte en kleur
                with Image.open(file_path) as img:
                    img = img.convert('RGB')
                    img = img.resize((224, 224))

                    # Kies willekeurig of de afbeelding in train-, test-, validation- of prediction-map terechtkomt
                    r = random.random()
                    if r < train:
                        new_file_path = os.path.join(train_dir, folder, filename)
                    elif r < train + test:
                        new_file_path = os.path.join(test_dir, folder, filename)
                    elif r < train + test + validation:
                        new_file_path = os.path.join(validation_dir, folder, filename)
                    else:
                        new_file_path = os.path.join(prediction_dir, folder, filename)

                    # Verplaats de afbeelding naar de juiste map
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.copy(file_path, new_file_path)
            except:
                click.echo(f"{filename} is geen geldig beeldbestand.")
                continue


if __name__ == '__main__':
    split_images_for_ml()
