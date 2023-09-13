<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>
<div id="badges" align="center">
  <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=yellow" alt="Python"/>
  <img src="https://img.shields.io/badge/React-white?style=for-the-badge&logo=react&logoColor=blue" alt="React"/>
  <img src="https://img.shields.io/badge/Django-dark_green?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/PostgreSQL-white?style=for-the-badge&logo=postgresql&logoColor=blue" alt="PostgreSQL"/>

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=25&pause=500&color=F70000&center=true&vCenter=true&width=435&lines=Foodgram" alt="Kittygram" /></a>
</div>

### Доступ к проекту:

https://foodgram.servecounterstrike.com/

https://158.160.21.11/

Учетная запись администратора:

Логин: `admin@admin.ru`

Пароль: `admin`

Учетная запись тестового пользователя:

Логин: `test@test.ru`

Пароль: `testtesttest`

### Описание:
Проект "Продуктовый помощник" предоставляет пользователям следующие возможности:

- регистрироваться и менять пароль
- создавать свои рецепты и управлять ими
- добавлять рецепты других пользователей в избранное и корзину
- подписываться на других пользователей
- скачать список ингредиентов для рецептов, добавленных в корзину

### Технологии используемые в проекте:
- Django==4.2.5
- djangorestframework==3.14.0
- django-filter==23.2
- django-import-export==3.2.0
- django-modeladmin-reorder==0.3.1
- djoser==2.2.0
- drf-base64==2.0
- Pillow==10.0.0
- psycopg2_binary==2.9.7
- python-dotenv==1.0.0
- webcolors==1.13
- nodejs==v13.12.0
- PostgreSQL==13
- Docker

### Инструкция по деплою
1) Установите curl, docker и docker-compose-plugin
```
sudo apt update && sudo apt install curl
```
```
curl -fSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh
```
```
sudo apt-get install docker-compose-plugin
```
2) Перейдите в папку `foodgram-project-react` и скопируйте `.env.example` в `.env`. Заполните его своими данными

3) Создайте и скопируйте содержимое `docker-compose.production.yml` удобым вам способом в корневую папку `foodgram-project-react` и запустите установку контейнеров продакшн версии
```
sudo docker compose -f docker-compose.production.yml up -d
```
4) Примените миграции, создайте статические файлы для админки и скопируйте статику в директорию веб-сервера
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/static/static/
```
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/docs/. /app/static/api/docs/
```
5) Создайте суперпользователя
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

### Автор:
#### Первоначальное авторское право © 2020 Яндекс.Практикум <https://github.com/yandex-praktikum>
#### Раздвоенное авторское право © 2023 Quality <mr.quality@ya.ru>