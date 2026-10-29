import os
import requests
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import musicLibrary

load_dotenv()

app = Flask(__name__, template_folder="templates")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def ai_process(command):
    if not OPENAI_API_KEY:
        return "OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable in your deployment dashboard."
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are NOVA, a smart virtual assistant skilled in explaining complex programming contents with creative flares. Give short, concise responses please."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_command():
    data = request.get_json() or {}
    c = data.get("command", "").strip()
    if not c:
        return jsonify({"reply": "I didn't catch that. Please speak again.", "url": None})

    c_lower = c.lower()
    url = None
    reply = ""

    if "open google" in c_lower:
        url = "https://www.google.com"
        reply = "Opening Google"
    elif "open facebook" in c_lower:
        url = "https://www.facebook.com"
        reply = "Opening Facebook"
    elif "open youtube" in c_lower:
        url = "https://www.youtube.com"
        reply = "Opening YouTube"
    elif "open github" in c_lower:
        url = "https://github.com/JawadkhanHakim"
        reply = "Opening GitHub"
    elif "open linkedin" in c_lower:
        url = "https://www.linkedin.com/in/jawad-khan-hakim/"
        reply = "Opening LinkedIn"
    elif "open spotify" in c_lower:
        url = "https://open.spotify.com/user/31unbnmi7deloctfum2fpnbvpvnm?si=2ab40eea8a1e4ef7"
        reply = "Opening Spotify"
    elif c_lower.startswith("play "):
        parts = c_lower.split(" ", 1)
        song = parts[1].strip() if len(parts) > 1 else ""
        link = musicLibrary.music.get(song)
        if link:
            reply = f"Playing {song}"
            url = link
        else:
            reply = f"Sorry, I don't have {song} in my playlist"
    elif "news" in c_lower:
        if not NEWS_API_KEY:
            reply = "News API key is not configured."
        else:
            try:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
                if r.status_code == 200:
                    articles = r.json().get('articles', [])
                    if articles:
                        top_headlines = [a['title'] for a in articles[:3] if 'title' in a]
                        reply = "Here are the top headlines: " + ". ".join(top_headlines)
                    else:
                        reply = "No current news headlines found."
                else:
                    reply = "Unable to fetch news at the moment."
            except Exception as e:
                reply = f"Error fetching news: {str(e)}"
    else:
        reply = ai_process(c)

    return jsonify({"reply": reply, "url": url, "command": c})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
