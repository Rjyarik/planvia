from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sight(Base):
    __tablename__ = 'sights'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    image = Column(String)
    coordinates = Column(String)
    address = Column(String)