import argparse
import json
import os
import sys
from pathlib import Path

import dotenv
import pymongo
from loguru import logger
from tqdm import tqdm


def mongodb():
    dotenv.load_dotenv()
    client = pymongo.MongoClient(os.environ['DB_CONNECTION_STRING'])
    db = client[os.environ['DB_NAME']]
    return db


def skip_list():
    db = mongodb()
    data = db.completed.find().distinct('_id')
    with open('skip_list.json', 'w') as j:
        json.dump(data, j)
    logger.info(f'Skip list file path: {Path("skip_list.json").absolute()}')


def main(data_file):
    db = mongodb()
    col = db.completed

    logger.info(f'Processing: {data_file}')
    with open(data_file) as j:
        data = json.load(j)
    logger.info(f'Number of documents to add: {len(data["images"])}')

    for image in tqdm(data['images']):
        file_path = f'{Path(Path(image["file"]).parent).name}/{Path(image["file"]).name}'
        image.update({'_id': Path(file_path).name, 'file': file_path})
        try:
            col.insert_one(image)
        except pymongo.errors.DuplicateKeyError:
            logger.debug('Duplicate:', image)

    with open(data_file, 'rb') as f:
        db.processed.insert_one({
            '_id':
            Path(data_file).name,
            'detection_completion_time':
            data['info']['detection_completion_time'],
            'data':
            f.read()
        })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='Path to the .json output data file')
    parser.add_argument('--get-skip-list', action='store_true', help='Get a list of files to skip')
    args = parser.parse_args()
    if args.data:
        assert Path(args.data).exists(), 'The specified path does not exist!'
        main(args.data)
    if args.get_skip_list:
        skip_list()
