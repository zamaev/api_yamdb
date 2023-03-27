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
Запустить проект:
```bash
python3 manage.py runserver
```

## Авторы
- [Айдрус](https://github.com/zamaev), [Алексей](https://github.com/potashka), [Марсель](https://github.com/honour4life)
