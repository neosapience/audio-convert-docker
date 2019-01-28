from app.app import app
from unittest import TestCase


class Test(TestCase):
    def test_version(self):
        cli = app.test_client()
        r = cli.get('/')
        self.assertEqual(200, r.status_code)
        self.assertEqual('latest', r.get_json()['version'])

    def test_health(self):
        cli = app.test_client()
        r = cli.get('/health')
        self.assertEqual(200, r.status_code)

    def test_wav_to_mp3(self):
        cli = app.test_client()
        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_mp3', content_type='multipart/form-data', data={
                'wav': f
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            self.assertEqual(b'ID3', r.data[:3])

    def test_wav_to_ogg(self):
        cli = app.test_client()
        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_ogg', content_type='multipart/form-data', data={
                'wav': f
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            self.assertEqual(b'OggS', r.data[:4])
