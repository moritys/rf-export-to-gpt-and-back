from bs4 import BeautifulSoup


def remove_html_tags(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    
    # Получаем текст с сохранением пробелов
    text = soup.get_text(separator=" ", strip=True)
    
    return text


html_text = "<p>Привет, <strong>мир!</strong></p><p>Как дела?</p>"
clean_text = remove_html_tags(html_text)

print(clean_text)
