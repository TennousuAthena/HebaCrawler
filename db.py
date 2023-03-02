from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///data/results.db', echo=True)
# 映射基类
Base = declarative_base()


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    Key = Column(String(30))
    Value = Column(String(128))


class Thread(Base):
    __tablename__ = 'threads'

    TId = Column(Integer, primary_key=True)
    Title = Column(String(256))
    Href = Column(String(64))
    Author = Column(String(16))
    Content = Column(String(4096))


class Comment(Base):
    __tablename__ = 'comments'

    Pid = Column(Integer, primary_key=True)
    Author = Column(String(16))
    Content = Column(String(8192))
    MotherThread = Column(Integer)
    CreatedAt = Column(Integer)


class SmallComment(Base):
    __tablename__ = 'small_comments'

    SPid = Column(Integer, primary_key=True)
    Author = Column(String(16))
    Content = Column(String(1024))
    MotherComment = Column(Integer)
    CreatedAt = Column(Integer)


# 创建表
Base.metadata.create_all(engine)
