from flask import Flask, request, render_template, send_from_directory
import yt_dlp
import os
import imageio_ffmpeg as iio_ffmpeg

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# Make sure downloads folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('youtube_url').strip()
        # get ffmpeg executable supplied by imageio-ffmpeg
        ffmpeg_path = iio_ffmpeg.get_ffmpeg_exe()  # returns full path to ffmpeg executable

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # point yt-dlp to the ffmpeg binary
            'ffmpeg_location': ffmpeg_path,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = f"{info['title']}.mp3"
            return f"Downloaded successfully! File saved as: {filename}"
        except Exception as e:
            return f"Error downloading audio: {e}"

    return render_template('index.html')  # HTML form for URL input

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
