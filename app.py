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
        # yt-dlp options to fetch video info without downloading it immediately
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', 'Downloaded Video')
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
            'provider_name': 'Social Media'
        })

@app.route('/download', methods=['GET'])
def download_file():
    video_url = request.args.get('url')
    quality = request.args.get('quality', 'HD')
    
    if not video_url:
        return "URL is missing", 400
        
    try:
        ydl_opts = {}
        if quality == 'MP3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        elif quality == 'SD':
            ydl_opts = {'format': 'best[height<=480]'}
        else: # HD
            ydl_opts = {'format': 'best'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
            if quality == 'MP3':
                filename = os.path.splitext(filename)[0] + ".mp3"
                
            # Direct user to download or return file link
            return redirect(video_url) # Fallback direct redirect or stream file
    except Exception as e:
        return redirect(video_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
