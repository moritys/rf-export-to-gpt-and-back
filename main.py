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


def traverse(node):
    '''
    Собирает инфу со всей ветки и выводит заголовок.
    '''
    type_node = is_it_nontype_node(node)
    if type_node:
        # здесь должно быть создание категорий
        print(type_node)
    # а здесь отправка в ии !через else!
    print(remove_html_tags(node['body']['properties']['global']['title']))
    print('✿══════✿══════✿══════✿══════✿══════✿')

    if "children" in node['body']:
        for child in node['body']['children']:
            traverse(child)


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
    else:
        print("Ошибка:", response.status_code, response.text)
    # nodeid_parent = response_data.get('parent')
    # nodes_children = response_data.get('children')
    # nontype_dict = {}
    traverse(response_data)


def test_post():
    post_url = f'{BASE_URL}/nodes/bb44c287-13ca-4aeb-934a-2234051cfd98'
    data = {
        "properties": {
            "global": {
                "title": "Test заголовок"
            }
        },
    }
    # params = {"nodeid": "6f6e8a7e-ccbe-4f3f-9f63-797a68a575e5"}
    response = requests.post(post_url, auth=AUTH, json=data)

    if response.status_code == 200:
        response_data = response.json()
        pretty_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(pretty_json)
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
