from pydoc import text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
from TEST.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    create_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default= text('now()'))
