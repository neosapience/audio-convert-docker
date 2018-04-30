from flask import Flask
from flask import jsonify, request, send_file

import soundfile as sf
import io
import os

app = Flask(__name__)


@app.route("/")
def version():
    return jsonify({
        'version': '0.0.1'
    })


@app.route("/wav_to_ogg", methods=['POST'])
def wav_to_ogg():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    wav_file = request.files['wav']
    filename = wav_file.filename
    wav_data = wav_file.read()

    filename = os.path.basename(filename)
    new_filename, _ = os.path.splitext(filename)
    new_filename = f'{new_filename}.ogg'

    data, samplerate = sf.read(io.BytesIO(wav_data))
    buffer = io.BytesIO()
    sf.write(buffer, data, samplerate, format='ogg')
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     attachment_filename=new_filename,
                     mimetype='audio/ogg')

