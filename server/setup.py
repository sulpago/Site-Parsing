from flask import Flask
from flask_restplus import Api
from flask_bootstrap import Bootstrap
from server.front.setup import create_view
from server.api.setup import create_api
from common.logger import logger

logger.initialize()


def create_app():
    template_path = "../resources/templates"
    static_path = "../resources/static"

    flask_app = Flask(__name__, template_folder=template_path,static_folder=static_path)

    # Crate Views
    logger.info("Create Server Health Check")
    create_view(flask_app)
    Bootstrap(flask_app)
    flask_app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Create Api
    rest_api = Api(flask_app, doc=False)
    rest_parser = rest_api.parser()
    logger.info("Create Api For Check")
    create_api(rest_api)

    logger.info("All Application Create Done")

    return flask_app
