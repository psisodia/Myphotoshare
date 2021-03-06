from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
#import pdb

# ENGINE = None
# Session = None

ENGINE = create_engine("sqlite:///photodb.db", echo = False)
dbsession = scoped_session(sessionmaker(bind = ENGINE,
                                    autocommit = False,
                                    autoflush = False))
Base = declarative_base()
Base.query = dbsession.query_property()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    email = Column(String(35), nullable=True)
    
    
    def add_user(self): 
        dbsession.add(self)
        dbsession.commit()

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key= True)
    name = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # pic_id = Column(Integer, nullable=False)

    user = relationship("User", backref=backref("album", order_by=id))

    def add_album(self): 
        dbsession.add(self)
        dbsession.commit()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable=False)
    img_path = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    album_id = Column(Integer, ForeignKey('album.id'), nullable=True)

    user = relationship("User", backref=backref("image", order_by=id))
    album = relationship("Album", backref=backref("image", order_by=id))

    def add_picture(self): 
        dbsession.add(self)
        dbsession.commit()

def connect():
    ENGINE = None
    Session = None

    ENGINE = create_engine("sqlite:///photodb.db", echo = False)
    dbsession = scoped_session(sessionmaker(bind = ENGINE,
                                        autocommit = False,
                                        autoflush = False))
    # Base = declarative_base()
    Base.query = dbsession.query_property()
    return dbsession()

def main():
    """In case we need this for something"""
    
# if __name__ == "__main__":
#     main()