from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel


class Notice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    updated: str
    url: str
    content: str = ""


engine = create_async_engine("sqlite+aiosqlite:///./data/notice.db")
