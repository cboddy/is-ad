import sys
import logging
import os
import pickle
import gzip
import os.path
from argparse import ArgumentParser
from is_ad.learn.skl import (
    PipelineInput,
    run,
    run_grid_optimization
)

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def main():
    parser = ArgumentParser('Run the text classification pipeline.')
    parser.add_argument('--docs', help='Path to input zip docs.', type=str, required=True)
    parser.add_argument('--categories', help='Path to input category zip docs.', type=str, required=True)
    parser.add_argument('--test_fraction', help='Fraction of docs used for testing.', type=float, default=0.1)
    parser.add_argument('--pipeline', help='Name of pipeline', type=str, default='baseline')
    parser.add_argument('--max_doc_count', help='Maximum number of documents to use.', type=int, default=-1)
    parser.add_argument('--output_path', help='Path to save text-classification model.', type=str, required=False)
    args = parser.parse_args()

    pipeline_name = args.pipeline
    category_path = args.categories
    test_fraction = args.test_fraction
    max_doc_count = args.max_doc_count

    if os.path.isdir(args.docs):
        input_files = [os.listdir(args.docs)]
    elif os.path.isfile(args.docs):
        input_files = [args.docs]
    else:
        raise ValueError('{} is not a directory or a file.'.format(args.docs))

    logging.info('''Running {pipeline_name} pipeline,
    input files: {input_files},
    category-file path: {category_path},
    testing-document fraction: {test_fraction},
    max-doc-count: {max_doc_count}'''.format(**locals()))

    pipeline_input = PipelineInput(category_path,
                                   input_files,
                                   test_fraction,
                                   max_doc_count)

    model, report = run(pipeline_input,
        pipeline_name)

    # run_grid_optimization(pipeline_input,
    #                       pipeline_name)

    if 'output_path' in args:
        output_path = args.output_path
        if not output_path.endswith('.gz'):
            output_path += '.gz'
        logging.info('Writing output model to {}'.format(output_path))
        with gzip.open(output_path, 'w') as f:
            pickle.dump(model, f)


if __name__ == '__main__':
    main()
