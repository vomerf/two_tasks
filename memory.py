import psutil
import requests
import time


api_url = 'https://example.com/api/alarm'
memory_threshold = 80

while True:
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > memory_threshold:
        payload = {f'message: Memory usage exceeded {memory_threshold}'}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200:
                print('HTTP запрос успешно отправлен')
            else:
                print(
                    'Ошибка при отправке HTTP запроса. Код ответа:', response.status_code
                )
        except requests.exceptions.RequestException as e:
            print('Ошибка при отправке HTTP запроса:', str(e))
    time.sleep(60)
