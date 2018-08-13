# Audio Convert wav to ogg

## run
```
make build
make run
```

## api
```
curl -X POST localhost/wav_to_ogg\
  -o out.ogg \
  -F "wav=@/your/wav-path.wav"
```
