import json
import os
import sys
from pathlib import Path

import dotenv
import pymongo
from loguru import logger
from tqdm import tqdm


def main(data_file):
    client = pymongo.MongoClient(os.environ['DB_CONNECTION_STRING'])
    db = client[os.environ['DB_NAME']]
    col = db.completed

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
    dotenv.load_dotenv()
    assert len(sys.argv) > 1, 'You need to specify a data file path!'
    assert Path(sys.argv[1]).exists(), 'The specified path does not exist!'
    main(sys.argv[1])
