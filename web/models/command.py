from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY

from database import Base


class Command(Base):
    __tablename__ = 'commands'

    name = Column(String(50), primary_key=True)
    aliases = Column(ARRAY(String(50)), default=[])

    help = Column(String, default="")
    usage = Column(String, default="")
