from flask import Flask, request, jsonify, render_template
import datetime
import pytz
import requests
from iso3166 import countries

app = Flask(__name__)

# ----------------------------
# Agent 1: Greet by Name (with simple language detection)
# ----------------------------
@app.route("/api/agent1", methods=["POST"])
def agent1():
    data = request.json or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Please provide a name."}), 400

    # Detect Arabic letters
    if any('\u0600' <= ch <= '\u06FF' for ch in name):
        greeting = f"مرحبًا يا {name}!"
    else:
        greeting = f"Hey {name}!"

    return jsonify({"response": greeting})


# ----------------------------
# Agent 2: Weather & Time (No API key required)
# ----------------------------
@app.route("/api/agent2", methods=["POST"])
def agent2():
    data = request.json or {}
    country = data.get("country")
    if not country:
        return jsonify({"error": "Missing country"}), 400

    try:
        # Get weather from wttr.in (Free, no API key)
        weather_url = f"https://wttr.in/{country}?format=3"
        weather_resp = requests.get(weather_url)
        if weather_resp.status_code != 200:
            raise Exception("Weather API error")

        weather_text = weather_resp.text.strip()

        # Get time using country name → country code → timezone
        try:
            country_code = countries.get(country).alpha2  # e.g., France → FR
            tz = pytz.country_timezones[country_code][0]
            now = datetime.datetime.now(pytz.timezone(tz))
            time_text = now.strftime("Current time: %H:%M - %d %B %Y")
        except:
            time_text = "Time not available."

        return jsonify({"response": f"{weather_text}. {time_text}"})

    except Exception as e:
        return jsonify({"error": "Could not get data for that country."}), 500


# ----------------------------
# Routes to Pages
# ----------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/agent1")
def agent1_page():
    return render_template("agent1.html")

@app.route("/agent2")
def agent2_page():
    return render_template("agent2.html")


# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
