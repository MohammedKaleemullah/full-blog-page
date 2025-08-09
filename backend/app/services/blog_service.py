# app/services/blog_service.py
from sqlalchemy.orm import Session
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogOut, BlogUpdate
from typing import List, Optional
import uuid

from sqlalchemy import cast, String
from sqlalchemy.dialects.postgresql import array


def create_blog(db: Session, blog_data: BlogCreate, user_id: uuid.UUID) -> Blog:
    blog = Blog(
        user_id=user_id,
        title=blog_data.title,
        content=blog_data.content,
        visibility=blog_data.visibility,
        main_image_url=blog_data.main_image_url,
        sub_images=blog_data.sub_images or [],
        tags=blog_data.tags or []
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def get_blogs(
    db: Session,
    limit: int = 10,
    offset: int = 0,
    tags: Optional[list[str]] = None,
    visibility: Optional[str] = "public"
) -> List[Blog]:
    query = db.query(Blog).filter(Blog.is_deleted == False)

    if visibility:
        query = query.filter(Blog.visibility == visibility)

    if tags:
        query = query.filter(Blog.tags.overlap(array(tags, type_=String)))

    return query.offset(offset).limit(limit).all()

def get_blog(db: Session, blog_id: uuid.UUID) -> Blog:
    return db.query(Blog).filter(Blog.id == blog_id, Blog.is_deleted == False).first()

def soft_delete_blog(db: Session, blog_id: uuid.UUID) -> bool:
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        return False
    blog.is_deleted = True
    db.commit()
    return True

def update_blog(db: Session, blog_id: uuid.UUID, blog_data: BlogUpdate) -> Blog:
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.is_deleted == False).first()
    if not blog:
        return None

    for field, value in blog_data.dict(exclude_unset=True).items():
        setattr(blog, field, value)

    db.commit()
    db.refresh(blog)
    return blog
