import json
import sys
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
from loguru import logger
from tqdm import tqdm


def make_headers():
    load_dotenv()
    TOKEN = os.environ['TOKEN']
    headers = CaseInsensitiveDict()
    headers["Content-type"] = "application/json"
    headers["Authorization"] = f"Token {TOKEN}"
    return headers


def get_all_tasks(project_id):
    logger.debug('Getting tasks data... This might take few minutes...')
    url = f"https://ls.aibird.me/api/projects/{project_id}/tasks?page_size=10000"
    headers = make_headers()
    resp = requests.get(url,
                        headers=headers,
                        data=json.dumps({'project': project_id}))
    with open('tasks_latest.json', 'w') as j:
        json.dump(resp.json(), j)
    return resp.json()


def find_image(img_name):
    for im in mm_data['images']:
        if Path(im['file']).name == img_name:
            return im


def main(task_id):
    headers = make_headers()
    url = f"https://ls.aibird.me/api/tasks/{task_id}"
    resp = requests.get(url, headers=headers)
    task_ = resp.json()
    if not task_['predictions']:
        img = task_['data']['image']
    else:
        return
    mm_preds = find_image(Path(img).name)

    results = []
    scores = []
    for item in mm_preds['detections']:
        if item['category'] != '1':
            continue
        x, y, width, height = [x * 100 for x in item['bbox']]
        scores.append(item['conf'])
        results.append({
            'from_name': 'label',
            'to_name': 'image',
            'type': 'rectanglelabels',
            'value': {
                'rectanglelabels': ['object'],
                'x': x,
                'y': y,
                'width': width,
                'height': height
            },
            'score': item['conf']
        })

    post_ = {
        "model_version": "Megadetector",
        "result": results,
        "score": np.mean(scores),
        "cluster": 0,
        "neighbors": {},
        "mislabeling": 0,
        "task": task_id
    }

    url = "https://ls.aibird.me/api/predictions/"
    resp = requests.post(url, headers=headers, data=json.dumps(post_))
    logger.debug(resp.json())


if __name__ == '__main__':
    # mm_data_file = 'data_.json'
    if len(sys.argv) == 1:
        raise Exception('You need to provide a path to the output data file!')
    if not Path(sys.argv[1]).exists():
        raise FileNotFoundError('The path you entered does not exist!')
    mm_data_file = sys.argv[1]
    with open(mm_data_file) as j:
        mm_data = json.load(j)

    data = get_all_tasks(4)
    # with open('tasks_latest.json') as j:
    #     data = json.load(j)
    tasks_ids = [x['id'] for x in data]

    for cur_task in tqdm(tasks_ids):
        main(cur_task)
