# =============================================================================
# Build
# =============================================================================
FROM python:3.6-alpine3.8 as build
RUN apk update && apk add build-base
RUN pip install gevent

WORKDIR /tmp/site-packages
RUN cp -r /usr/local/lib/python3.6/site-packages/gevent .
RUN cp -r /usr/local/lib/python3.6/site-packages/greenlet.*.so .
RUN cp -r /usr/local/lib/python3.6/site-packages/gevent-*dist-info .
RUN cp -r /usr/local/lib/python3.6/site-packages/greenlet-*dist-info .


# =============================================================================
# Image
# =============================================================================
FROM python:3.6-alpine3.8

RUN apk update && apk add ffmpeg \
  && rm -f /var/cache/apk/*

COPY --from=build /tmp/site-packages /usr/local/lib/python3.6/site-packages

WORKDIR /opt/audio-convert
COPY requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

ENV PYTHONPATH=/opt/audio-convert:$PYTHONPATH

COPY . .
EXPOSE 80
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn"]