import argparse
import shutil
from glob import glob
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from loguru import logger
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tqdm import tqdm


def preprocess_image(file):
    img = tf.keras.preprocessing.image.load_img(file, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, 0)
    return img


def predict(img):
    pred = model.predict(img)
    result = decode_predictions(pred)[0]
    return result


def opts():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--images-dir',
        type=str,
        help='Path to the `with_detections` output folder (local)',
        required=True)
    parser.add_argument('--exclude',
                        help='Exclusion classes (comma-separated values)',
                        type=str,
                        required=True)
    parser.add_argument(
        '--not-just-birds',
        help=
        'Pass the flag if the model is meant to detect more than just birds',
        action='store_true')
    args = parser.parse_args()
    return args


def main():
    exclude_classes = args.exclude.split(',')
    detections_folder = f'{args.images_dir}/output/with_detections'
    Path(f'{detections_folder}_excluded').mkdir(exist_ok=True)

    df = pd.read_csv(
        'https://raw.githubusercontent.com/noameshed/novelty-detection/master/imagenet_categories.csv'
    )
    birds = sum(df[3:4].T.dropna().values.tolist(), [])[1:]

    if args.not_just_birds:
        birds = []

    i = 0
    for file in tqdm(glob(f'{args.images_dir}/output/with_detections/*.jpg')):
        img = preprocess_image(file)
        result = predict(img)
        if not [
                bird for bird in birds
                if bird.lower() in [x[1].lower() for x in result]
        ]:
            if [
                    obj for _, obj, prob in result
                    if obj.lower() in exclude_classes
            ]:
                i += 1
                logger.debug(
                    f'Found an excluded class in {Path(file).name}: {result}')
                shutil.move(file,
                            f'{detections_folder}_excluded/{Path(file).name}')

    logger.info(f'Number of excluded images: {i}')


if __name__ == '__main__':
    logger.add('exclude_specific_classes.log')
    args = opts()
    model = tf.keras.applications.EfficientNetB0(weights='imagenet',
                                                 include_top=True)
    main()
