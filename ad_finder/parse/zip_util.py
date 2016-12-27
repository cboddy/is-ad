import zipfile
import contextlib


@contextlib.contextmanager
def zip_open(path, name):
    """
    Read a zip-file entry.

    :param path: `str`
        Path to zip file.
    :param name: `str
        entry-name of zip-file entry.
    :return:
    `generator`
        for lines of name.
    """
    with zipfile.ZipFile(path, 'r') as z_file:
        with z_file.open(name) as f:
            yield f
