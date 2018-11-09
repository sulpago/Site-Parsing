from flask_restplus import Resource
from flask import request

from common.logger import logger
logger.initialize()

def create(rest_api):
    @rest_api.route('/status/healthcheck')
    class HealthCheck(Resource):
        def get(self):
            logger.debug("Health Check")
            return {"HealthCheck": str(True)}

    @rest_api.route('/postcheck')
    class Postcheck(Resource):
        def post(self):
            img_file = request.files['image_data']
            ret_name = img_file.filename
            logger.debug(ret_name)
            html_code = "<h4> Target Image :" + str(ret_name) + "</h4>"
            return str(html_code)
