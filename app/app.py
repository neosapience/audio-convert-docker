from . import file
from flask import Flask
from flask import jsonify, request, send_file, abort, make_response
from pydub import AudioSegment
import os
from io import BytesIO
import shortuuid
import json

app = Flask(__name__)

_MP3_BITRATE = os.environ.get('MP3_BITRATE', '32k')
_MP3_SAMPLING_RATE = os.environ.get('MP3_SAMPLING_RATE', '22050')
_MP3_SAMPLE_FMT = os.environ.get('_MP3_SAMPLE_FMT', 's16')
_content_type_map = {
    'wav': 'audio/wav',
    'ogg': 'audio/ogg',
    'mp3': 'audio/mpeg',
    'default': 'application/octet-stream'
}

@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'error': error.description}), 400)


@app.route("/")
def version():
    return jsonify({
        'version': 'latest'
    })


@app.route("/health")
def health():
    return jsonify({
        'health': 'ok'
    })


@app.route("/wav_to_ogg", methods=['POST'])
def wav_to_ogg():
    if 'wav' not in request.files:
        abort(400, description='file is not attached')
    data = request.form.to_dict()
    
    wav_file = request.files['wav']
    wav_data = BytesIO(wav_file.read())
    audio = AudioSegment.from_wav(wav_data)


    if data.get('silence', False):
        silence_ms = int(float(data.get('silence')) * 1000)
        audio += AudioSegment.silent(duration=silence_ms)

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

    if data.get('silence', False):
        silence_ms = int(float(data.get('silence')) * 1000)
        audio += AudioSegment.silent(duration=silence_ms)

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


@app.route("/merge", methods=['POST'])
def merge():
    ext = request.args.get('out', 'wav')
    if ext not in ('wav', 'mp3', 'ogg'):
        abort(400, description='only support wav or mp3')
    
    data = request.form.to_dict()
    json_data = json.loads(data['json_data'])

    if len(json_data['meta_list']) != len(request.files):
        abort(400, description='mismatch audio files and silence data')

    combined = AudioSegment.empty()
    for meta in json_data['meta_list']:
        key, silence = meta
        audio_file = request.files.get(key)
        audio_data = BytesIO(audio_file.read())
        silence_ms = int(silence * 1000)
        combined += AudioSegment.from_wav(audio_data)
        combined += AudioSegment.silent(duration=silence_ms)

    output_data = BytesIO()
    if ext == 'wav':
        r = combined.export(output_data, format="wav")
    elif ext == 'mp3':
        mp3_params = _mp3_parameters(json_data)
        r = combined.export(output_data, format="mp3", **mp3_params)
    elif ext == 'ogg':
        r = combined.export(output_data, format="ogg", codec="libopus")

    if not r:
        abort(400, description='failed wave to mp3')

    output_data.seek(0)
    return send_file(
        output_data,
        as_attachment=True,
        attachment_filename=f'audio.{ext}',
        mimetype=_content_type_map[ext])


def _mp3_parameters(data):
    ret = dict()
    parameters = []
    
    ret['bitrate'] = data.get('bitrate', _MP3_BITRATE)
    parameters += ['-ar', data.get('sampling_rate', _MP3_SAMPLING_RATE)]
    parameters += ['-sample_fmt', data.get('sample_fmt', _MP3_SAMPLE_FMT)]
    
    if parameters:
        ret['parameters'] = parameters
    return ret
