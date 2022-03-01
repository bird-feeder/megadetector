import os
import time

import dotenv
import requests
import schedule
from loguru import logger
from requests.structures import CaseInsensitiveDict


def main():
    TOKEN = os.environ['TOKEN']
    headers = CaseInsensitiveDict()
    headers["Accept"] = 'application/json'
    headers["Authorization"] = f'token {TOKEN}'
    headers["Content-Type"] = 'application/json'

    urls = [
        'https://ls.aibird.me/api/storages/export/azure/1/sync?project=1',
        'https://ls.aibird.me/api/storages/export/localfiles/5/sync?project=1'
    ]

    for url in urls:
        resp = requests.post(url, headers=headers)
        logger.debug(f'API request: {url}')
        logger.info(f"Sync response: {resp.json()}")


if __name__ == '__main__':
    logger.add('sync_export.log')
    dotenv.load_dotenv()
    schedule.every(10).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
