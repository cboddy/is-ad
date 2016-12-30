import os.path
from itertools import chain
from ad_finder.parse.classification import parse_classifications
from ad_finder.util.zip_util import (
    zip_open_all,
    get_namelist
)


class PipelineInput(object):

    def __init__(self,
                 doc_classifications_zip_path,
                 doc_zip_paths,
                 test_fraction=0.1,
                 max_doc_count=-1):
        """
        Parameters
        ----------
        doc_classifications_zip_path: `str`
            Path to zip-file containing doc classifications.
        doc_zip_paths: `iter[str]`
            Path to zip-file containing docs.
        test_fraction: `float`
            Fraction of input to use as test, 1-test_fraction used to train.
        """
        if not 0 < test_fraction < 1:
            raise ValueError('Invalid test fraction {:.3f}'.format(test_fraction))
        self.n_skip = int(1. / test_fraction) - 1
        self.doc_zip_paths = doc_zip_paths
        self.classification_dict = parse_classifications(doc_classifications_zip_path)
        self.max_doc_count = max_doc_count

    def train_docs(self):
        return self._doc_iter(False)

    def test_docs(self):
        return self._doc_iter(True)

    def train_doc_categories(self):
        return list(self._category_iter(False))

    def test_doc_categories(self):
        return list(self._category_iter(True))

    def _do_skip(self, name):
        return not name in self.classification_dict

    def _doc_iter(self, skip_train):
        count = 0
        doc_iterables = [zip_open_all(path) for path in self.doc_zip_paths]
        for name, f_handle in chain(*doc_iterables):
            last_name = os.path.basename(name)
            if len(last_name) == 0:
                continue
            if not self._do_skip(last_name):
                count += 1
                if self.max_doc_count != -1 and self.max_doc_count < count:
                    break
                if not skip_train ^ (count % self.n_skip):
                    continue

                lines = f_handle.readlines()
                yield ''.join(lines)

    def _category_iter(self, skip_train):
        count = 0
        doc_namelists = [get_namelist(path) for path in self.doc_zip_paths]
        for name in chain(*doc_namelists):
            last_name = os.path.basename(name)
            if len(last_name) == 0:
                continue
            if not self._do_skip(last_name):
                count += 1
                if self.max_doc_count != -1 and self.max_doc_count < count:
                    break
                if not skip_train ^ (count % self.n_skip):
                    continue
                if not last_name in self.classification_dict:
                    pass
                yield int(self.classification_dict[last_name])
