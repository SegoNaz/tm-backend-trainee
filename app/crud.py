from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, cast, Numeric

from . import models as md
from . import schemas as sc

# Константа для: средняя стоимость 1000 показов. cpm = cost/views * SHOW_COUNT
SHOW_COUNT = 1000


def get_events_by_event_date(db: Session, from_date: date, to_date: date, order_column):
    """
    Согласно ТЗ: Функция формирует данные:
    date - дата события
    views - количество показов
    clicks - количество кликов
    cost - стоимость кликов
    cpc = cost/clicks (средняя стоимость клика). 3 знака после запятой.
    cpm = cost/views * 1000 (средняя стоимость 1000 показов). 3 знака после запятой.
    Агрегация по дате.
    Фильтр по дате (from, to), включительно.
    Сортировка по любому полю.
    """
    if order_column not in sc.ShowStatistics.__fields__:
        order_column = 'date'
    query = db.query(md.EventDate.event_date.label('date'),
                     func.sum(md.Event.views).label('views'),
                     func.sum(md.Event.clicks).label('clicks'),
                     (cast(func.sum(md.Event.cost), Numeric(12, 2))).label('cost'),
                     (cast(func.sum(md.Event.cost) / func.sum(md.Event.clicks), Numeric(12, 3))).label('cpc'),
                     (cast((func.sum(md.Event.cost) / func.sum(md.Event.views))*SHOW_COUNT, Numeric(12, 3))).label('cpm'))\
        .filter(and_(md.Event.clicks > 0, md.Event.views > 0, md.Event.cost.is_not(None))) \
        .join(md.EventDate).filter(md.EventDate.event_date.between(from_date, to_date)) \
        .group_by(md.EventDate.event_date)
    query = query.order_by(order_column)
    return query.all()


def create_event(db: Session, event: sc.EventCreate):
    """
    Функция сохранения статистики.
    Принимает на вход:
    date - дата события
    views - количество показов
    clicks - количество кликов
    cost - стоимость кликов (в рублях с точностью до копеек)
    EventCreate - pydanic схема для создания данных
    Поля views, clicks и cost - опциональные. Статистика агрегируется по дате (при выводе данных).
    """
    # Проверяем существует ли дата
    db_date = db.query(md.EventDate).filter(md.EventDate.event_date == event.date).first()
    # Если даты нет, создаём ее
    if not db_date:
        db_new_date = md.EventDate(event_date=event.date)
        db.add(db_new_date)
        db.commit()
        db.refresh(db_new_date)
        db_date = db_new_date
    # Дата присутствует в базе, создаём событие
    db_new_event = md.Event(views=event.views, cost=event.cost, clicks=event.clicks, date_id=db_date.id)
    db.add(db_new_event)
    db.commit()
    db.refresh(db_new_event)
    return {'cost': db_new_event.cost, 'views': db_new_event.views, 'clicks': db_new_event.clicks,
            'date': db_new_event.aggr_date.event_date}


def delete_statistics(db: Session, tables: tuple):
    """
    Функция очищает таблицы от данных.
    """
    for table in tables:
        db.query(table).delete()
        db.commit()
    return {'msg': 'Statistics deleted successfully'}

