from app.app import app as application
import os
import logging

gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    application.run(
        host=os.environ.get('FLASK_RUN_HOST', None),
        port=os.environ.get('FLASK_RUN_PORT', None),
        debug=os.environ.get('FLASK_RUN_DEBUG', None)
    )
