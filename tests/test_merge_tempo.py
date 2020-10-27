from app.app import app
from unittest import TestCase
from io import BytesIO
import json
import tarfile
import wave
from mutagen.mp3 import MP3


class Test(TestCase):
    def _load_data(self, tempo):
        json_data = json.dumps({
            'meta_list': [
                ('wav_file_1', 0.5),
                ('wav_file_2', 1.5)
            ],
            'tempo': tempo
        })

        with open('./tests/assets/test.wav', 'rb') as f:
            buffer = BytesIO(f.read())
        buffer2 = BytesIO(buffer.read())
        buffer.seek(0, 2)
        audio_size = buffer.tell()
        buffer.seek(0)

        return {
            'json_data': json_data,
            'wav_file_1': (buffer, 'audio1.wav'),
            'wav_file_2': (buffer2, 'audio2.wav'),
        } 

    def test_merge_out_mp3_tempo(self):
        cli = app.test_client()

        data = self._load_data(tempo=1.0)
        r = cli.post('/merge?out=mp3', content_type='multipart/form-data', data=data, buffered=True)
        assert 200 == r.status_code
        len1 = MP3(BytesIO(r.data)).info.length
        # assert b'ID3' == r.data[:3]

        data = self._load_data(tempo=1.3)
        r = cli.post('/merge?out=mp3', content_type='multipart/form-data', data=data, buffered=True)
        assert 200 == r.status_code
        # assert b'ID3' == r.data[:3]
        len2 = MP3(BytesIO(r.data)).info.length
        assert len1 > len2 * 1.25
