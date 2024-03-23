from flask import Flask, request, jsonify, render_template
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
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def handle_download():
    data = request.get_json()
    video_link = data.get('videoLink')

    if not video_link:
        return jsonify({'error': 'Video link not provided'}), 400

    save_path =('downloaded_video.mp4')  # Change this to your desired save path

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
