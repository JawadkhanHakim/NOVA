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
