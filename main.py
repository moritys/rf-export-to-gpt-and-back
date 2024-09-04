import requests
import json
from bs4 import BeautifulSoup
import re

from constants import AUTH, BASE_URL


def get_node_data(node_url):
    '''Выдает всю инфу о конкретном узле.'''
    node_id = node_url.split('=')[-1]
    api_endpoint = f'{BASE_URL}/nodes/{node_id}'
    response = requests.get(api_endpoint, auth=AUTH)

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print("Ошибка:", response.status_code, response.text)


def post_new_node(node_url):
    post_url = f'{BASE_URL}/nodes'
    map_id, _ = get_mapid_nodeid_from_link(node_url)
    parent_id = get_node_data(node_url).get('parent')
    body = {
        "map_id": map_id,
        "parent": parent_id,
        "position": ["P", "0"],
        "properties": {
            "global": {
                "title": "hello from script"
            },
            "byUser": [],
            "byType": {},
            "style": {}
        }
    }
    response = requests.post(post_url, auth=AUTH, json=body)

    if response.status_code == 200:
        response_data = response.json()
        pretty_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(pretty_json)
    else:
        print("Ошибка:", response.status_code, response.text)


def remove_html_tags(html_text):
    '''Убирает html тэги из текста заголовков.'''
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


def get_mapid_nodeid_from_link(url):
    '''
    Достает id карты и id узла из ссылки.
    '''
    pattern = r'mapid=([a-f0-9-]+)&nodeid=([a-f0-9-]+)'
    match = re.search(pattern, url)
    if match:
        mapid = match.group(1)
        nodeid = match.group(2)
    else:
        print('Ошибка в ссылке')
        return None
    return mapid, nodeid


def is_it_nontype_node(node):
    '''
    Проверяет тип узла (нонтайп или категория).
    '''
    body = node.get('body')
    type_id = body.get('type_id')
    return type_id or None


def get_text_from_single_node(node_url):
    '''
    Выдает инфу о конкретном узле.
    '''
    response_data = get_node_data(node_url)

    body = response_data.get('body')
    properties = body.get('properties')
    global_f = properties.get('global')
    title = global_f.get('title')
    print('Текст узла:')
    print(remove_html_tags(title))


def copy_node_data(node, parent_id):
    # Create a mirrored copy of the node under the specified parent
    body = {
        "map_id": node['map_id'],
        "parent": parent_id,
        "position": node.get('position', ["P", "0"]),
        "properties": {
            "global": node['body']['properties']['global'],
            "byUser": node['body']['properties'].get('byUser', []),
            "byType": node['body']['properties'].get('byType', {}),
            "style": node['body']['properties'].get('style', {}),
        }
    }
    response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
    if response.status_code != 200:
        print("Ошибка при копировании узла:", response.status_code, response.text)


def create_text_node(node, parent_id):
    # Create a new node with just text
    title = node['body']['properties']['global']['title']
    body = {
        "map_id": node['map_id'],
        "parent": parent_id,
        "position": ["P", "0"],
        "properties": {
            "global": {
                "title": remove_html_tags(title),
            },
            "byUser": [],
            "byType": {},
            "style": {},
        }
    }
    response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
    if response.status_code != 200:
        print("Ошибка при создании текстового узла:", response.status_code, response.text)


def traverse(node, parent_id):
    '''
    Собирает инфу со всей ветки и выводит заголовок.
    '''
    type_node = is_it_nontype_node(node)
    if type_node:
        copy_node_data(node, parent_id)
    else:
        create_text_node(node, parent_id)
    print(remove_html_tags(node['body']['properties']['global']['title']))
    print('✿══════✿══════✿══════✿══════✿══════✿')

    if "children" in node['body']:
        for child in node['body']['children']:
            traverse(child, node['id'])


def get_data_from_parent(url):
    mapid, nodeid = get_mapid_nodeid_from_link(url)
    branch_url = f'{BASE_URL}/maps/{mapid}/nodes/{nodeid}'
    response = requests.get(branch_url, auth=AUTH)
    if response.status_code == 200:
        response_data = response.json()
        # Start traversal with the initial node and its parent
        traverse(response_data, response_data.get('parent'))
    else:
        print("Ошибка:", response.status_code, response.text)


# https://beta.app.redforester.com/mindmap?mapid=c04981ec-9f3b-4234-a062-476b597e6587&nodeid=3c7d0d0b-c7c3-44f3-b0e5-7e450047567d
if __name__ == '__main__':
    '''
    Сценарий:
    1. Запрашиваем урл ветки
    2. Запрашиваем файл промпта
    3. Включаем ее обработку
        3.1 Циклом идем по узлам
        3.2 Если узел нонтайп, берем его заголовок и кидаем в ИИ
        3.3 Если узел не нонтайп, то копируем в другую ветку
    '''
    # находим текст одного узла
    # node_url = input("Введите URL узла: ")
    # print('✿══════✿══════✿══════✿══════✿══════✿')
    # get_text_from_single_node(node_url)

    # находим текст ветки
    parent_url = input("Введите URL ветки: ")
    print('✿══════✿══════✿══════✿══════✿══════✿')
    get_data_from_parent(parent_url)
    # test_post()
