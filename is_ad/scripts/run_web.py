import sys
import logging
import argparse
import os.path

from is_ad.learn.skl import read_model
from is_ad.web.app import (
    app,
    init
)

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def main():
    parser = argparse.ArgumentParser('Is this an ad webservice runner.')
    parser.add_argument('--model_path', help='Path to text-classification model.', type=str, required=True)
    parser.add_argument('--db_url', help='database connection URL.', type=str, required=True)
    parser.add_argument('--port', type=int, default=6543, required=False)
    args = parser.parse_args()
    model_path = args.model_path
    db_url = args.db_url
    port = args.port

    logging.info('Starting web-service with model-path {model_path} and db-url {db_url} on port {port}.'
                 .format(**locals()))

    # de-serialize the model
    logging.info('Starting model deserialisation from {}'.format(model_path))
    text_cf = read_model(model_path)
    # text_cf = None
    logging.info('Finished model deserialisation from {}'.format(model_path))
    # init the web-app
    model_name = os.path.basename(model_path)
    init(text_cf, model_name, db_url)
    # start the app
    app.run(port=port, threaded=True)


if __name__ == '__main__':
    main()
