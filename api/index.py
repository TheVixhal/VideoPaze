from flask import Flask, request, render_template_string, Response
import requests
from pytube import YouTube
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
  try:
    if 'youtube.com' in url or 'youtu.be' in url:
      # Try using pytube first
      try:
        yt = YouTube(url)
        video_url = yt.streams.filter(progressive=True, file_extension='mp4').first().url
        return video_url, None
      except Exception as e:
        # Fallback to yt-dlp if pytube fails
        try:
          with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url')
            return video_url, None
        except Exception as e:
          return None, f"Error extracting video URL with yt-dlp: {e}"
    elif 'instagram.com/reel/' in url:
      # Instagram extraction is not supported with pytube or yt-dlp
      return None, "Instagram video extraction is not supported."
    else:
      return None, "Unsupported URL format."
  except Exception as e:
    return None, f"Error extracting video URL: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
  message = ""
  if request.method == 'POST':
    url = request.form.get('url')
    if url:
      video_url, error = get_video_info(url)
      if video_url:
        try:
          response = requests.get(video_url, stream=True)
          if response.status_code == 200:
            return Response(
              response.iter_content(chunk_size=1024),
              headers={
                'Content-Disposition': 'attachment; filename=video.mp4',
                'Content-Type': 'video/mp4',
              }
            )
          else:
            message = "Error downloading video."
        except Exception as e:
          message = f"Error fetching video: {e}"
      else:
        message = error if error else "Error extracting video URL."
    else:
      message = "Please enter a valid URL."

  return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>VideoPaze.com - Instagram and YouTube Video Downloader</title>
      <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">                      
      <style>
        body {
        font-family: 'Montserrat', sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-image: url('https://www.transparenttextures.com/patterns/exclusive-paper.png');
        }
        .container {
        width: 90%;
        max-width: 600px;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        }
        h1 {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5em;
        margin-bottom: 10px;
        }
        h2 {
        font-family: 'Montserrat', sans-serif;
        font-size: 2em;
        margin-bottom: 20px;
        }
        p {
        font-size: 1.2em;
        margin-bottom: 20px;
        }
        form {
        display: flex;
        flex-direction: column;
        align-items: center;
        }
        label {
        margin-bottom: 10px;
        font-size: 1.2em;
        }
        input[type="text"] {
        padding: 10px;
        font-size: 1em;
        border: 2px solid #ccc;
        border-radius: 5px;
        margin-bottom: 20px;
        width: 100%;
        }
        button {
        padding: 10px 20px;
        font-size: 1.2em;
        border: none;
        border-radius: 5px;
        background: #007bff;
        color: #fff;
        cursor: pointer;
        transition: background 0.3s;
        }
        button:hover {
        background: #0056b3;
        }
        h1:hover, h2:hover, p:hover, label:hover, input[type="text"]:hover, button:hover {
                              color: red; }
        .social-icons {
        margin-top: 20px;
        }
        .social-icons i {
        font-size: 2em;
        margin: 0 10px;
        cursor: pointer;
        transition: color 0.3s;
        }
        .social-icons i:hover {
        color: #007bff;
        }
        .message {
        color: red;
        font-size: 1em;
        margin-top: 20px;
        }
      </style>
      </head>
      <body>
      <div class="container">
        <h1>Instagram video donloader</h1>
        <h2>Video Downloader</h2>
        <p>Download YouTube Videos</p>
        <form method="post">
          <label for="url">Video URL</label>
          <input type="text" id="url" name="url" placeholder="Enter Instagram reel or YouTube video URL">
          <button type="submit">Download</button>
        </form>
        <div class="social-icons">
          <i class="fab fa-youtube"></i>
          <i class="fab fa-instagram"></i>
        </div>
        <p class="message">{{ message }}</p>
      </div>
      </body>
    </html>
  ''', message=message)

if __name__ == '__main__':
  app.run(debug=True)
