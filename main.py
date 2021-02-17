import logging
from argparse import ArgumentParser

from aiohttp import web

from blog_app.web.app import create_app
from blog_app.settings import config
from blog_app.worker.worker import run_worker

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    arg_parser = ArgumentParser(description="specify running service")
    arg_parser.add_argument(
        "service", help="web or worker", default="web", type=str
    )
    args = arg_parser.parse_args()
    if args.service == "worker":
        run_worker()
    else:
        web.run_app(create_app(), port=config["server"]["port"])
