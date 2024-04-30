Чтобы запустить проект нужно:

1. Создать проект в Google Cloud Console (https://console.cloud.google.com/)
2. В разделе API&Servcies добавить (+ ENABLE API&SERVCIES) два сервиса: Google Drive, Goole Slides
3. Перейти в раздел Credentials и создать Service Account
4. Скачать json файл, назвать его credentials.json, поместить в директорию проекта
5. Прописать команду:
```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
6. Создать папку images в корне проекта и добавить туда файлы, которые будут google слайдами
7. Запустить проект:
```python main.py```