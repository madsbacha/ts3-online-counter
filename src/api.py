from flask import Flask, render_template
from redis import Redis
from utils import env

app = Flask(__name__)
@app.route("/")
def client_count():
    r = Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0)
    counter = r.get('counter')
    counter = counter.decode("ascii") if counter else None
    return render_template("index.html", online_count=counter)
  
if __name__ == "__main__":
    app.run(host="0.0.0.0")