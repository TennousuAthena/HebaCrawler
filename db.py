from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///data/results.db', echo=True)
# 映射基类
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Status(Base):
    """当前Bot状态记录"""
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    Key = Column(String(30))
    Value = Column(String(128))


class Thread(Base):
    """帖子信息记录"""
    __tablename__ = 'threads'

    tId = Column(Integer, primary_key=True)
    Title = Column(String(256))
    Href = Column(String(64))
    Author = Column(String(16))
    Content = Column(String(4096))


class Comment(Base):
    """帖子回复"""
    __tablename__ = 'comments'

    Pid = Column(Integer, primary_key=True)
    Author = Column(String(16))
    Content = Column(String(8192))
    MotherThread = Column(Integer)
    CreatedAt = Column(Integer)


class SmallComment(Base):
    """楼中楼信息"""
    __tablename__ = 'small_comments'

    SPid = Column(Integer, primary_key=True)
    Author = Column(String(16))
    Content = Column(String(1024))
    MotherComment = Column(Integer)
    CreatedAt = Column(Integer)


Base.metadata.create_all(engine)
