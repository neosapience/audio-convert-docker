# Audio Convert wav to ogg

## run
```
make build
make run
```

## api
```
curl -X POST localhost:32769/wav_to_ogg\
  -o out.ogg \
  -F "wav=@test/test.wav"

curl -X POST localhost:32769/wav_to_mp3\
  -o out.mp3 \
  -F "wav=@test/test.wav"
```
