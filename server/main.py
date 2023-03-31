from fastapi import FastAPI, UploadFile, File
from cachetools import TTLCache
import json
import uuid


cache = TTLCache(maxsize=50, ttl=120) # cache for storing session id and result

app = FastAPI()

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