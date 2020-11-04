from flask import Flask, render_template
from redis import Redis
from utils import env, fromb64

app = Flask(__name__)
@app.route("/")
def client_count():
    r = Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0)
    counter = r.get('counter')
    counter = counter.decode("ascii") if counter else None
    usernames = r.get('usernames')
    usernames = [fromb64(x) for x in usernames.decode("ascii").split(',')] if usernames else []
    return render_template("index.html", online_count=counter, usernames=usernames)
  
if __name__ == "__main__":
    app.run(host="0.0.0.0")