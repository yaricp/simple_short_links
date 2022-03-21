from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from schemas.link import LinkIn, Link, LinkUpdate
from schemas.user import User
from models.link import Link as LinkModel
from utils.links import get_short_url
from settings import SHORT_LINK_EXPIRE_DAYS

from .deps import get_db, get_current_user


router = APIRouter()


@router.get("/{short_text}")
def redirect_to_long_url(
    *,
    db: Session = Depends(get_db),
    short_text: str,
) -> Any:
    """
    Gets link by short url and redirects to long url
    """
    link = db.query(LinkModel).filter(
        LinkModel.short_text == short_text
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(link.text)


@router.get("/api/links", response_model=List[Link])
async def read_links(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve links.
    Admin can get all links. Other users can get only own links
    """
    if current_user.is_admin:
        links = (
            db.query(LinkModel)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        links = (
            db.query(LinkModel)
            .filter(LinkModel.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    return links


@router.post("/api/links", response_model=Link)
async def create_link(
    *,
    item_in: LinkIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Test if link with text exists then return one.
    Create new link if not found.
    """
    link = db.query(LinkModel).filter(LinkModel.text == item_in.text).first()
    if link:
        return Link(
            id=link.id,
            text=link.text,
            short_text=link.short_text,
            expired=link.expired,
            owner_id=link.owner_id
        )
    short_text = get_short_url(item_in.text)
    db_obj = LinkModel(
        text=item_in.text,
        short_text=short_text,
        expired=datetime.utcnow() + timedelta(
            days=SHORT_LINK_EXPIRE_DAYS
        ),
        owner_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.put("/api/link/{id}", response_model=Link)
def update_link(
    *,
    db: Session = Depends(get_db),
    id: int,
    item_in: LinkUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a link.
    Admin cat edit any links. Usual user can edit only own links.
    """
    db_obj = db.query(LinkModel).get(id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Link not found")
    if not current_user.is_admin and (db_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    hero_data = item_in.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/api/link/{id}", response_model=Link)
def read_link(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get link by ID.
    Admin get get any link. Regular user cat get only own link.
    """
    db_obj = db.query(LinkModel).get(id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Link not found")
    if not current_user.is_admin and (db_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return Link(
        id=db_obj.id,
        text=db_obj.text,
        short_text=db_obj.short_text,
        expired=db_obj.expired,
        owner_id=db_obj.owner_id
    )


@router.delete("/api/link/{id}")
def delete_link(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete an link.
    Admin can delete any links. Other users ca delete only their own links
    """
    db_obj = db.query(LinkModel).get(id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Link not found")
    if not current_user.is_admin and (db_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    db.delete(db_obj)
    db.commit()
    return {"deleted": True}
