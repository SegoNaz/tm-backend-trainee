# Тестовое задание для стажёра Backend в команду Trade Marketing.

Нужно разработать микросервис для счетчиков статистики. Сервис должен уметь взаимодействовать с клиентом при помощи REST API или JSON RPC запросов. Также нужно реализовать валидацию входных данных.

## API методы:
- Метод сохранения статистики
- Метод показа статистики
- Метод сброса статистики

## Метод сохранения статистики.
Принимает на вход: 
- **date** - дата события
- **views** - количество показов
- **clicks** - количество кликов
- **cost** - стоимость кликов (в рублях с точностью до копеек)

Поля **views**, **clicks** и **cost** - опциональные.
Статистика агрегируется по дате.

## Метод показа статистики
Принимает на вход:
- **from** - дата начала периода (включительно)
- **to** - дата окончания периода (включительно)

Отвечает статистикой, отсортированной по дате. В ответе должны быть поля:
- **date** - дата события
- **views** - количество показов
- **clicks** - количество кликов
- **cost** - стоимость кликов
- **cpc** = cost/clicks (средняя стоимость клика)
- **cpm** = cost/views * 1000 (средняя стоимость 1000 показов)
 
## Метод сброса статистики
Удаляет всю сохраненную статистику. 
 
## Критерии приемки:
- язык программирования: *Go/PHP/Python*.
- можно использовать любое хранилище(*PostgreSQL, MySQl, Redis* и т.д.) или обойтись без него (*in-memory*). При использовании СУБД нужен файл с запросами на создание - - всех необходимых таблиц.
- формат даты **YYYY-MM-DD**.
- стоимость указывается в рублях с точностью до копеек.
- простая инструкция для запуска (в идеале — с возможностью запустить в *docker*).

## Усложнения:
- в методе показа статистики можно выбрать сортировку по любому из полей ответа.
- покрытие unit-тестами.
- документация (достаточно структурированного описания методов, примеров их вызова в README.md).

# Решение с помощью Python, FastAPI.
## Установка и запуск:
- **Linux + docker-compose:**
- cd where-you-keep-your-projects
- mkdir tm-project
- cd tm-project
- git init
- git pull https://github.com/SegoNaz/tm-backend-trainee
- docker-compose up

После запуска сервера, интерактивная документация будет доступна по адресу: http://your_ip_address:8000/docs, или http://127.0.0.1:8000/docs  
Альтернативная документация: http://your_ip_address:8000/redoc, или http://localhost:8000/redoc

- **Python, uvicorn + venv (Ubuntu 20.04)**
- cd where-you-keep-your-projects
- mkdir tm-project
- cd tm-project
- git init
- git pull https://github.com/SegoNaz/tm-backend-trainee
- python3 -m venv tm-venv
- source tm-venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --host 127.0.0.1 --port 8000

После запуска сервера, интерактивная документация будет доступна по адресу: http://127.0.0.1:8000/docs  
Альтернативная документация: http://127.0.0.1:8000/redoc

### Примеры запросов:
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/stat?from=2022-01-01&to=2022-01-04&order_column=date' \
  -H 'accept: application/json'
  
  
 curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/stat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "views": 10,
  "clicks": 10,
  "cost": 1.99,
  "date": "2022-01-02"
}'
  
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/v1/stat' \
  -H 'accept: application/json'

## Основные функции:
+ **get_events_by_event_date(db: Session, from_date: date, to_date: date, order_column)**  
Функция формирует данные:
+ date - дата события
+ views - количество показов
+ clicks - количество кликов
+ cost - стоимость кликов
+ cpc = cost/clicks (средняя стоимость клика). 3 знака после запятой.
+ cpm = cost/views * 1000 (средняя стоимость 1000 показов). 3 знака после запятой.
+ Агрегация по дате.
+ Фильтр по дате (from, to), включительно.
+ Сортировка по любому полю.  
- **create_event(db: Session, event: sc.EventCreate)**   
Функция сохранения статистики. EventCreate - pydantic схема для сохранения и валидации данных:  
- date - дата события.
- views - количество показов.
- clicks - количество кликов.
- cost - стоимость кликов (в рублях с точностью до копеек).
- Поля views, clicks и cost - опциональные.  

+ **delete_statistics(db: Session, tables: tuple)**  
Функция очищает таблицы от данных:
+ Принимает на вход необходимые таблицы



 



