from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, BigInteger, DateTime

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    avatar_url = Column(String(200), nullable=False)

    title = Column(String(100), default="플레이어")
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)

    token = Column(Integer, default=0)
    star = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    last_command_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User[{self.id}](username={self.username})>"
