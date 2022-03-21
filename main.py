from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from routers.links import router as link_router
from routers.users import router as user_router

from db import Base, engine
from settings import TIME_CHECK_EXPIRED_LINKS_SECONDS
from utils.links import remove_expired_links
import models  # noqa

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(link_router)
app.include_router(user_router)


# Periodic task for delete links with date expired
@app.on_event("startup")
@repeat_every(seconds=TIME_CHECK_EXPIRED_LINKS_SECONDS)
def remove_expired_links_task() -> None:
    remove_expired_links()
