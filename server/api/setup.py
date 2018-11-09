from common.logger import logger
from backend.watcher import Watcher
from server.api.status import api_healthcheck
from server.api.item_parsing import api_itemparsing
from server.api.item_download import api_itemdownload

logger.initialize()

def create_api(rest_api):

    watcher = Watcher("DEV")

    logger.info("Create API Health Check")
    api_healthcheck.create(rest_api)

    logger.info("Create API Item Parsing")
    api_itemparsing.create(rest_api, watcher)

    logger.info("Create API Item Download")
    api_itemdownload.create(rest_api, watcher)