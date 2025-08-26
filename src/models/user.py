from sqlalchemy import Column, Integer, String, BigInteger

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)

    token = Column(Integer, default=0)

    def __repr__(self):
        return f"<User[{self.id}](username={self.username})>"
