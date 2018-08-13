import tempfile
import os


class make_tempfile:
    fd = None
    path = None
    delete = True

    def __enter__(self, prefix='', delete=True):
        self.delete = delete
        self.fd, self.path = tempfile.mkstemp(prefix=prefix)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            os.close(self.fd)
            if self.delete:
              os.remove(self.path)
