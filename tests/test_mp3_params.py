from app.app import app
from unittest import TestCase


class Test(TestCase):
    def test_wav_to_mp3_bitrate(self):
        cli = app.test_client()
        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_mp3', content_type='multipart/form-data', data={
                'wav': f
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            default_bitrate_data_size = len(r.data)

        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_mp3', content_type='multipart/form-data', data={
                'wav': f,
                'bitrate': '192k'
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            higher_bitrate_data_size = len(r.data)

        self.assertTrue(default_bitrate_data_size < higher_bitrate_data_size)

    def test_wav_to_mp3_sampling_rate(self):
        cli = app.test_client()
        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_mp3', content_type='multipart/form-data', data={
                'wav': f,
                'bitrate': '16k'
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            default_bitrate_data_size = len(r.data)

        with open('./tests/assets/test.wav', 'rb') as f:
            r = cli.post('/wav_to_mp3', content_type='multipart/form-data', data={
                'wav': f,
                'bitrate': '16k',
                'sampling_rate': '24000',
                'sample_fmt': 'flt'
            }, buffered=True)

            self.assertEqual(200, r.status_code)
            higher_bitrate_data_size = len(r.data)

        self.assertTrue(default_bitrate_data_size != higher_bitrate_data_size)
