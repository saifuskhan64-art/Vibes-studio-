from flask import Flask, render_template, request, jsonify, redirect
import os
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', 'Vibes Studio Video')
            thumbnail = info_dict.get('thumbnail', '')
            uploader = info_dict.get('uploader', 'Social Media')
            
            return jsonify({
                'status': 'success',
                'title': title,
                'thumbnail': thumbnail,
                'provider_name': uploader
            })
    except Exception as e:
        return jsonify({
            'status': 'success',
            'title': 'Video Ready for Download',
            'thumbnail': '',
            'provider_name': 'Vibes Studio'
        })

@app.route('/download', methods=['GET'])
def download_file():
    video_url = request.args.get('url')
    if not video_url:
        return "URL is missing", 400
        
    try:
        # Direct clean extraction for quick user download link
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            direct_url = info_dict.get('url', video_url)
            return redirect(direct_url)
    except Exception as e:
        return redirect(video_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
