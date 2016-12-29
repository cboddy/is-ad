import sys
import logging
from argparse import ArgumentParser
from multiprocessing import Pool
from ad_finder.parse.html import unzip_and_extract_text

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level = logging.INFO)


def main():
    parser = ArgumentParser('HTML doc  text extraction.')
    parser.add_argument('--input', help='Path to input zip files.', type=str, required=True)
    parser.add_argument('--output', help='Path to output  zip file.', type=str, required=True)
    args = parser.parse_args()

    logging.info('Running with input {} and n-proc {}'.format(args.input, args.output))
    # pool = Pool(n_proc)
    # pool.apply()

    unzip_and_extract_text(args.input, args.output)


if  __name__ == '__main__':
    main()