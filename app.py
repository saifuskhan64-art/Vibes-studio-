from flask import Flask, render_template, request, jsonify

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
    return jsonify({'status': 'success', 'url': video_url})

if __name__ == '__main__':
    app.run(debug=True)
