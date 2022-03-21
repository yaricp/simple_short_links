from datetime import datetime
from pydantic import AnyUrl
from hashids import Hashids

from sqlalchemy import delete

from models.link import Link
from routers import deps


def get_short_url(long_url: AnyUrl):
    """Creates short link from a long link"""
    hashids = Hashids(long_url)
    return hashids.encode(123456)


def remove_expired_links():
    """Removes all link objects in database if date expired"""
    db = deps.get_db()
    statement = delete(Link).where(Link.expired < datetime.utcnow())
    db.execute(statement=statement)
