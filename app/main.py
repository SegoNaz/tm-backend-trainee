from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, Query
from . database import SessionLocal, engine
from . import crud, models, schemas

from . doc.doc_order_column import OrderColumn
from . doc.doc_description import api_description, tags_metadata


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Trade Market API', openapi_url='/openapi.json', version='1.0', description=api_description,
              openapi_tags=tags_metadata)
api_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get('/api/v1/stat', response_model=List[schemas.ShowStatistics], tags=['get stat'])
def read_statistics(
        from_date: date = Query(date.today().strftime('%Y-%m-%d'), alias='from',
                                description='Start date, default today'),
        to_date: date = Query(date.today().strftime('%Y-%m-%d'), alias='to', description='End date, default today'),
        order_column: Optional[OrderColumn] = Query('date', description='Column for sorting'),
        db: Session = Depends(get_db)):
    events = crud.get_events_by_event_date(db=db, from_date=from_date, to_date=to_date, order_column=order_column)
    return events


@api_router.post('/api/v1/stat', response_model=schemas.EventWithDate, tags=['post stat'], status_code=201)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@api_router.delete('/api/v1/stat', response_model=schemas.ResultDelete, tags=['delete stat'])
def delete_statistic(db: Session = Depends(get_db)):
    return crud.delete_statistics(db=db, tables=(models.EventDate, models.Event))


app.include_router(api_router)
