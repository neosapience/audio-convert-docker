from app.app import app
from unittest import TestCase
from io import BytesIO
import json


class Test(TestCase):
    def setUp(self):
        json_data = json.dumps({
            'silences': [
                0.5,
                1.5,
            ]
        })

        with open('./tests/assets/test.wav', 'rb') as f:
            buffer = BytesIO(f.read())
        
        buffer2 = BytesIO(buffer.read())
        buffer.seek(0)

        self.data = {
            'wav_files[]': [
                (buffer, 'audio1.wav'),
                (buffer2, 'audio2.wav')
            ],
            'json_data': json_data
        }

    def test_merge_out_mp4_unsupported(self):
        cli = app.test_client()
        r = cli.post('/merge?out=mp4', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(400, r.status_code)

    def test_merge_out_wav(self):
        cli = app.test_client()
        r = cli.post('/merge?out=wav', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(200, r.status_code)
        self.assertEqual(b'RIFF', r.data[:4])
        
        # with open('test.wav', 'wb') as f:
        #     f.write(r.data)

    def test_merge_out_mp3(self):
        cli = app.test_client()
        r = cli.post('/merge?out=mp3', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(200, r.status_code)
        self.assertEqual(b'ID3', r.data[:3])

    def test_merge_out_ogg(self):
        cli = app.test_client()
        r = cli.post('/merge?out=ogg', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(200, r.status_code)
        self.assertEqual(b'OggS', r.data[:4])
