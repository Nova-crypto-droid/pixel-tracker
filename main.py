from flask import Flask, request, send_file
import json
import datetime

app = Flask(__name__)

@app.route("/pixel")
def pixel():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "timestamp": timestamp,
        "ip": ip,
        "user_agent": ua
    }

    try:
        with open("log.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("log.json", "w") as f:
        json.dump(data, f, indent=4)

    return send_file("pixil-frame-0.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
