# Тут будут инструменты работы с изображениями
class ImageFile():
    pass
    # валидация изображения

class ImageFormats():
    pass
    # только jpg \ jpeg \ png

class ImageSize():
    pass
    # инт, не может быть отрицательным

class ImageFilter():
    pass
    # Список имеющихся фильров

class ImageParam(): # todo rename
    pass
    # Параметры размещения?

class ImageApp:
    """
    123
    """
    def __init__(self):
        pass

    def upload_file(self, images):
        pass

    def get_file_info(self):
        print('hello world, i am image')
        pass

    def change_format(self, new_format):
        """

        :param new_format:
        :return:
        """
        pass

    def change_size(self, new_size_x: int, new_size_y: int):
        """

        :param new_size_x:
        :param new_size_y:
        :return:
        """
        pass

    def crop_image(self, new_size_x: int, new_size_y: int):
        """

        :param new_size_x:
        :param new_size_y:
        :return:
        """
        pass

    def add_filter(self, filter):
        pass

    def image_stitching(self, images, param):
        pass


def main():
    image = '' # берем картинку из files/
    app = ImageApp()
    app.upload_file(image)
    app.get_file_info()


if __name__ == '__main__':
    main()
