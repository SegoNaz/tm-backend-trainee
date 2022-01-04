from sqlalchemy import Column, ForeignKey, Integer, Float, Date
from sqlalchemy.orm import relationship
from . database import Base


# Связь один ко многим. Одна дата может быть у нескольких событий.
class EventDate(Base):
    __tablename__ = 'event_date'

    id = Column(Integer, primary_key=True, index=True)
    event_date = Column(Date, index=True)

    join_events = relationship('Event', back_populates='aggr_date', cascade="all, delete", passive_deletes=True)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    views = Column(Integer)
    clicks = Column(Integer)
    cost = Column(Float)
    date_id = Column(Integer, ForeignKey('event_date.id', ondelete="CASCADE"))

    aggr_date = relationship('EventDate', back_populates='join_events')



