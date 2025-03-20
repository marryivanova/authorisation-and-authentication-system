Материалы для написания:
1. https://habr.com/ru/articles/829742/

запуск:
- pip install -r requirements.txt
- uvicorn src.app.main:app --reload

Задание:
1. Как избежать утечек токена?

Что пременила для этого:

а) Использование HTTPOnly и Secure флагов для куки
Если токен хранится в куках, установите флаги HTTPOnly и Secure:
- HTTPOnly предотвращает доступ к куке через JavaScript.
- Secure гарантирует, что кука передается только по HTTPS.

б) Использование CORS (Cross-Origin Resource Sharing)
Ограничивает доступ к  API только с доверенных доменов.

в) Ограничение времени жизни токена
Устанавливайте короткое время жизни для токенов и используйте механизм обновления токенов (refresh tokens)

г) Использование JWT (JSON Web Tokens)
JWT позволяет подписывать токены, что делает их более безопасными. 

д) Защиту от атак Brute Force и XSS, Clickjacking.

е) Настройка в nginx.


Запуск:
- docker-compose -f docker/docker-compose.yml build
- docker-compose -f docker/docker-compose.yml up -d --force-recreate
- Проверка - docker ps -a
