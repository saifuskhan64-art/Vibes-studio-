from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Vibes Studio Backend is Running! 🚀"

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL missing"}), 400

    # Yeh settings YouTube ke block ko bypass karne mein madad karti hain
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        # YouTube ke liye Android client use karein (block bypass)
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': ['webpage', 'configs'],
            }
        },
    }

    # Agar aap cookies file use karna chahte hain (recommended)
    # cookies_path = '/app/cookies.txt' # Railway par is path par upload karein
    # if os.path.exists(cookies_path):
    #     ydl_opts['cookiefile'] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            video_link = info.get('url')
            if not video_link and 'formats' in info:
                for f in info['formats']:
                    if f.get('ext') == 'mp4' and f.get('vcodec') != 'none':
                        video_link = f['url']
                        break
            if not video_link:
                 video_link = info.get('formats')[-1].get('url')

            return jsonify({
                "title": info.get('title', 'Video Detected'),
                "thumbnail": info.get('thumbnail', ''),
                "video": video_link,
                "audio": video_link 
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
