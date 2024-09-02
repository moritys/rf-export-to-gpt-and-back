import requests
import json
from bs4 import BeautifulSoup
import re

from constants import AUTH, BASE_URL


def get_node_data(node_url):
    node_id = node_url.split('=')[-1]
    api_endpoint = f'{BASE_URL}/nodes/{node_id}'
    response = requests.get(api_endpoint, auth=AUTH)

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print("Ошибка:", response.status_code, response.text)


def remove_html_tags(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


def get_mapid_nodeid_from_link(url):
    pattern = r'mapid=([a-f0-9-]+)&nodeid=([a-f0-9-]+)'
    match = re.search(pattern, url)
    if match:
        mapid = match.group(1)
        nodeid = match.group(2)
    else:
        print('Ошибка в ссылке')
        return None
    return mapid, nodeid


def is_it_nontype_node(node_url):
    response_data = get_node_data(node_url)
    body = response_data.get('body')
    type_id = body.get('type_id')
    return type_id or None


def get_text_from_single_node(node_url):
    response_data = get_node_data(node_url)

    body = response_data.get('body')
    properties = body.get('properties')
    global_f = properties.get('global')
    title = global_f.get('title')
    print('Текст узла:')
    print(remove_html_tags(title))


def get_data_from_parent(parent_url):
    '''
    1. Получаем ответ по всей ветке
    2. Идем по узлам
    3. Если узел не нонтайп, то копируем его ниже в ветку
    4. Если нонтайп, сохраняем в отдельный массив
    '''
    mapid, nodeid = get_mapid_nodeid_from_link(parent_url)
    branch_url = f'{BASE_URL}/maps/{mapid}/nodes/{nodeid}'
    response = requests.get(branch_url, auth=AUTH)
    if response.status_code == 200:
        response_data = response.json()
        pretty_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(pretty_json)
    else:
        print("Ошибка:", response.status_code, response.text)


def test_post():
    post_url = f'{BASE_URL}/nodes/'
    data = {
        "properties": {
            "global": {
                "title": "Test заголовок"
            }
        },
    }
    params = {"nodeid": "6f6e8a7e-ccbe-4f3f-9f63-797a68a575e5"}
    response = requests.post(post_url, auth=AUTH, params=params, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        pretty_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(pretty_json)
    else:
        print("Ошибка:", response.status_code, response.text)


# https://beta.app.redforester.com/mindmap?mapid=c04981ec-9f3b-4234-a062-476b597e6587&nodeid=3c7d0d0b-c7c3-44f3-b0e5-7e450047567d
if __name__ == '__main__':
    # находим текст одного узла
    # node_url = input("Введите URL узла: ")
    # print('✿══════✿══════✿══════✿══════✿══════✿')
    # get_text_from_single_node(node_url)

    # находим текст ветки
    # parent_url = input("Введите URL ветки: ")
    # print('✿══════✿══════✿══════✿══════✿══════✿')
    # get_data_from_parent('https://beta.app.redforester.com/mindmap?mapid=c04981ec-9f3b-4234-a062-476b597e6587&nodeid=65ced594-2ce7-4118-8d67-6025bea6a02c')
    test_post()
