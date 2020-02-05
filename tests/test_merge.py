from app.app import app
from unittest import TestCase
from io import BytesIO
import json
import tarfile
import wave


class Test(TestCase):
    def setUp(self):
        json_data = json.dumps({
            'meta_list': [
                ('wav_file_1', 0.5),
                ('wav_file_2', 1.5)
            ]
        })

        with open('./tests/assets/test.wav', 'rb') as f:
            buffer = BytesIO(f.read())
        
        buffer2 = BytesIO(buffer.read())
        buffer.seek(0, 2)
        audio_size = buffer.tell()
        buffer.seek(0)

        self.data = {
            'json_data': json_data,
            'wav_file_1': (buffer, 'audio1.wav'),
            'wav_file_2': (buffer2, 'audio2.wav'),
        }
        
        self.expected_lower_bound = audio_size + audio_size + int(1.5 * 32000)
        self.expected_upper_bound = self.expected_lower_bound + int(0.5 * 32000)

    def test_merge_out_mp4_unsupported(self):
        cli = app.test_client()
        r = cli.post('/merge?out=mp4', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(400, r.status_code)

    def test_merge_out_wav(self):
        cli = app.test_client()
        r = cli.post('/merge?out=wav', content_type='multipart/form-data', data=self.data, buffered=True)
        self.assertEqual(200, r.status_code)
        self.assertEqual(b'RIFF', r.data[:4])

        audio_size = len(r.data)
        assert self.expected_lower_bound <= audio_size
        assert self.expected_upper_bound >= audio_size

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
