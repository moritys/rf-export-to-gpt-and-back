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


def remove_html_tags(html_text):
    '''Убирает html тэги из текста заголовков.'''
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


def get_mapid_nodeid_from_link(url):
    '''Достает id карты и id узла из ссылки.'''
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
    '''Проверяет тип узла (нонтайп или категория).'''
    body = node.get('body')
    type_id = body.get('type_id')
    return type_id or None


def get_text_from_single_node(node_url):
    '''Выдает инфу о конкретном узле.'''
    response_data = get_node_data(node_url)
    body = response_data.get('body')
    properties = body.get('properties')
    global_f = properties.get('global')
    title = global_f.get('title')
    print('Текст узла:')
    print(remove_html_tags(title))


def copy_node_data(node, parent_id):
    '''Копирует узел без изменений в нового родителя.'''
    type_id = is_it_nontype_node(node)
    body = {
        "map_id": node['map_id'],
        "parent": parent_id,
        "position": node.get('position', ["P", "0"]),
        "type_id": type_id,
        "properties": {
            "global": node['body']['properties']['global'],
            "byUser": node['body']['properties'].get('byUser', []),
            "byType": node['body']['properties'].get('byType', {}),
            "style": node['body']['properties'].get('style', {}),
        }
    }
    response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
    if response.status_code == 200:
        return response.json().get('id')
    else:
        print(
            "Ошибка при копировании узла:",
            response.status_code, response.text
        )
        return None


def create_text_node(node, parent_id):
    '''Создает нонтайп узел в новом родителе.'''
    body = {
        "map_id": node['map_id'],
        "parent": parent_id,
        "position": ["P", "0"],
        "properties": {
            "global": {
                "title": 'это ответ ии',
            },
            "byUser": [],
            "byType": {},
            "style": {},
        }
    }
    response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
    if response.status_code == 200:
        return response.json().get('id')
    else:
        print(
            "Ошибка при создании текстового узла:",
            response.status_code, response.text
        )
        return None


def traverse(node, new_parent_id):
    '''Проходит по ветке и копирует ее зеркально.'''
    type_node = is_it_nontype_node(node)
    if type_node:
        new_node_id = copy_node_data(node, new_parent_id)
    else:
        new_node_id = create_text_node(node, new_parent_id)
    print(
        f'✿ {remove_html_tags(node["body"]["properties"]["global"]["title"])} ✅'
    )
    # print('✿══════✿══════✿══════✿══════✿══════✿')

    if "children" in node['body']:
        for child in node['body']['children']:
            traverse(child, new_node_id)


def get_data_from_parent(url):
    '''Обрабатывает ссылку на ветку и запускает копирование.'''
    mapid, nodeid = get_mapid_nodeid_from_link(url)
    branch_url = f'{BASE_URL}/maps/{mapid}/nodes/{nodeid}'
    response = requests.get(branch_url, auth=AUTH)
    if response.status_code == 200:
        response_data = response.json()
        new_parent_id = response_data.get('parent')
        traverse(response_data, new_parent_id)
    else:
        print("Ошибка:", response.status_code, response.text)


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
    parent_url = input("Введите URL ветки: ")
    print('✿══════✿══════✿══════✿══════✿══════✿')
    get_data_from_parent(parent_url)
    print('✿══════✿══════✿══════✿══════✿══════✿')
    print('D O N E ✅')
