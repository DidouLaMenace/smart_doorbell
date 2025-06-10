from flask import Flask, request, jsonify, render_template
from events.logger import log
from notifications.notifier import send_notification
from database.db_utils import init_db, get_all_events
import os

app = Flask(__name__, template_folder="templates")


EVENT_MESSAGES = {
    "sound": "Un bruit a été détecté !",
    "move": "Une présence a été détectée !",
    "button": "Une personne a appuyé sur la sonnette !"
}


@app.route("/event", methods=["POST"])
def event():
    data = request.get_json()
    event_type = data.get("event_type")
    log(event_type)

    message = EVENT_MESSAGES.get(event_type, f"Événement inconnu : {event_type}")
    send_notification(message)
    return jsonify({"status": "ok"})

@app.route("/events", methods=["GET"])
def events():
    events = get_all_events()
    return jsonify(events)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
