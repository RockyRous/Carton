# Тут будут инструменты работы с аудио
class AudioFile():
    pass
    # валидация аудио


class AudioFormats():
    pass
    # только mp3 / wav и др

class AudioParamCutting():
    pass

class AudioParamCleaning():
    pass

class AudioSpeed():
    pass # Ограничения

class AudioParamSplicing():
    pass


class AudioApp:
    """
    123
    """

    def __init__(self):
        pass

    def upload_file(self, audio):
        pass

    def get_file_info(self):
        print('hello world, i am audio')
        pass

    def change_format(self, new_format):
        """

        :param new_format:
        :return:
        """
        pass

    def cutting(self, param_cutting):
        pass

    def cleaning(self, param_cleaning):
        pass

    def change_speed(self, new_speed: float):
        pass

    def audio_splicing(self, audio, param_splicing):
        pass


def main():
    audio = '' # берем аудио из files/
    app = AudioApp()
    app.upload_file(audio)
    app.get_file_info()


if __name__ == '__main__':
    main()







