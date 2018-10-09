from flask import Flask
from flask import jsonify, request, send_file
from pydub import AudioSegment
from . import file

import os

app = Flask(__name__)


@app.route("/")
def version():
    return jsonify({
        'version': '0.0.2'
    })


@app.route("/wav_to_ogg", methods=['POST'])
def wav_to_ogg():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    
    wav_file = request.files['wav']
    with file.make_tempfile(prefix='wav_') as wav_path:
        wav_file.save(wav_path)
        audio = AudioSegment.from_wav(wav_path)
        
        with file.make_tempfile(prefix='ogg_') as ogg_path:
            r = audio.export(ogg_path, format="ogg", codec="libopus")
            if not r:
                abort(400, description='failed wave to ogg opus')
        
            return send_file(
                ogg_path, 
                as_attachment=True,
                attachment_filename=f'{os.path.basename(ogg_path)}.ogg',
                mimetype='audio/ogg')


@app.route("/wav_to_mp3", methods=['POST'])
def wav_to_mp3():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    
    wav_file = request.files['wav']
    with file.make_tempfile(prefix='wav_') as wav_path:
        wav_file.save(wav_path)
        audio = AudioSegment.from_wav(wav_path)
        with file.make_tempfile(prefix='mp3_') as mp3_path:
            r = audio.export(mp3_path, format="mp3")
            if not r:
                abort(400, description='failed wave to mp3')

            return send_file(
                mp3_path, 
                as_attachment=True,
                attachment_filename=f'{os.path.basename(mp3_path)}.mp3',
                mimetype='audio/mp3')
