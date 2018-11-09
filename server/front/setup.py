from common.logger import logger

from server.front.views import view_items, view_home

logger.initialize()

def create_view(flask_app):
    logger.info("Create Index View")
    view_home.create(flask_app)

    logger.info("Create Item View")
    view_items.create(flask_app)