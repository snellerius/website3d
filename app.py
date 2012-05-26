import glob, random, os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from sqlalchemy import Column, Integer, String

class Click(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    ip = Column(String)
    image1 = Column(String)
    image2 = Column(String)

    def __init__(self, user, ip, image1, image2):
        self.user = user
        self.ip = ip
        self.image1 = image1
        self.image2 = image2

    def __repr__(self):
        return "<Click('%s', '%s', '%s', '%s')>" % (self.user, self.ip, self.image1, self.image2)

Base.metadata.create_all(bind=engine)

from flask import *

# set random seed
random.seed(os.urandom(128))

app = Flask(__name__)

# fixed secret key for secure cookies
app.secret_key = 'WUM6X]iYC#r|Cq5nYGUu<6:iR.ng[_nTy8k}|MLM'

# create list of images, strip "static/"
f = lambda s: s.replace("static/","")
images = map(f, glob.glob("static/*.jpg"))

# alphabet for random username
K = "0123456789abcdefghijklmnopqrstuvwxyz"
def random_username():
    return ''.join([str(random.choice(K)) for i in range(12)])

#clicks = []

@app.route("/")
def index():
    image1, image2 = random.sample(images, 2)
    return render_template("index.html", image1=image1, image2=image2)

@app.route("/hotter/<image1>/<image2>/")
def hotter(image1, image2):

    # new user? assign unique id (is stored in cookie)
    if not 'user' in session:
        session['user'] = random_username()

    # create database row (session, ip, im1, im2)
    c = Click(session["user"], request.remote_addr, image1, image2)
    db_session.add(c)
    db_session.commit()

    return redirect(url_for('index'))

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/stats/")
def stats():
    return render_template("stats.html", clicks=Click.query.all())

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")

