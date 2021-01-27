from flask import Flask, render_template
from redis import Redis
from utils import env
import base64

app = Flask(__name__)
@app.route("/")
def client_count():
    counter = "0"
    usernames = []
    try:
        r = Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0)
        counter = r.get('counter')
        counter = counter.decode("utf8") if counter else None
        usernames = r.get('usernames')
        usernames = [base64.b64decode(x.encode('utf8')).decode('utf8') for x in usernames.decode("utf8").split(',')] if usernames else []
    except Exception:
        pass
    return render_template("index.html", online_count=counter, usernames=usernames)

@app.route("/api")
def client_count_api():
    counter = "0"
    usernames = []
    try:
        r = Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0)
        counter = r.get('counter')
        counter = counter.decode("utf8") if counter else None
        usernames = r.get('usernames')
        usernames = [base64.b64decode(x.encode('utf8')).decode('utf8') for x in usernames.decode("utf8").split(',')] if usernames else []
    except Exception:
        pass

    return {
      'count': counter,
      'users': usernames
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0")