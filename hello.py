from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
#def hello_world():
#   return "<p>Hello, World!</p>"

def index():
   return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404