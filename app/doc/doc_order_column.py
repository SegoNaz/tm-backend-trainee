from enum import Enum


# Установки параметра сортировки. Данные для документации.
class OrderColumn(str, Enum):
    date = 'date'
    views = 'views'
    clicks = 'clicks'
    cost = 'cost'
    cpc = 'cpc'
    cpm = 'cpm'
