from flask import Flask, request, render_template_string, Response
import requests
import re

app = Flask(__name__)

def download_video(url):
    try:
        response = requests.get(url, stream=True)
        return response, None
    except Exception as e:
        return None, f"Error downloading video: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        url = request.form['url']
        if 'instagram.com/reel/' in url or 'youtube.com/' in url or 'youtu.be/' in url:
            response, error = download_video(url)
            if response and response.status_code == 200:
                return Response(
                    response.iter_content(chunk_size=1024),
                    headers={
                        'Content-Disposition': 'attachment; filename=video.mp4',
                        'Content-Type': 'video/mp4',
                    }
                )
            else:
                message = error if error else "Error downloading video."
        else:
            message = "Invalid URL. Please enter a valid Instagram reel or YouTube video URL."
    
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>VideoPaze.com - Instagram and YouTube Video Downloader</title>
            <link href="https://fonts.googleapis.com/css2?family=Homemade+Apple&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Shadows+Into+Light&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">                      
            <style>
              body {
                font-family: "Playwrite GB J", cursive;
                background-color: #f8f9fa;
                background-size: cover;                  
                margin: 0;
                padding: 0;
                background-image: url('https://www.transparenttextures.com/patterns/exclusive-paper.png');
              }
              .container {
                width: 80%;
                margin: 50px auto;
                background: rgba(255, 255, 255, 0);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0);
              }
              h1 {
                font-family: "Playwrite GB J", cursive;
                font-size: 2.5em;
                text-align: center;
                margin-bottom: 0px;
                cursor: pointer;
              }
              h2 {
                font-family: "Playwrite GB J", cursive;                  
                font-size: 2em;
                font-weight: lighter;                  
                text-align: center;
                margin-bottom: 5px;
                cursor: pointer;
              }
              p {
               font-family: "Playwrite GB J", cursive;
               font-style: normal;                                    
               font-size: 1.2em;
               text-align: center;
               margin-bottom: 20px;
              }
              form {
                display: flex;
                flex-direction: column;
              }
              label {
                margin-bottom: 10px;
                font-size: 1.2em;
              }
              input[type="text"] {
                padding: 10px;
                font-size: 1em;
                border: 2px solid #000000;
                background-color: #c3e6cb00;
                border-radius: 5px;
                margin-bottom: 20px;
              }
              button {
                padding: 10px;
                font-size: 1.2em;
                border: 2px solid #000;
                border-radius: 5px;
                background: #03f2a257;
                cursor: pointer;
              }
              button:hover {
                background: #f9020263;
              }
              .social-icons {
                  text-align: center;
                  margin-top: 20px;
              }
              .social-icons i {
                  font-size: 2em;
                  margin: 0 10px;
                  cursor: pointer;
              }
              .social-icons i:hover {
                  color: #007bff;
              }
              h1:hover {
                 color: #007bff;
              }
              h2:hover {
                  color: #ff0000;
              }
            </style>
          </head>
          <body>
            <header>
                <div class="logo">
                     <h1>VideoPaze.com</h1> 
                </div>
            </header>
            <div class="container">
              <h2>Video Downloader</h2>
              <p>[Download Instagram and YouTube Videos]</p>
              <form method="post">
                  <label for="url">Video URL</label>
                  <input type="text" class="form-control" id="url" name="url" placeholder="Enter Instagram reel or YouTube video URL">
                  <button type="submit" class="btn btn-primary">Download</button>
              </form>
              <div class="social-icons">
                   <i class="fab fa-youtube"></i>
                   <i class="fab fa-instagram"></i>
              </div>
              <p>{{ message }}</p>
            </div>
          </body>
        </html>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True)
