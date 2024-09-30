import json
import os
import requests

with open('gallery.photo.har', 'r', encoding='utf-8') as file:
    har_data = json.load(file)

# Создание папки output, если она не существует
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Массив для хранения всех ссылок
urls = []

# Проход по всем записям в HAR-файле
for entry in har_data['log']['entries']:
    url = entry['request']['url']
    if 'lh3.googleusercontent.com' in url:
        # Если в URL есть параметры w или s (например, w768-rw), заменяем их на s0
        if 'w' in url or 's' in url:
            # Разделить URL на основную часть и параметры
            base_url = url.split('=')[0]
            url = base_url + '=s0'
        else:
            # Если параметров нет, добавляем s0 в конец
            url += '=s0'
        urls.append(url)

# Сохранение ссылок в файл output.txt
with open('output.txt', 'w', encoding='utf-8') as output_file:
    for url in urls:
        output_file.write(url + '\n')

print(f'Найдено ссылок: {len(urls)}')

# Скачивание изображений
for idx, url in enumerate(urls):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        # Сохранение изображения в папке output
        file_path = os.path.join(output_folder, f'image_{idx + 1}.jpg')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Изображение сохранено: {file_path}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при скачивании {url}: {e}')
