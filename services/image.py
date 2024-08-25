# Тут будут инструменты работы с изображениями
# todo:
# make async?
# Добавить в инфо файла его расположение

from typing import Optional, Union

from pydantic import BaseModel, field_validator
from PIL import Image
from PIL.Image import Resampling
import os
from fastapi import UploadFile, HTTPException

# Допустимые форматы изображений
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg"]
ALLOWED_IMAGE_FORMATS = ["image/png", "image/jpeg"]
ALLOWED_IMAGE_FILTERS = []  # in progress


class ImageFile(BaseModel):
    file: Union[UploadFile, str]

    @field_validator("file")
    def validate_file(cls, v: Union[UploadFile, str]):
        # Если передан UploadFile
        if isinstance(v, UploadFile):
            # Проверяем тип файла (MIME-тип)
            if v.content_type not in ALLOWED_IMAGE_FORMATS:
                raise HTTPException(status_code=400, detail="Invalid image format. Only PNG and JPG are allowed.")

            # Проверяем расширение файла
            extension = v.filename.split(".")[-1].lower()
            if extension not in ALLOWED_IMAGE_EXTENSIONS:
                raise HTTPException(status_code=400, detail="Invalid image extension. Only .png and .jpg are allowed.")

        # Если передан путь к локальному файлу
        elif isinstance(v, str):
            if not os.path.isfile(v):
                raise HTTPException(status_code=400, detail="File path is invalid or file does not exist.")

            # Проверяем расширение файла
            extension = os.path.splitext(v)[1].lower().strip(".")
            if extension not in ALLOWED_IMAGE_EXTENSIONS:
                raise HTTPException(status_code=400, detail="Invalid image extension. Only .png and .jpg are allowed.")

        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Must be an UploadFile or a file path.")

        return v


class ImageFormats(BaseModel):
    format: str

    @field_validator("format")
    def validate_format(cls, v: str):
        if v.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid format. Only 'png' and 'jpg' are allowed.")
        return v.lower()


class ImageSize(BaseModel):
    x: int
    y: int

    @field_validator("x", "y")
    def validate_size(cls, v: int):
        if v < 0:
            raise HTTPException(status_code=400, detail="Size must be a non-negative integer.")
        return v


class ImageFilter(BaseModel):
    filter: str

    @field_validator("filter")
    def validate_filter(cls, v: str):
        if v.lower() not in ALLOWED_IMAGE_FILTERS:
            raise HTTPException(status_code=400, detail=f"Invalid filter. Allowed filters are: {', '.join(ALLOWED_IMAGE_FILTERS)}.")
        return v.lower()


class ImageParam(BaseModel): # todo rename  # in progress
    pass
    # Параметры размещения?


class ImageApp:
    """
    123
    """
    def __init__(self):
        self.image = None
        self.name = None
        self.format = None
        self.size = None

    def upload_file(self, file: ImageFile):
        if type(file) is str:  # Для работы с локальными файлами
            self.image = Image.open(file)
            self.name = file.split('/')[-1].split('.')[0]
        else:
            self.image = Image.open(file.file)
            self.name = file.filename
        self.format = self.image.format.lower()
        if self.format == 'jpg':
            self.format = 'jpeg'
        self.size = self.image.size

    def save_file(self, filename: Optional[str] = None):
        if self.image is None:
            return "Файл отсутствует"

        if filename is None:
            filename = self.name
        else:
            self.name = filename

        self.image.save(f'../files/{filename}.{self.format}', format=self.format)
        return f"Изображение сохранено как {filename} в формате {self.format}"

    def get_file_info(self):
        if self.image is None:
            return "Файл отсутствует"
        return {
            "name": self.name,
            "format": self.format,
            "size": self.size
        }

    def change_format(self, new_format: ImageFormats):
        if self.format == new_format.lower():
            return "Формат уже установлен"

        if new_format == 'jpg':
            new_format = 'jpeg'

        self.format = new_format.lower()

        # Преобразование изображения в формат RGB, если оно в формате RGBA
        if self.format == 'jpeg' and self.image.mode in ('RGBA', 'P'):
            # Преобразуем изображение в RGB
            self.image = self.image.convert('RGB')

        return f"Формат изменен на {new_format.lower()}"

    def change_size(self, new_size: ImageSize):
        if self.image is None:
            return "Файл отсутствует"
        x, y = new_size

        self.image = self.image.resize((x, y), Resampling.LANCZOS)
        self.size = (x, y)
        return f"Размер изменен на {x}x{y}"

    def crop_image(self, new_size: ImageSize):
        if self.image is None:
            return "Файл отсутствует"

        x, y = new_size
        current_width, current_height = self.image.size

        # Вычисляем размеры для центрирования
        left = (current_width - x) / 2
        top = (current_height - y) / 2
        right = (current_width + x) / 2
        bottom = (current_height + y) / 2

        # Создаем новое изображение с белым фоном
        new_image = Image.new("RGB", (x, y), (0, 0, 0))  # Изменение цвета не работает :С Всегда черный
        # new_image = Image.new("RGBA", (x, y), (255, 0, 0, 0))

        # Вставляем старое изображение в новое
        new_image.paste(self.image.crop((left, top, right, bottom)), (0, 0))
        # new_image.paste(self.image.crop((left, top, right, bottom)), (0, 0), self.image.crop((left, top, right, bottom)).convert("RGBA"))

        self.image = new_image
        self.size = (x, y)
        return f"Изображение обрезано/изменено до {x}x{y}"


    def add_filter(self, filter):
        pass

    def image_stitching(self, images, param):
        pass


def main():
    image = '321.png'
    app = ImageApp()
    app.upload_file(f'../files/{image}')
    print(app.get_file_info())

    app.change_format('jpg')
    print(app.get_file_info())
    app.save_file()

    # app.change_size((100, 100))
    # print(app.get_file_info())
    # app.save_file('100x100')
    # app.change_format('png')
    # print(app.get_file_info())
    # app.crop_image((500, 500))
    # print(app.get_file_info())
    # app.save_file('500x500')


if __name__ == '__main__':
    main()
