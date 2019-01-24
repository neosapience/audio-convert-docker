from app.app import app
from unittest import TestCase


def get_version_from_makefile():
    found = ''
    with open('Makefile') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('tag'):
                found = line
                break
    version = found.split(':=')[1]
    return version.strip()


class Test(TestCase):
    def test_version(self):
        cli = app.test_client()
        r = cli.get('/')
        self.assertEqual(200, r.status_code)
        expected = get_version_from_makefile()
        self.assertEqual(expected, r.get_json()['version'])

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
