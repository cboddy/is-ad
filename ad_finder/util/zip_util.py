import zipfile
import contextlib
import logging


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
        n_elements = len(z_file.namelist())
        logging.info('{} has {} entries.'.format(path, n_elements))
        with z_file.open(name) as f:
            yield f


def zip_open_all(path):
    count = 0
    with zipfile.ZipFile(path, 'r') as z_file:
        namelist = z_file.namelist()
        for name in namelist:
            if count % 1000 == 0:
                logging.info('{} completed {:.3f}.'.format(path, float(count) / len(namelist)))
            count += 1
            with z_file.open(name) as f:
                yield (name, f)


def get_namelist(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z_file:
        return z_file.namelist()
