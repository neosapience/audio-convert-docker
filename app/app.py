from . import file
from flask import Flask
from flask import jsonify, request, send_file, abort
from pydub import AudioSegment
import os
from io import BytesIO
import shortuuid

app = Flask(__name__)


@app.route("/")
def version():
    return jsonify({
        'version': '0.0.5'
    })


@app.route("/wav_to_ogg", methods=['POST'])
def wav_to_ogg():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    
    wav_file = request.files['wav']
    wav_data = BytesIO(wav_file.read())
    audio = AudioSegment.from_wav(wav_data)

    output_data = BytesIO()
    r = audio.export(output_data, format="ogg", codec="libopus")
    if not r:
        abort(400, description='failed wave to ogg opus')

    name = shortuuid.ShortUUID().random(length=8)
    output_data.seek(0)
    return send_file(
        output_data,
        as_attachment=True,
        attachment_filename=f'{name}.ogg',
        mimetype='audio/ogg')


@app.route("/wav_to_mp3", methods=['POST'])
def wav_to_mp3():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    data = request.form.to_dict()
    
    wav_file = request.files['wav']
    wav_data = BytesIO(wav_file.read())
    audio = AudioSegment.from_wav(wav_data)

    mp3_params = _mp3_parameters(data)
    output_data = BytesIO()
    r = audio.export(output_data, format="mp3", **mp3_params)
    if not r:
        abort(400, description='failed wave to mp3')

    name = shortuuid.ShortUUID().random(length=8)
    output_data.seek(0)
    return send_file(
        output_data,
        as_attachment=True,
        attachment_filename=f'{name}.mp3',
        mimetype='audio/mpeg')


def _mp3_parameters(data):
    ret = dict()
    parameters = []
    
    if 'bitrate' in data:
        ret['bitrate'] = data['bitrate']

    if 'sampling_rate' in data:
        parameters += ['-ar', data["sampling_rate"]]
    
    if parameters:
        ret['parameters'] = parameters
    return ret
