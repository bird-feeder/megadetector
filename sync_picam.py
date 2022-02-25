import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from loguru import logger
from requests.structures import CaseInsensitiveDict


def main():
    dt = datetime.today().strftime("%m-%d-%Y")
    NEW_FOLDER_NAME = f'downloaded_{dt}'
    TITLE = f"{NEW_FOLDER_NAME}/with_detections"
    TOKEN = os.environ['TOKEN']

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"token {TOKEN}"
    headers["Content-Type"] = "application/json"

    _PATH = f"/label-studio/local-files/picam/{NEW_FOLDER_NAME}/with_detections"

    url = "https://ls.aibird.me/api/storages/localfiles?project=5"
    resp = requests.get(url, headers=headers)
    response = resp.json()

    EXISTS = False
    for x in response:
        if x['path'] == _PATH:
            logger.warning('Storage folder already exists!')
            EXISTS = True
            break

    if not EXISTS:
        data = "{" + f'"path":"{_PATH}","title":"{TITLE}","regex_filter":".*jpg","use_blob_urls":"true","project":5' + "}"
        resp = requests.post(url, headers=headers, data=data)
        response = resp.json()
        logger.info(response)

    url = f'https://ls.aibird.me/api/storages/localfiles/{x["id"]}/sync'
    resp = requests.post(url, headers=headers)
    logger.info(resp.text)


if __name__ == '__main__':
    main()
