import requests
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import re

from constants import AUTH, BASE_URL
from claude_connection import send_message


def get_node_data(node_url):
    '''Выдает всю инфу о конкретном узле.'''
    try:
        node_id = node_url.split('=')[-1]
        api_endpoint = f'{BASE_URL}/nodes/{node_id}'
        response = requests.get(api_endpoint, auth=AUTH)

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Ошибка при получении данных узла:", e)


def remove_html_tags(html_text):
    '''Убирает html тэги из текста заголовков.'''
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print("Ошибка при удалении HTML-тегов:", e)


def get_mapid_nodeid_from_link(url):
    '''Достает id карты и id узла из ссылки.'''
    try:
        pattern = r'mapid=([a-f0-9-]+)&nodeid=([a-f0-9-]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
        else:
            print('Ошибка в ссылке')
            return None
    except Exception as e:
        print("Ошибка при извлечении ID из ссылки:", e)


def is_it_nontype_node(node):
    '''Проверяет тип узла (нонтайп или категория).'''
    try:
        body = node.get('body')
        return body.get('type_id')
    except Exception as e:
        print("Ошибка при проверке типа узла:", e)


def get_text_from_single_node(node_url):
    '''Выдает инфу о конкретном узле.'''
    try:
        response_data = get_node_data(node_url)
        body = response_data.get('body')
        properties = body.get('properties')
        global_f = properties.get('global')
        title = global_f.get('title')
        print('Текст узла:')
        print(remove_html_tags(title))
    except Exception as e:
        print("Ошибка при получении текста узла:", e)


def copy_node_data(node, parent_id):
    '''Копирует узел без изменений в нового родителя.'''
    try:
        type_id = is_it_nontype_node(node)
        body = {
            "map_id": node['map_id'],
            "parent": parent_id,
            "type_id": type_id,
            "properties": {
                "global": node['body']['properties']['global'],
                # "byUser": node['body']['properties'].get('byUser', []),
                # "byType": node['body']['properties'].get('byType', {}),
                # "style": node['body']['properties'].get('style', {}),
            }
        }
        response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
        response.raise_for_status()
        return response.json().get('id')
    except requests.RequestException as e:
        print("Ошибка при копировании узла:", e)


def create_text_node(node, parent_id, prompt, text):
    '''Создает нонтайп узел в новом родителе.'''
    try:
        ai_answer = send_message(prompt, text)
        body = {
            "map_id": node['map_id'],
            "parent": parent_id,
            "properties": {
                "global": {
                    "title": ai_answer,
                },
                "byUser": [],
                "byType": {},
                "style": {},
            }
        }
        response = requests.post(f'{BASE_URL}/nodes', auth=AUTH, json=body)
        response.raise_for_status()
        return response.json().get('id')
    except requests.RequestException as e:
        print("Ошибка при создании текстового узла:", e)


def traverse(node, new_parent_id, prompt, text=None):
    '''Проходит по ветке и копирует ее зеркально.'''
    try:
        type_node = is_it_nontype_node(node)
        if type_node:
            new_node_id = copy_node_data(node, new_parent_id)
        else:
            text = remove_html_tags(node["body"]["properties"]["global"]["title"])
            new_node_id = create_text_node(node, new_parent_id, prompt, text)
        print(f'✿ {remove_html_tags(node["body"]["properties"]["global"]["title"])} ✅')

        if "children" in node['body']:
            for child in node['body']['children']:
                traverse(child, new_node_id, prompt)
    except Exception as e:
        print("Ошибка при обходе узлов:", e)


def get_data_from_parent(url, prompt_file):
    '''Обрабатывает ссылку на ветку и запускает копирование.'''
    try:
        mapid, nodeid = get_mapid_nodeid_from_link(url)
        branch_url = f'{BASE_URL}/maps/{mapid}/nodes/{nodeid}'
        response = requests.get(branch_url, auth=AUTH)
        response.raise_for_status()
        response_data = response.json()
        new_parent_id = response_data.get('parent')
        traverse(response_data, new_parent_id, prompt_file)
    except requests.RequestException as e:
        print("Ошибка при получении данных узла из родителя:", e)


def open_and_read_file():
    try:
        print("Выберите файл с промптом: ")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        root.destroy()

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
    except Exception as e:
        print("Ошибка при чтении файла:", e)
    return None


def main():
    '''
    Сценарий:
    1. Запрашиваем урл ветки
    2. Запрашиваем файл промпта
    3. Включаем ее обработку
        3.1 Циклом идем по узлам
        3.2 Если узел нонтайп, берем его заголовок и кидаем в ИИ
        3.3 Если узел не нонтайп, то копируем в другую ветку
    '''
    try:
        prompt_file = open_and_read_file()
        parent_url = input("Введите URL ветки: ").strip()
        print('✿══════✿══════✿══════✿══════✿══════✿')
        get_data_from_parent(parent_url, prompt_file)
        print('✿══════✿══════✿══════✿══════✿══════✿')
        print('D O N E ✅')
    except Exception as e:
        print("Ошибка в основном сценарии:", e)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        input("Нажмите Enter, чтобы закрыть...")
# https://beta.app.redforester.com/mindmap?mapid=c04981ec-9f3b-4234-a062-476b597e6587&nodeid=a7edf1a3-3c6b-4ac3-a937-7cdecb56f194