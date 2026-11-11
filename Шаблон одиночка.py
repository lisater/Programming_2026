def get_currencies(currencies_ids_lst: list) -> list:
    import requests
    from xml.etree import ElementTree as ET  # TODO 1: Исследовать самостоятельно есть ли более оптимальная библиотека для парсинга XML или

    # посмотреть есть ли возможность использовать у ЦБ другой API для получения json изначально

    cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    result = []

    root = ET.fromstring(cur_res_str.content)
    valutes = root.findall(
        "Valute"
    )  # исследовать, есть ли отдельный метод получения валют с опреденным id
    # если да, упростить алгоритм ниже
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
        # fruits = ['apple', 'blueberry', 'cherry', 'orange']
        # counts = [40, 100, 30, 55]
        # bar_labels = ['red', 'blue', '_red', 'orange']
        # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

        # ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        # ax.set_ylabel('fruit supply')
        # ax.set_title('Fruit supply by kind and color')
        # ax.legend(title='Fruit color')

        # plt.show()

        # обращается к атрибуту __cur_lst, преобразовывать значения курсов валют в нужный формат и выводить эти данные в файл

        # self.__cur_lst

        
if __name__ == '__main__':

    res = get_currencies(['R01035', 'R01335', 'R01700J'])
    if res:
        print(get_currencies(['R01035', 'R01335', 'R01700J']))
