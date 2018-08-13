# =============================================================================
# Build
# =============================================================================
FROM python:3.6-alpine as build
RUN apk update && apk add build-base
RUN pip install greenlet

WORKDIR /tmp/site-packages
RUN cp -r /usr/local/lib/python3.6/site-packages/greenlet-0.4.14.dist-info .
RUN cp -r /usr/local/lib/python3.6/site-packages/greenlet.*.so .


# =============================================================================
# Image
# =============================================================================
FROM python:3.6-alpine

RUN apk update && apk add ffmpeg \
  && rm -f /var/cache/apk/*

COPY --from=build /tmp/site-packages /usr/local/lib/python3.6/site-packages

WORKDIR /opt/audio-convert
COPY requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

COPY . .
EXPOSE 80
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn"]