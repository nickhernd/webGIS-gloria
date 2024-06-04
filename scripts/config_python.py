import os


class ConfigPath:
    @staticmethod
    def root_path():
        # TODO No está bien
        return os.path.dirname(os.getcwd())

    @staticmethod
    def data_path():
        return ConfigPath.root_path() + "/data/"

    @staticmethod
    def scripts_path():
        return ConfigPath.root_path() + "/scripts/"

    @staticmethod
    def keys_path():
        return ConfigPath.root_path() + "/keys/"

    @staticmethod
    def api_openweather():
        with open(ConfigPath.keys_path() + "api_openweather.txt") as f:
            return f.readline().rstrip()
        return None
