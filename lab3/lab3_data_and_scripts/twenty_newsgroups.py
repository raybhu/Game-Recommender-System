from os import listdir
from os.path import isdir, join
import numpy as np
import numbers
import re


# the code is adopted from
# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/datasets/twenty_newsgroups.py


class Bunch(dict):
    """Container object for datasets

    Dictionary-like object that exposes its keys as attributes.

    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2
    >>> b.a = 3
    >>> b['a']
    3
    >>> b.c = 6
    >>> b['c']
    6

    """

    def __init__(self, **kwargs):
        super(Bunch, self).__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        pass


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance

    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)


def load_files(container_path, description=None, categories=None,
               load_content=True, shuffle=True, encoding=None,
               decode_error='strict', random_state=0):
    """Load text files with categories as subfolder names.
    Individual samples are assumed to be files stored a two levels folder
    structure such as the following:
        container_folder/
            category_1_folder/
                file_1.txt
                file_2.txt
                ...
                file_42.txt
            category_2_folder/
                file_43.txt
                file_44.txt
                ...
    The folder names are used as supervised signal label names. The individual
    file names are not important.
    This function does not try to extract features into a numpy array or scipy
    sparse matrix. In addition, if load_content is false it does not try to
    load the files in memory.
    To use text files in a scikit-learn classification or clustering algorithm,
    you will need to use the `sklearn.feature_extraction.text` module to build
    a feature extraction transformer that suits your problem.
    If you set load_content=True, you should also specify the encoding of the
    text using the 'encoding' parameter. For many modern text files, 'utf-8'
    will be the correct encoding. If you leave encoding equal to None, then the
    content will be made of bytes instead of Unicode, and you will not be able
    to use most functions in `sklearn.feature_extraction.text`.
    Similar feature extractors should be built for other kind of unstructured
    data input such as images, audio, video, ...
    Read more in the :ref:`User Guide <datasets>`.
    Parameters
    ----------
    container_path : string or unicode
        Path to the main folder holding one subfolder per category
    description : string or unicode, optional (default=None)
        A paragraph describing the characteristic of the dataset: its source,
        reference, etc.
    categories : A collection of strings or None, optional (default=None)
        If None (default), load all the categories. If not None, list of
        category names to load (other categories ignored).
    load_content : boolean, optional (default=True)
        Whether to load or not the content of the different files. If true a
        'data' attribute containing the text information is present in the data
        structure returned. If not, a filenames attribute gives the path to the
        files.
    shuffle : bool, optional (default=True)
        Whether or not to shuffle the data: might be important for models that
        make the assumption that the samples are independent and identically
        distributed (i.i.d.), such as stochastic gradient descent.
    encoding : string or None (default is None)
        If None, do not try to decode the content of the files (e.g. for images
        or other non-text content). If not None, encoding to use to decode text
        files to Unicode if load_content is True.
    decode_error : {'strict', 'ignore', 'replace'}, optional
        Instruction on what to do if a byte sequence is given to analyze that
        contains characters not of the given `encoding`. Passed as keyword
        argument 'errors' to bytes.decode.
    random_state : int, RandomState instance or None (default=0)
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are: either
        data, the raw text data to learn, or 'filenames', the files
        holding it, 'target', the classification labels (integer index),
        'target_names', the meaning of the labels, and 'DESCR', the full
        description of the dataset.
    """
    target = []
    target_names = []
    filenames = []

    folders = [f for f in sorted(listdir(container_path))
               if isdir(join(container_path, f))]

    if categories is not None:
        folders = [f for f in folders if f in categories]

    for label, folder in enumerate(folders):
        target_names.append(folder)
        folder_path = join(container_path, folder)
        documents = [join(folder_path, d)
                     for d in sorted(listdir(folder_path))]
        target.extend(len(documents) * [label])
        filenames.extend(documents)

    # convert to array for fancy indexing
    filenames = np.array(filenames)
    target = np.array(target)

    if shuffle:
        random_state = check_random_state(random_state)
        indices = np.arange(filenames.shape[0])
        random_state.shuffle(indices)
        filenames = filenames[indices]
        target = target[indices]

    if load_content:
        data = []
        for filename in filenames:
            with open(filename, 'rb') as f:
                data.append(f.read())
        if encoding is not None:
            data = [d.decode(encoding, decode_error) for d in data]
        return Bunch(data=data,
                     filenames=filenames,
                     target_names=target_names,
                     target=target,
                     DESCR=description)

    return Bunch(filenames=filenames,
                 target_names=target_names,
                 target=target,
                 DESCR=description)


def strip_newsgroup_header(text):
    """
    Given text in "news" format, strip the headers, by removing everything
    before the first blank line.
    """
    _before, _blankline, after = text.partition('\n\n')
    return after


