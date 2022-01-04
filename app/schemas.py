from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field, validator


# EventBase schema. Базовая схема таблицы событий
class EventBase(BaseModel):
    views: Optional[int] = Field(None, title='Views count', ge=0, example=10)
    clicks: Optional[int] = Field(None, title='Clicks count', ge=0, example=10)
    cost: Optional[float] = Field(None, title='Price in rubles', ge=0, example=1.99)

    # Дополнительная проверка для копеек. Не больше 3-х разрядов, вместе с разделителем.
    @validator('cost')
    def cost_validation(cls, cost):
        if str(cost).find('.') != -1 and len(str(cost)[str(cost).find('.'):]) > 3:
            raise ValueError(f'Invalid cost value: {cost}')
        return cost


# Класс для создания событий, дополнительно нужна дата
class EventCreate(EventBase):
    date: date


#  Класс по умолчанию для показа события
class Event(EventBase):

    class Config:
        orm_mode = True


#  Класс отображения события, согласно заданию дополнительно нужна дата
class EventWithDate(EventBase):
    date: date

    class Config:
        orm_mode = True


# EventDate schema. Базовая схема таблицы с датами
class EventDateBase(BaseModel):
    event_date: date = Field(..., alias='date', title='Event date', example=date.today().strftime('%Y-%m-%d'))

    class Config:
        allow_population_by_field_name = True


# Класс по умолчанию для создания даты
class EventDateCreate(EventDateBase):
    pass


# Класс по умолчанию для отображения даты с привязанными событиями
class EventDate(EventDateBase):
    events: List[Event] = []

    class Config:
        orm_mode = True


# Класс для отображения статистики согласно задания. Кроме полей из БД, выводятся дополнительные поля.
class ShowStatistics(EventBase):
    date: date
    views: int = Field(..., title='Views count', ge=0, example=10)
    clicks: int = Field(..., title='Clicks count', ge=0, example=10)
    cost: float = Field(..., title='Price in rubles', ge=0, decimal_places=2, example=1.99)
    cpc: float = Field(..., title='cpc = cost/clicks', example='cpc = cost/clicks')
    cpm: float = Field(..., title='cpm = cost/views * 1000', example='cpm = cost/views * 1000')

    class Config:
        orm_mode = True


class ResultDelete(BaseModel):
    msg: str = Field(..., example='Statistics deleted successfully')
