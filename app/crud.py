from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status

from . import models as md
from . import schemas as sc

# Константа для: средняя стоимость 1000 показов. cpm = cost/views * SHOW_COUNT
from .settings import settings


def get_events_by_event_date(db: Session, from_date: date, to_date: date, order_column):
    query = db.query(md.EventDate.event_date.label('date'),
                     func.sum(md.Event.views).label('views'),
                     func.sum(md.Event.clicks).label('clicks'),
                     (func.round(func.sum(md.Event.cost), 2)).label('cost'),
                     (func.round(func.sum(md.Event.cost) / func.sum(md.Event.clicks), 3)).label('cpc'),
                     (func.round((func.sum(md.Event.cost) / func.sum(md.Event.views)) * settings.show_count, 3))
                     .label('cpm')) \
        .filter(and_(md.Event.clicks > 0, md.Event.views > 0, md.Event.cost.is_not(None))) \
        .join(md.EventDate).filter(md.EventDate.event_date.between(from_date, to_date)) \
        .group_by(md.EventDate.event_date)
    query = query.order_by(order_column).all()
    if not query:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return query


def create_event(db: Session, event: sc.EventCreate):
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
    for table in tables:
        db.query(table).delete()
        db.commit()
