import os
from datetime import datetime

import dotenv
import requests
from loguru import logger
from requests.structures import CaseInsensitiveDict


def main():
    dt = datetime.today().strftime("%m-%d-%Y")
    NEW_FOLDER_NAME = f'downloaded_{dt}'
    TITLE = f"{NEW_FOLDER_NAME}/with_detections"
    TOKEN = os.environ['TOKEN']

    headers = CaseInsensitiveDict()
    headers["Accept"] = 'application/json'
    headers["Authorization"] = f'token {TOKEN}'
    headers["Content-Type"] = 'application/json'

    _PATH = f"/label-studio/local-files/picam/{NEW_FOLDER_NAME}/with_detections"

    url = "https://ls.aibird.me/api/storages/localfiles?project=5"
    resp = requests.get(url, headers=headers)
    response = resp.json()

    EXISTS = False
    for x in response:
        if x['path'] == _PATH:
            logger.warning('Storage folder already exists!')
            logger.debug(f'Existing storage: {x}')
            EXISTS = True
            break

    if not EXISTS:
        data = "{" + f'"path":"{_PATH}","title":"{TITLE}","regex_filter":".*jpg","use_blob_urls":"true","project":5' + "}"
        resp = requests.post(url, headers=headers, data=data)
        response = resp.json()
        logger.info(f'Create new local storage response: {response}')
        storage_id = response['id']
    else:
        storage_id = x['id']

    logger.debug('Running sync...')
    url = f'https://ls.aibird.me/api/storages/localfiles/{storage_id}/sync?project=5'
    resp = requests.post(url, headers=headers)
    logger.info(f'Sync response: {resp.json()}')


if __name__ == '__main__':
    dotenv.load_dotenv()
    logger.add('sync_picam.log')
    main()
