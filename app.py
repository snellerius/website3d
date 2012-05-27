import glob, random, os, string

from copy import copy

from datetime import datetime
from flask import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Click(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    time = Column(DateTime)
    image = Column(String)
    kunst = Column(Boolean)

    def __init__(self, user, image, kunst):
        self.user = user
        self.time = datetime.now()
        self.image = image
        self.kunst = kunst

    def __repr__(self):
        return "<Click('%s', '%s', '%s', '%s')>" % (self.user, self.time, self.image1, self.kunst)

Base.metadata.create_all(bind=engine)

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


bijschriften = {}
for line in open('bijschrift.csv').readlines():
    k = map(string.strip, line.decode('utf8').split(","))
    f = k[0]
    b = ', '.join(k[1:])
    bijschriften[f] = b

for image in images:
    if not bijschriften.has_key(image):
        bijschriften[image] = ""

@app.route("/")
def index():
    # new user? assign unique id (is stored in cookie)
    if not 'counter' in session:
        session['user'] = random_username()
        session['counter'] = 0
        return render_template("welcome.html")

    r = random.Random()
    r.seed(session['user'])
    ims = copy(images)
    r.shuffle(ims)
    index = session['counter'] % len(images)
    image = ims[index]
    return render_template("index.html", image=image, bijschrift=bijschriften[image])

@app.route("/kunst/<image>/")
def kunst(image):
    if not 'user' in session:
        abort(403)

    # increase counter
    session['counter'] += 1

    c = Click(session["user"], image, True)
    db_session.add(c)
    db_session.commit()

    return redirect(url_for('index'))

@app.route("/weg/<image>/")
def weg(image):

    if not 'user' in session:
        abort(403)

    # increase counter
    session['counter'] += 1

    c = Click(session["user"], image, False)
    db_session.add(c)
    db_session.commit()

    return redirect(url_for('index'))

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/stats/")
def stats():
    return "registered clicks: %d" % len(Click.query.all())

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
