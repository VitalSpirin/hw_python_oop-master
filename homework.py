import datetime as dt
from typing import Dict, List, Optional, Tuple


Format: str = '%d.%m.%Y'

class Record:
    """ Создает записи о:
        1. денежной сумме/калориях
        2. комментарий на что потрачены/как получены
        3. дата создания записи"""

    def __init__(self, amount: float, comment: str, date: Optional[str] = None) -> None:
        self.amount: float = amount
        self.comment: str = comment
        self.date: dt.date = dt.datetime.strptime(date,Format).date() if date is not None else dt.datetime.today().date()


class Calculator:
    """Основной функционал обоих калькуляторов"""

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.records: List[Record] =[]

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) ->float:
        today: dt.date = dt.date.today()
        return sum([x.amount for x in self.records if x.date == today])


    def get_today_balance(self) -> float:
        """Получить данные о балансе/доступных калориях на текущий момент."""
        return self.limit - self.get_today_stats()


    def get_week_stats(self) -> float:
        today: dt.date = dt.date.today()
        week_ago: dt.date = today - dt.timedelta(days=7)
        return sum([x.amount for x in self.records if week_ago < x.date <= today])

class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        x: float = self.limit - self.get_today_stats()
        return f"Сегодня можно сьесть еще, но не более {x} калорий" if x > 0 else "Хватит жрать!"

class CashCalculator(Calculator):

    usd_rate: float = 61.47
    euro_rate: float = 63.66

    def get_today_cash_remained(self, currency: str) -> str:
        self.currency = currency
        busket_of_currency: dict = { "RUB" : 1, "USD" : self.usd_rate, "EURO" : self.euro_rate}

        if self.currency not in busket_of_currency.keys():
            print(f'Такой валюты {self.currency} не существует')

        cash_in_currency: float = round(self.get_today_balance()/busket_of_currency[currency],2)

        if cash_in_currency == 0:
            return f"Денег нет, держись"

        if self.get_today_balance() >0:
            return f"На сегодня осталось {cash_in_currency} в {currency} "
        else:
            return f"Денег нет, держись, твой долг {cash_in_currency} в {currency}"

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))


# print(type(dt.date.today()))
# print(type(dt.datetime.today()))
print(cash_calculator.get_today_cash_remained('RUB'))
# должно напечататься
# На сегодня осталось 555 руб