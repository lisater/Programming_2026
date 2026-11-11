import time


class SingletonMeta(type):
    """Метакласс для шаблона "одиночка""""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CurrenciesLst(metaclass=SingletonMeta):
    """Класс для работы с курсами валют ЦБ РФ."""

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__cur_lst = [
                {'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')},
                {'KZT': ('Казахстанских тенге', '19,8264')},
                {'TRY': ('Турецких лир', '33,1224')}
            ]
            self.__last_request_time = 0.0
            self._initialized = True

    @property
    def cur_lst(self):
        return self.__cur_lst

    @cur_lst.setter
    def cur_lst(self, value):
        self.__cur_lst = value

    @property
    def last_request_time(self):
        return self.__last_request_time

    @last_request_time.setter
    def last_request_time(self, value):
        self.__last_request_time = value

    def visualize_currencies(self):
        pass


if __name__ == '__main__':
    obj1 = CurrenciesLst()
    obj2 = CurrenciesLst()
    print(obj1 is obj2)  
