# Тут будет интерфейс фастапи и ендпоинты
from general.audio import AudioApp
from general.image import ImageApp

if __name__ == '__main__':
    audio = AudioApp()
    image = ImageApp()

    audio.upload_file('')
    image.upload_file('')

    audio.get_file_info()
    image.get_file_info()

    print()