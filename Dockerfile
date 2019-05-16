FROM neosapience/audio-convert:base

COPY . .

EXPOSE 80
ENTRYPOINT ["/opt/audio-convert/docker-entrypoint.sh"]
CMD ["gunicorn"]
