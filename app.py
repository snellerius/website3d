import glob, random, os

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


clicks = []

@app.route("/")
def index():
    image1, image2 = random.sample(images, 2)
    return render_template("index.html", image1=image1, image2=image2)

@app.route("/hotter/<image1>/<image2>/")
def hotter(image1, image2):

    if not 'user' in session:
        session['user'] = random_username()

    click = (session["user"], request.remote_addr, image1, image2)
    print "clicked: ", click

    clicks.append(click)

    return redirect(url_for('index'))

@app.route("/stats/")
def stats():
    return render_template("stats.html", clicks=clicks)

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
