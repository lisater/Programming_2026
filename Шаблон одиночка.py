def get_currencies(currencies_ids_lst: list) -> list:
    import requests
    from xml.etree import ElementTree as ET  # TODO 1: Исследовать самостоятельно есть ли более оптимальная библиотека для парсинга XML или

    # посмотреть есть ли возможность использовать у ЦБ другой API для получения json изначально

    cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    result = []

    root = ET.fromstring(cur_res_str.content)
    valutes = root.findall(
        "Valute"
    ) 
    for _v in valutes:
        valute_id = _v.get('ID')
        valute = {}
        if (str(valute_id) in currencies_ids_lst):
            valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find(
                'Value').text
            valute_charcode = _v.find('CharCode').text
            valute[valute_charcode] = (valute_cur_name, valute_cur_val)
            result.append(valute)

    return result


class CurrenciesLst():

    def __init__(self):

        self.__cur_lst = [{
            'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')
        }, {
            'KZT': ('Казахстанских тенге', '19,8264')
        }, {
            'TRY': ('Турецких лир', '33,1224')
        }]

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        for el in self.__cur_lst:
            currencies.append(str(el.keys()))

        print(currencies)


        
if __name__ == '__main__':

    res = get_currencies(['R01035', 'R01335', 'R01700J'])
    if res:
        print(get_currencies(['R01035', 'R01335', 'R01700J']))
