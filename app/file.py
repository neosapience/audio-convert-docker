import tempfile
import os
import glob


class make_tempfile:
    fd = None
    path = None
    delete = True

    def __init__(self, prefix='', delete=True):
        self.prefix = prefix
        self.delete = delete

    def __enter__(self):
        self.fd, self.path = tempfile.mkstemp(prefix=self.prefix)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            os.close(self.fd)
            if self.delete:
                for f in glob.glob(self.path + "*"):
                    os.remove(f)