_QUOTE_RE = re.compile(r'(writes in|writes:|wrote:|says:|said:'
                       r'|^In article|^Quoted from|^\||^>)')


def strip_newsgroup_quoting(text):
    """
    Given text in "news" format, strip lines beginning with the quote
    characters > or |, plus lines that often introduce a quoted section
    (for example, because they contain the string 'writes:'.)
    """
    good_lines = [line for line in text.split('\n')
                  if not _QUOTE_RE.search(line)]
    return '\n'.join(good_lines)


def strip_newsgroup_footer(text):
    """
    Given text in "news" format, attempt to remove a signature block.

    As a rough heuristic, we assume that signatures are set apart by either
    a blank line or a line made of hyphens, and that it is the last such line
    in the file (disregarding blank lines at the end).
    """
    lines = text.strip().split('\n')
    for line_num in range(len(lines) - 1, -1, -1):
        line = lines[line_num]
        if line.strip().strip('-') == '':
            break

    if line_num > 0:
        return '\n'.join(lines[:line_num])
    else:
        return text


TRAIN_FOLDER = '20news-bydate-train'
TEST_FOLDER = '20news-bydate-test'


# only this function is modified in this .py file
def load_20newsgroups(data_home, subset='train', categories=None,
                      shuffle=True, random_state=42,
                      remove=()):
    """Load the filenames and data from the 20 newsgroups dataset.

    Read more in the :ref:`User Guide <20newsgroups>`.

    Parameters
    ----------
    data_home :
        Specify a main folder holding one subfolder per category for the datasets.

    subset : 'train' or 'test', 'all', optional
        Select the dataset to load: 'train' for the training set, 'test'
        for the test set, 'all' for both, with shuffled ordering.

    categories : None or collection of string or unicode
        If None (default), load all the categories.
        If not None, list of category names to load (other categories
        ignored).

    shuffle : bool, optional
        Whether or not to shuffle the data: might be important for models that
        make the assumption that the samples are independent and identically
        distributed (i.i.d.), such as stochastic gradient descent.

    random_state : numpy random number generator or seed integer
        Used to shuffle the dataset.

    remove : tuple
        May contain any subset of ('headers', 'footers', 'quotes'). Each of
        these are kinds of text that will be detected and removed from the
        newsgroup posts, preventing classifiers from overfitting on
        metadata.

        'headers' removes newsgroup headers, 'footers' removes blocks at the
        ends of posts that look like signatures, and 'quotes' removes lines
        that appear to be quoting another post.

        'headers' follows an exact standard; the other filters are not always
        correct.
    """

    if not isdir(data_home):
        raise ValueError(
            "data_home can only be a folder, got '%s'" % subset)

    train_path = join(data_home, TRAIN_FOLDER)
    test_path = join(data_home, TEST_FOLDER)
    cache = dict(train=load_files(train_path, encoding='latin1'),
                 test=load_files(test_path, encoding='latin1'))

    # the following code remains unchanged
    if subset in ('train', 'test'):
        data = cache[subset]
    elif subset == 'all':
        data_lst = list()
        target = list()
        filenames = list()
        for subset in ('train', 'test'):
            data = cache[subset]
            data_lst.extend(data.data)
            target.extend(data.target)
            filenames.extend(data.filenames)

        data.data = data_lst
        data.target = np.array(target)
        data.filenames = np.array(filenames)
    else:
        raise ValueError(
            "subset can only be 'train', 'test' or 'all', got '%s'" % subset)

    data.description = 'the 20 newsgroups by date dataset'

    if 'headers' in remove:
        data.data = [strip_newsgroup_header(text) for text in data.data]
    if 'footers' in remove:
        data.data = [strip_newsgroup_footer(text) for text in data.data]
    if 'quotes' in remove:
        data.data = [strip_newsgroup_quoting(text) for text in data.data]

    if categories is not None:
        labels = [(data.target_names.index(cat), cat) for cat in categories]
        # Sort the categories to have the ordering of the labels
        labels.sort()
        labels, categories = zip(*labels)
        mask = np.in1d(data.target, labels)
        data.filenames = data.filenames[mask]
        data.target = data.target[mask]
        # searchsorted to have continuous labels
        data.target = np.searchsorted(labels, data.target)
        data.target_names = list(categories)
        # Use an object array to shuffle: avoids memory copy
        data_lst = np.array(data.data, dtype=object)
        data_lst = data_lst[mask]
        data.data = data_lst.tolist()

    if shuffle:
        random_state = check_random_state(random_state)
        indices = np.arange(data.target.shape[0])
        random_state.shuffle(indices)
        data.filenames = data.filenames[indices]
        data.target = data.target[indices]
        # Use an object array to shuffle: avoids memory copy
        data_lst = np.array(data.data, dtype=object)
        data_lst = data_lst[indices]
        data.data = data_lst.tolist()

    return data
