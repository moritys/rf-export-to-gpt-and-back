import requests

from constants import HEADERS, AUTH


# пример запроса с авторизацией
# response = requests.get(url, auth=auth, headers=headers)


BASE_URL = "https://example.com/api"


# Функция для GET-запроса
def get_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        return response.status_code, response.text


# Функция для POST-запроса
def create_data(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json=data)
    return response.status_code, response.json()


# Функция для PUT-запроса (обновление)
def update_data(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.put(url, json=data)
    return response.status_code, response.json()


# Функция для DELETE-запроса
def delete_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.delete(url)
    return response.status_code, response.text


# Примеры использования
if __name__ == "__main__":
    # GET пример
    print(get_data("items"))

    # POST пример
    new_item = {"name": "Item1", "price": 100}
    print(create_data("items", new_item))
