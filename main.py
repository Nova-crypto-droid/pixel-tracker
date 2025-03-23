from flask import Flask, request, send_file, jsonify, render_template_string
import json
import datetime

app = Flask(__name__)

@app.route("/pixel")
def pixel():
    ip = get_real_ip()
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

    return send_file("pixel.png", mimetype="image/png")

@app.route("/view")
def view_logs():
    try:
        with open("log.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Logs</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
            table { border-collapse: collapse; width: 100%; background: white; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>Pixel Tracker Logs</h1>
        <table>
            <tr><th>Timestamp</th><th>IP Address</th><th>User Agent</th></tr>
            {% for entry in data %}
                <tr>
                    <td>{{ entry.timestamp }}</td>
                    <td>{{ entry.ip }}</td>
                    <td>{{ entry.user_agent }}</td>
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''

    return render_template_string(html_template, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
