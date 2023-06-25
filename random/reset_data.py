import os
import click
import zipfile
import random
from PIL import Image


@click.command()
@click.option('--dir', type=click.Path(exists=True), default='./data.zip', help='Directory path')
def process_data(dir):
    # remove data directory
    if os.path.exists('../data'):
        os.system('rm -rf ./data')

    # extract data.zip file
    with zipfile.ZipFile(dir, 'r') as zip_ref:
        zip_ref.extractall('./')

    # iterate through train, test, and validation folders
    for folder in ['train', 'test', 'validation']:
        folder_path = os.path.join('../data/', folder)

        # iterate through mooi and stom folders
        for label in ['mooi', 'stom']:
            label_path = os.path.join(folder_path, label)

            # iterate through images
            images = os.listdir(label_path)
            for img_name in images:
                img_path = os.path.join(label_path, img_name)
                try:
                    # resize and compress image
                    img = Image.open(img_path)
                    img = img.resize((224, 224))
                    img.save(img_path, optimize=True, quality=80)
                except Exception as e:
                    print(e)

        # remove extra images from stom folder
        mooi_path = os.path.join(folder_path, 'mooi')
        stom_path = os.path.join(folder_path, 'stom')
        mooi_images = os.listdir(mooi_path)
        stom_images = os.listdir(stom_path)
        diff = len(stom_images) - len(mooi_images)
        if diff > 0:
            random.shuffle(stom_images)
            for i in range(diff):
                os.remove(os.path.join(stom_path, stom_images[i]))

if __name__ == '__main__':
    process_data()
