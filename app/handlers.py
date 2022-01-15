from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Query, status, Response

from . database import get_db
from . import crud, models, schemas


api_router = APIRouter(prefix='/api/v1')


@api_router.get('/stat', response_model=List[schemas.ShowStatistics], tags=['statistics'])
def read_statistics(
        from_date: date = Query(date.today().strftime('%Y-%m-%d'), alias='from',
                                description='Start date, default today'),
        to_date: date = Query(date.today().strftime('%Y-%m-%d'), alias='to', description='End date, default today'),
        order_column: Optional[schemas.OrderColumn] = Query('date', description='Column for sorting'),
        db: Session = Depends(get_db)):
    """
    ## Функция формирует данные:
    - ***date*** - дата события
    - ***views*** - количество показов
    - ***clicks*** - количество кликов
    - ***cost*** - стоимость кликов
    - ***cpc*** = cost/clicks (средняя стоимость клика). 3 знака после запятой.
    - ***cpm*** = cost/views * 1000 (средняя стоимость 1000 показов). 3 знака после запятой.
    Агрегация по дате.
    Фильтр по дате (***from***, ***to***), включительно.
    Сортировка по любому полю.
    \f
    :param from_date:
    :param to_date:
    :param order_column:
    :param db:
    :return:
    """
    events = crud.get_events_by_event_date(db=db, from_date=from_date, to_date=to_date, order_column=order_column)
    return events


@api_router.post('/stat', response_model=schemas.EventWithDate, tags=['events'], status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    ## Функция сохранения статистики.
    Принимает на вход:
    - ***date*** - дата события
    - ***views*** - количество показов
    - ***clicks*** - количество кликов
    - ***cost*** - стоимость кликов (в рублях с точностью до копеек)
    Поля ***views***, ***clicks*** и ***cost*** - опциональные.
    """
    return crud.create_event(db=db, event=event)


@api_router.delete('/stat', tags=['events'], name='Clear events data')
def delete_statistic(db: Session = Depends(get_db)):
    """
    ## Функция очищает таблицы от данных.
    \f
    :param db:
    :return:
    """
    crud.delete_statistics(db=db, tables=(models.EventDate, models.Event))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
