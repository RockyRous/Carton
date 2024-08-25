import os
from typing import Union
from uuid import uuid4
import shutil

from services.audio import AudioApp, AudioFormats
from services.image import ImageApp, ImageFormats

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Body, Form
from fastapi.responses import FileResponse
import aiofiles  # Библиотека для асинхронной работы с файлами
import uvicorn  # Импортируем uvicorn


app = FastAPI()

UPLOAD_DIR = "../files/"
TASKS = {}


@app.post("/image/change-format_sync/")
async def change_image_format_sync(file_format: str, file: UploadFile = File(...)):
    try:
        file_format = ImageFormats(format=file_format).format
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    image_app = ImageApp()
    try:
        image_app.upload_file(file)
        image_app.change_format(file_format)

        # save
        image_app.save_file('example')
        info = image_app.get_file_info()
        file_path = f'{UPLOAD_DIR}{info["name"]}.{info["format"]}'
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {e}")

    return FileResponse(file_path, media_type="image/" + info["format"])  # Возвращает сразу изображение
    # return {"message": "Image format changed successfully", "file_info": info}


async def change_image_format(task_id: str, file: Union[str, UploadFile], new_format: str):
    try:
        file_app = ImageApp()

        file_app.upload_file(file)
        file_app.change_format(new_format)
        info = file_app.get_file_info()

        TASKS[task_id] = {"status": "completed", "result": info}
    except Exception as e:
        TASKS[task_id] = {"status": "failed", "error": str(e)}


@app.post("/image/change-format_async/")
async def change_image_format_async(
        file_format: str,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
):
    try:
        file_format = ImageFormats(format=file_format).format
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    temp_file_path = f"{UPLOAD_DIR}{uuid4().hex}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task_id = str(uuid4())  # Генерация уникального ID задачи
    TASKS[task_id] = {"status": "processing"}

    background_tasks.add_task(change_image_format, task_id, temp_file_path, file_format)

    return {"task_id": task_id, "message": "Image processing started"}


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


##############################
# Сейчас не используется:

# Функции сохранения файлов (надо интегрировать и в перспективе добавить облако)
def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    try:
        with open(destination, "wb") as buffer:
            buffer.write(upload_file.file.read())
        return destination
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

async def save_upload_file_async(upload_file: UploadFile, destination: str) -> str:
    try:
        async with aiofiles.open(destination, "wb") as buffer:
            content = await upload_file.read()  # Асинхронное чтение файла
            await buffer.write(content)  # Асинхронная запись файла
        return destination
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

# Работа с аудио
@app.post("/audio/change-format_async/")
async def change_audio_format_async(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        request: str = None
):
    return {"task_id": '123', "message": "Audio processing started"}

@app.post("/audio/change-format_sync/")
async def change_audio_format_sync(file_format: str, file: UploadFile = File(...)):
    try:
        file_format = AudioFormats(format=file_format).format
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    audio_app = AudioApp()

    try:
        audio_app.upload_file(file)
        audio_app.change_format(file_format)
        info = audio_app.get_file_info()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process audio: {e}")

    return {"message": "Audio format changed successfully", "file_info": info}

if __name__ == '__main__':
    """
    Локальный запуск
    """
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    # audio = AudioApp()
    # image = ImageApp()
    #
    # audio.upload_file('')
    # image.upload_file('')
    #
    # audio.get_file_info()
    # image.get_file_info()
    #
    # print()