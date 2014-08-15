from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os
import psycopg2
import urlparse

# urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL_LOCAL"])

print url
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)



#import pdb

ENGINE = None
Session = None

ENGINE = create_engine(os.environ.get("DATABASE_URL", "DATABASE_URL_LOCAL"), echo = True)
dbsession = scoped_session(sessionmaker(bind = ENGINE,
                                    autocommit = False,
                                  autoflush = False))
Base = declarative_base()
Base.query = dbsession.query_property()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=True)
    fbid = Column(String, nullable=True)
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
    desc = Column(String(54), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", backref=backref("albums", order_by=id))

    def add_album(self): 
        dbsession.add(self)
        dbsession.commit()

    def album_image_url(self):
        # album.images[0].name|replace(" ","_")
        if len(self.images) > 0:
            return self.images[0].image_url()
            # print self.images[0].extention
            # image_name = str(self.images[0].id) + "." + self.images[0].extention
            # return '/static/uploads/%d/%d/%s' % (self.user_id, self.id,image_name)
        return "/static/default_album.png"


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key = True)
    extention = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=True)

    user = relationship("User", backref=backref("images", order_by=id))
    album = relationship("Album", backref=backref("images", order_by=id))

    

    def add_picture(self): 
        dbsession.add(self)
        dbsession.commit()

    def image_url(self):
        image_name = str(self.id) + "." + self.extention
        image_aws_url = "https://s3-us-west-1.amazonaws.com" + "/" + "photoshare-webapp" + "/" + str(self.user_id) + "/" + str(self.album_id) + "/" + image_name
        print image_aws_url
        return image_aws_url

class Blogpost(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key = True)
    BlogText = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=True)

    user = relationship("User", backref=backref("blogs", order_by=id))
    album = relationship("Album", backref=backref("blogs", order_by=id))

    def add_blog(self): 
        dbsession.add(self)
        dbsession.commit()

# def connect():
#     ENGINE = None
#     Session = None

#     ENGINE = create_engine("sqlite:///photodb.db", echo = False)
#     dbsession = scoped_session(sessionmaker(bind = ENGINE,
#                                         autocommit = False,
#                                         autoflush = False))
#     Base.query = dbsession.query_property()
#     return dbsession()

def create_tables():
    Base.metadata.create_all(ENGINE)

def main():
    """In case we need this for something"""
    
# if __name__ == "__main__":
#     main()