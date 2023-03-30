# api_yamdb
API к платформе для оставления отзывов к произведениям, составления рейтингов и комментирования отзывов

## Требования
- Python (3.7+)

### Пакеты:
- Django (3.2)
- djangorestframework (3.12.4)
- djangorestframework-simplejwt (4.7.2)

## Установка
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:zamaev/api_yamdb.git
cd api_yamdb
```
Установить и активировать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Добавление тестовых данных (импорт из фикстур)
```
python manage.py csvfullfillment
```
Запустить проект:
```bash
python3 manage.py runserver
```

## Примеры запросов
### Регистрация 
Отправляет на почту код подтверждения для получения токена.
```
POST /api/v1/auth/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "user"
}
```
### Получение токена
```
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "user",
  "confirmation_code": "blwe40-caa91ba6bc59d8a5bc3bded3b4c56972"
}
```

## Документация
Полный список эндпоинтов можно посмотреть запустив сайт и перейдя по ссылке `/redoc/`

## Авторы
- [Айдрус](https://github.com/zamaev), [Алексей](https://github.com/potashka), [Марсель](https://github.com/honour4life)
