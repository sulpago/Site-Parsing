from flask import request
from flask_restplus import Resource
from common.logger import logger
from backend.keyword_parsing import get_ipbk_object
from backend.image_downloader import get_imdo_object, ImageDownloader

import copy

logger.initialize()


def create(rest_api, watcher):
    @rest_api.route('/joosohn/image/list')
    class Image_List_Check(Resource):
        def delete(self):
            req_goodscode = request.form["goodscode"]
            if req_goodscode is None:
                return {"Error": "Unexpected form error"}
            image_parsing_manager = get_ipbk_object(watcher, request)
            image_parsing_manager.delete_goodscode(req_goodscode)
            return "Delete"

        def put(self):
            req_goodscode = request.form["goodscode"]
            if req_goodscode is None:
                return {"Error": "Unexpected form error"}
            image_parsing_manager = get_ipbk_object(watcher, request)
            image_parsing_manager.put_goodscode(req_goodscode)
            return "Put"

        def get(self):
            image_parsing_manager = get_ipbk_object(watcher, request)
            itemlist = image_parsing_manager.get_delete_item_list()
            return str(itemlist)

    @rest_api.route('/joosohn/image/download')
    class Image_List_Check(Resource):
        def post(self):
            req_basepath = request.form["basepath"]
            req_categorname = request.form["categoryname"]
            if req_basepath is None or req_categorname is None:
                return {"Error": "Unexpected form error"}

            image_parsing_manager = get_ipbk_object(watcher, request)
            items_dict = copy.deepcopy(image_parsing_manager.get_itemlist())
            item_remove_dict = copy.deepcopy(image_parsing_manager.get_delete_item_list())

            image_download_manager = get_imdo_object(watcher, request)
            # image_download_manager = ImageDownloader("Downloader")
            image_download_manager.create_folders(req_basepath, req_categorname)
            image_download_manager.get_item_dict(items_dict, item_remove_dict)
            image_download_manager.image_download()

            return "Downloaded"
