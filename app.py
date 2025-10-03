from flask import Flask, render_template, request, send_file
import os
from pytube import YouTube

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        # handle conversion later
        return f"Got link: {youtube_url}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
