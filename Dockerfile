FROM neosapience/audio-convert:base

COPY . .

HEALTHCHECK --interval=30s --timeout=2s --start-period=10s \
  CMD curl -f http://localhost/health || exit 1

RUN pip install sox

EXPOSE 80
ENTRYPOINT ["/opt/audio-convert/docker-entrypoint.sh"]
CMD ["gunicorn"]
