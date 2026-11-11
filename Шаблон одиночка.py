import time
import requests
from xml.etree import ElementTree as ET


class SingletonMeta(type):
    """Метакласс для шаблона "одиночка"."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CurrenciesLst(metaclass=SingletonMeta):
    """Класс для работы с курсами валют ЦБ РФ."""

    CBR_URL = 'http://www.cbr.ru/scripts/XML_daily.asp'

    def __init__(self, min_interval: float = 1.0):
        if not hasattr(self, '_initialized'):
            self.__cur_lst = []
            self.__last_request_time = 0.0
            self.__min_interval = min_interval
            self._initialized = True

    def __del__(self):
        self.__cur_lst = []
        self.__last_request_time = 0.0

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

    @property
    def min_interval(self):
        return self.__min_interval

    @min_interval.setter
    def min_interval(self, value):
        self.__min_interval = value

    @staticmethod
    def _split_value(value_str: str):
        """Функция которая разбивает валюту на целую и дробную часть"""
        value_str = value_str.replace(' ', '')
        if ',' in value_str:
            int_part, frac_part = value_str.split(',', 1)
        else:
            int_part, frac_part = value_str, ''
        return int_part, frac_part

    def _throttle(self):
        """Функция, контролирующая сколько прошло времени с запроса"""
        elapsed = time.time() - self.__last_request_time
        if elapsed < self.__min_interval:
            time.sleep(self.__min_interval - elapsed)

    def fetch_currencies(self, currencies_ids_lst: list) -> list:
        """Функция, которая получает курсы валют с ЦБ РФ по списку ID."""
        self._throttle()

        response = requests.get(self.CBR_URL)
        response.raise_for_status()
        self.__last_request_time = time.time()

        result = []
        found_ids = set()

        root = ET.fromstring(response.content)
        for _v in root.findall('Valute'):
            valute_id = _v.get('ID')
            if valute_id not in currencies_ids_lst:
                continue

            name_el = _v.find('Name')
            value_el = _v.find('Value')
            charcode_el = _v.find('CharCode')
            nominal_el = _v.find('Nominal')

            if name_el is None or value_el is None or charcode_el is None:
                continue

            name = name_el.text
            charcode = charcode_el.text
            int_part, frac_part = self._split_value(value_el.text)

            nominal = nominal_el.text if nominal_el is not None else '1'
            try:
                nominal_int = int(nominal)
            except ValueError:
                nominal_int = 1

            if nominal_int != 1:
                result.append({charcode: (name, (int_part, frac_part), nominal_int)})
            else:
                result.append({charcode: (name, (int_part, frac_part))})

            found_ids.add(valute_id)

        for req_id in currencies_ids_lst:
            if req_id not in found_ids:
                result.append({req_id: None})

        self.__cur_lst = result
        return result

    def visualize_currencies(self, filename: str = 'currencies.jpg'):
        """Функция котрая строит график курсов и сохраняет в файл."""
        import matplotlib
        matplotlib.use('Agg') 
        import matplotlib.pyplot as plt

        labels = []
        values = []
        for item in self.__cur_lst:
            for charcode, data in item.items():
                if data is None:
                    continue
                name, (int_part, frac_part) = data[0], data[1]
                labels.append(charcode)
                values.append(int(int_part))

        if not labels:
            print("Нет данных для визуализации.")
            return

        fig, ax = plt.subplots()
        ax.bar(labels, values, color='tab:blue')
        ax.set_ylabel('Курс (целая часть, руб.)')
        ax.set_title('Курсы валют ЦБ РФ')
        plt.savefig(filename)
        plt.close(fig)


if __name__ == '__main__':
    currencies = CurrenciesLst()

    ids = ['R01035', 'R01335', 'R01700J']  # GBP, KZT, TRY
    print("Курсы:", currencies.fetch_currencies(ids))
    currencies.visualize_currencies()
