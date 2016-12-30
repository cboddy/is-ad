import os.path

from ad_finder.util.zip_util import zip_open


def parse_classifications(zip_path):
    """Parse classification zip file.

    Parameters
    ----------
    zip_path: str
        Path to zip file.

    Returns
    -------
    dict[str,bool]
        entry-name: is_ad
    """
    if not zip_path.endswith('.zip'):
        raise ValueError('{} is not a zip-file.'.format(zip_path))
    name = os.path.basename(zip_path).replace('.zip', '')
    with zip_open(zip_path, name) as z_open:
        return get_classifications(z_open)


def get_classifications(lines):
    """
    Parameters
    ----------
    lines: `list[str]`
        `entry, [0,1]'

    Returns
    -------
    dict[str, bool]
        A dictionary of entry-names  where the value is True iff it is a native-ad.
    """
    header = next(lines)  #skip header

    parsed = (_parse(line) for line in lines)
    return {entry: is_ad for entry, is_ad in parsed}


def  _parse(line):
    """Parse 'entry-name,[0,1] and return (entry-name,is_ad) """
    line = line.strip()
    div_pos = line.find(',')
    if div_pos+2 != len(line):
        raise ValueError('Could not parse {}.'.format(line))
    entry = line[:div_pos]
    is_ad = bool(int(line[-1]))
    return entry, is_ad

