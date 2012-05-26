from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

ed_user = User('ed', 'Ed Jones', 'edspassword')

session.add(ed_user)
session.commit()

for name, fullname in session.query(User.name, User.fullname):
    print name, fullname

