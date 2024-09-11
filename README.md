# Скрипт для обработки узлов через gpt

## ВАЖНО

- ! запускать только с vpn !
- текст промта в формате .txt
- ссылка полная, пример: https://beta.app.redforester.com/mindmap?mapid=c04981ec-9f3b-4234-a062-476b597e6587&nodeid=cbf46d0c-7a51-4eee-8186-d770d3cd106d

## Установка

1. Клонируйте репозиторий

``` bash
git clone https://github.com/moritys/rf-export-to-gpt-and-back.git
```

2. Создайте файл '.env' в корне проекта. Пример наполнения файла в 'example.env'

3. Создайте и запустите виртуальное окружение

``` bash
python -m venv venv
. venv/Scripts(bin для linux)/activate
```

4. Установите зависимости

``` bash
pip install -r requirements.txt
```

5. Запустите скрипт

``` bash
cd app/
python main.py
```

6. Выберите файл с промтом и введите ссылку на ветку
