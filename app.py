from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
from pytube.exceptions import *
from pathlib import Path
import os

app = Flask(__name__)

def get_info(url):
    yt = YouTube(url)
    error = ""
    message = ""
    try:
        video = yt.streams.get_highest_resolution()
        error = "false"
        message = ""
    except (AgeRestrictedError, 
            MaxRetriesExceeded, 
            HTMLParseError, 
            RegexMatchError, 
            VideoUnavailable, 
            LiveStreamError,
            VideoPrivate,
            RecordingUnavailable,
            MembersOnly,
            VideoRegionBlocked) as e:
        error = "true"
        message = str(e)
        message = message.replace(" is ", "~")
        arrMess = []
        arrMess = message.split("~")
        message = "Error: " + arrMess[1].capitalize()
    thumbnail = yt.thumbnail_url
    title = yt.title
    link = url
    
    return thumbnail, title, link, error, message

@app.route('/')
def home():
    state = "none"
    error = "false"
    return render_template("index.html", state=state, error=error)

@app.post("/find")
def find():
    link = request.form.get("link")
    thumbnail, title, link, error, message = get_info(link)
    state = "block"

    return render_template("index.html", thumbnail=thumbnail, title=title, link=link, error=error, message=message, state=state)

@app.route("/downloadMP4", methods=["GET","POST"])
def downloadVideo():
    youtubeUrl = request.form.get("url")
    url = YouTube(youtubeUrl)
    video = url.streams.get_highest_resolution()
    downloadFolder = str(os.path.join(Path.home(), "Downloads"))
    out_file = video.download(downloadFolder)
    base, ext = os.path.splitext(out_file) 
    base = base + " - MP4"
    new_file = base + '.mp4'
    os.rename(out_file, new_file)

    return redirect(url_for("home"))

@app.route("/downloadMP3", methods=["GET","POST"])
def convertVideo():
    youtubeUrl = request.form.get("url")
    url = YouTube(youtubeUrl)
    video = url.streams.get_highest_resolution()
    downloadFolder = str(os.path.join(Path.home(), "Downloads"))
    out_file = video.download(downloadFolder)
    base, ext = os.path.splitext(out_file)
    base = base + " - MP3"
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    return redirect(url_for("home"))
    
app.run(host="0.0.0.0", port=80, debug=True)