from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Data(Base):
    __tablename__ = 'datas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    feed_id = Column(Integer, ForeignKey('feeds.id'), nullable=False)
    subject = Column(String(200), nullable=False)
    actions = Column(String(1000), nullable=True)
    object = Column(String(1000), nullable=True)
    locations = Column(String(500), nullable=True)
    effect = Column(String(50), nullable=False)
    ts = Column(BigInteger, nullable=False)

class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False, unique=True)
    filter_data = Column(String(50), nullable=True)
    field_mapping = Column(String(50), nullable=True)
    model_saved = Column(Integer, ForeignKey('models.id'), nullable=True)
    prompt_request = Column(Integer, ForeignKey('prompts.id'), nullable=True)
    timeout = Column(Integer, nullable=True)

class Model(Base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(1000), nullable=False)

class Prompt(Base):
    __tablename__ = 'prompts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(1000), nullable=False)