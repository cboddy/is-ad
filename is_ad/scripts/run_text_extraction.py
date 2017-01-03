import sys
import logging
import os
import os.path
from argparse import ArgumentParser
from multiprocessing import Pool
from is_ad.parse.html import unzip_and_extract_text

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def main():
    parser = ArgumentParser('HTML doc  text extraction.')
    parser.add_argument('--input', help='Path to input zip files.', type=str, required=True)
    parser.add_argument('--output', help='Path to output  zip file.', type=str, required=True)
    parser.add_argument('--n_proc', help='Number of processes.', type=int, default=4)
    args = parser.parse_args()

    input_zip_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.zip')]
    n_proc = args.n_proc
    output_dir = args.output

    logging.info(
        'Running with input {input_zip_files},  {n_proc} processes and output_dir {output_dir}'.format(**locals()))

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    pool = Pool(n_proc)

    output_zip_files = [os.path.join(output_dir, os .path.basename(x)) for x in input_zip_files]

    results = [pool.apply_async(unzip_and_extract_text, [in_file, out_file])
               for in_file, out_file in zip(input_zip_files, output_zip_files)]

    for result in results:
        result.get()

    pool.close()

if __name__ == '__main__':
    main()
