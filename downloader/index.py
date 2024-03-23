from flask import Flask, request, jsonify, render_template_string
from pytube import YouTube
import os

app = Flask(__name__)

def download_youtube_video(video_link, save_path):
    try:
        yt = YouTube(video_link)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
        return yt.thumbnail_url
    except Exception as e:
        print('An error occurred:', e)
        return None

def download_youtube_audio(video_link, save_path):
    try:
        yt = YouTube(video_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
        return True
    except Exception as e:
        print('An error occurred:', e)
        return False

@app.route('/')
def index():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Downloader</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            .container {
                text-align: center;
            }
            input[type="text"] {
                padding: 8px;
                margin-right: 8px;
            }
            button {
                padding: 8px 16px;
                cursor: pointer;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 4px;
            }
            button:hover {
                background-color: #0056b3;
            }
            .loading {
                display: none;
            }
            img {
                margin-top: 10px;
                max-width: 200px;
                height: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Video Downloader</h1>
            <input type="text" id="videoLink" placeholder="Enter video link">
            <button id="downloadBtn">Download</button>
            <button id="downloadAudioBtn">Download Audio</button>
            <div class="loading" id="loadingIndicator">Downloading...</div>
            <img id="thumbnail" src="" alt="Video Thumbnail">
        </div>

        <script>
            document.getElementById('downloadBtn').addEventListener('click', function() {
                var videoLink = document.getElementById('videoLink').value;
                if (videoLink.trim() === '') {
                    alert('Please enter a video link.');
                    return;
                }

                // Disable the download button and show loading indicator
                document.getElementById('downloadBtn').disabled = true;
                document.getElementById('loadingIndicator').style.display = 'block';

                // Send the video link to the backend for processing
                fetch('/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ videoLink: videoLink }),
                })
                .then(response => {
                    if (response.ok) {
                        alert('Video download initiated.');
                    } else {
                        alert('Failed to initiate video download.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while initiating video download.');
                })
                .finally(() => {
                    // Re-enable the download button and hide loading indicator
                    document.getElementById('downloadBtn').disabled = false;
                    document.getElementById('loadingIndicator').style.display = 'none';
                });
            });

            document.getElementById('downloadAudioBtn').addEventListener('click', function() {
                var videoLink = document.getElementById('videoLink').value;
                if (videoLink.trim() === '') {
                    alert('Please enter a video link.');
                    return;
                }

                // Send the video link to the backend for audio processing
                fetch('/download/audio', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ videoLink: videoLink }),
                })
                .then(response => {
                    if (response.ok) {
                        alert('Audio download initiated.');
                    } else {
                        alert('Failed to initiate audio download.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while initiating audio download.');
                });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code)

@app.route('/download', methods=['POST'])
def handle_download():
    data = request.get_json()
    video_link = data.get('videoLink')

    if not video_link:
        return jsonify({'error': 'Video link not provided'}), 400

    save_path = 'downloaded_video.mp4'  # Change this to your desired save path

    thumbnail_url = download_youtube_video(video_link, save_path)
    if thumbnail_url:
        return jsonify({'message': 'Video downloaded successfully', 'thumbnailUrl': thumbnail_url}), 200
    else:
        return jsonify({'error': 'Failed to download video'}), 500


@app.route('/download/audio', methods=['POST'])
def handle_audio_download():
    data = request.get_json()
    video_link = data.get('videoLink')

    if not video_link:
        return jsonify({'error': 'Video link not provided'}), 400

    save_path = 'downloaded_audio.mp3'  # Change this to your desired save path

    if download_youtube_audio(video_link, save_path):
        return jsonify({'message': 'Audio downloaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to download audio'}), 500


if __name__ == "__main__":
    app.run(debug=True)