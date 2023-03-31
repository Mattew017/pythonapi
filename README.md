# Тестовое задание на Python

## Содержание
1. [Описание задания](#Описание-задания)
2. [Деплой и запуск](#Деплой-и-запуск)
3. [Решение](#решение)



# Описание задания
### Необходимо разработать HTTP сервис, который на входе будет получать файл json формата со списком цифр, обратно пользователю направлять сумму всех цифр. Сервис должен предоставлять клиенту rest api с интерфейсом openapi/swagger ui.

Пример входных данных:

```json
{
"array": ["1", "2", "3", "4", null]
}
```
Реализовать с помощью двух методов:

1) Синхронный

2) Асинхронный (пользователь получает ID сессии и получает ответ по ID сессии). Реализовать простую схему хранения сессии и результата

Весь код должен запускаться в виде докер сервиса с помощью docker-compose up.


# Деплой и запуск

Веб приложение с интерфейсом Swagger  нужно открывать по пути [http://localhost:8008/docs](http://localhost:8008/docs).

Первый способ. С помощью github.

```
git clone https://github.com/Mattew017/pythonapi.git
```

```
cd /path/to/repo/
```

```
docker-compose up -d
```

Втрой способ. С помощью Docker Hub.

В рабочей директории создать файл ***docker-compose.yml*** со следующим содержанием:

```
version: '3.9'

services:
  server:
    ports:
      - 8008:8000
    image: mattew017/pythonapi
```

Выполнить
```
docker-compose up -d
```



# Решение

Синхронный метод:

```python
@app.post("/get_sum")
def get_sum(file: UploadFile = File(...)):
    """
    POST method to calculate the sum of numbers from an uploaded JSON file.
    Returns calculated sum.

    :param file: json file
    :returns: sum of numbers in file
    :raises Exception: when any exception occurs
    """
    try:
        data = file.file.read()
        data = json.loads(data)
        array = data.get("array", [])
        array = [int(x) for x in array if x is not None]
        result = sum(array)
        return {"total sum": result}
    except Exception as e:
        return {"error": str(e)}
``` 

Асинхронный метод. POST методом клиент получает id сессии, GET запросом получает результат:
```python
@app.post("/get_session_id")
async def get_session_id(file: UploadFile = File(...)):
    """
    POST async method to calculate the sum of numbers from an uploaded JSON file.
    Returns session ID.

    :param file: json file
    :returns: session id
    :raises Exception: when any exception occurs
    """
    try:
        session_id = uuid.uuid4().hex

        data = await file.read()
        data = json.loads(data)
        array = data.get("array", [])
        array = [int(x) for x in array if x is not None]
        result = sum(array)

        cache[session_id] = result
        return {"session_id": session_id}
    except Exception as e:
        return {"error": str(e)}
        
@app.get("/{get_sum_async}")
async def get_sum_async(session_id: str):
    """
    GET method to obtain calculated sum by the session id.
    Returns calculated sum.

    :param session_id: session id
    :returns: corresponding result of session_id or error message
    """
    result = cache.get(session_id)
    if result is None:
        return {"error": "Invalid session id"}
    else:
        return {"total sum": result}
```
