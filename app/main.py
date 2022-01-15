from fastapi import FastAPI

from . database import engine
from . import models
from . api_description import api_description, tags_metadata
from . handlers import api_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title='Trade Market API', openapi_url='/openapi.json', version='1.0', description=api_description,
              openapi_tags=tags_metadata)


app.include_router(api_router)
