from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from shortener.models.base import Base


class Snippet(Base):

    """A snippet url."""

    desktop_redirect = Column(String, nullable=False)
    desktop_redirect_count = Column(Integer, default=0)
    mobile_redirect = Column(String)
    mobile_redirect_count = Column(Integer, default=0)
    tablet_redirect = Column(String)
    tablet_redirect_count = Column(Integer, default=0)
    short_url = Column(String)
