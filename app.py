from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import tempfile
import mimetypes

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)
                if not filepath.endswith(".mp4"):
                    filepath = filepath.rsplit(".", 1)[0] + ".mp4"

                filename = os.path.basename(filepath)
                mimetype = mimetypes.guess_type(filepath)[0]

                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=filename,
                    mimetype=mimetype or "application/octet-stream"
                )

    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
