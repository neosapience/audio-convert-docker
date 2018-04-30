FROM python:3.6-alpine

RUN apk update && apk add --update \ 
  build-base libffi-dev libsndfile-dev \
  && rm -f /var/cache/apk/* \
  && \
  pip install \
    pysoundfile \
	numpy

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["gunicorn", \
     "wsgi", \
     "--name=audio-convert",\
     "--bind=0.0.0.0:5000",\
     "--log-level=debug",\
     "--timeout=1800"]
