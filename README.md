# Audio Convert wav to ogg

## run
```
make build
make run
```

## api
```bash
# simple ogg
curl -X POST localhost:32769/wav_to_ogg\
  -o out.ogg \
  -F "wav=@test/test.wav"

# full option for ogg
curl -X POST localhost:32769/wav_to_ogg\
  -o out.ogg \
  -F "wav=@test/test.wav" \
  -F "silence=5"

# simple mp3
curl -X POST localhost:32769/wav_to_mp3\
  -o out.mp3 \
  -F "wav=@test/test.wav"

# full option for mp3
curl -X POST localhost:32769/wav_to_mp3\
  -o out.mp3 \
  -F "wav=@test/test.wav" \
  -F "silence=5" \
  -F "bitrate=320k" \
  -F "sampling_rate=44100"

```
