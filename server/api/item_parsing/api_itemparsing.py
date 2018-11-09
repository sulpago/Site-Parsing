from flask import request
from flask_restplus import Resource
from backend.keyword_parsing import get_ipbk_object

from common.logger import logger

logger.initialize()


def create(rest_api, watcher):
    @rest_api.route('/joosohn/image/parsing/keyword')
    class Image_Parsing_Keyword(Resource):
        def post(self):
            # print(request.remote_addr)

            req_category = request.form["category"]
            req_keyword = request.form["keyword"]
            req_page = request.form["page"]

            if req_page is None or req_keyword is None or req_category is None:
                return {"Error": "Unexpected form error"}

            # ipbk = image_parsing_manager
            # page = 4
            # keyword = '기본셔츠
            # category = '400000076/500001266/600005249'
            ipbk = get_ipbk_object(watcher, request)
            ipbk.request_query(category=req_category, keyword=req_keyword, page=req_page)
            ipbk.get_items_in_page()
            item_dicts = ipbk.get_item_url_check()
            item_dicts_key = item_dicts.keys()
            html_item_card = ""
            for goodscode in item_dicts_key:
                html_item_card = html_item_card + imageBoxMaker(goodscode=goodscode)

            html_header = "<div class='row'>"
            html_footer = "</div>"
            html_code = html_header + html_item_card + html_footer
            return html_code


def imageBoxMakerV0(goodscode):
    item_goodscode = str(goodscode)
    item_img_id = 'img_' + str(goodscode)
    item_img_src = 'http://image.g9.co.kr/g/' + str(goodscode) + '/o'
    base_html_card_title = "<div class='card'><div class='card-header'><h3><b>" + item_goodscode + "</b></h3></div>"
    base_html_image_body = "<div class='card-body'><img id=" + item_img_id + " src=" + item_img_src
    base_html_image_option = " width='60' height='60' align='center' style='display:block;'>"
    base_html_card_footer = "</div></div>"
    base_html_code = base_html_card_title + base_html_image_body + base_html_image_option + base_html_card_footer
    return base_html_code


def imageBoxMakerV1(goodscode):
    item_goodscode = str(goodscode)
    item_img_id = 'img_' + str(goodscode)
    item_img_src = 'http://image.g9.co.kr/g/' + str(goodscode) + '/o'
    base_html_card_header = "<div class='card' style='width: 18rem;'>"
    base_html_img_top = "<img class='card-img-top' src=" + item_img_src + " alt=" + item_img_id
    base_html_image_option = " style='height: 160px; width: 160px; object-fit: contain;'>"
    base_html_card_body = "<div class='card-body'><h5 class='card-title'>" + item_goodscode + "</h5>"
    base_html_card_footer = "</div></div>"
    base_html_code = base_html_card_header + base_html_img_top + base_html_image_option + base_html_card_body + base_html_card_footer
    return base_html_code


def imageBoxMaker(goodscode):
    item_goodscode = str(goodscode)
    item_img_id = 'img_' + str(goodscode)
    item_img_src = 'http://image.g9.co.kr/g/' + str(goodscode) + '/o'
    item_vip_link = 'http://www.g9.co.kr/Display/VIP/Index/' + str(goodscode)
    base_html_header = "<div class='col-sm-2';>"
    base_html_img = "<img src=" + item_img_src + " alt=" + item_goodscode + " id=" + item_img_id
    base_html_image_action = " onclick='removeImage(" + item_img_id + ")'"
    base_html_image_option = " style='height: 100%; width: 100%; object-fit: contain; opacity: 1;'>"
    base_html_body = "<h5><a href=" + item_vip_link + " target='_blank'> " + item_goodscode + "</a></h5>"
    # base_html_image_option = ' >'
    base_html_footer = "</div>"
    base_html_code = base_html_header + base_html_img + base_html_image_action + base_html_image_option + base_html_body + base_html_footer
    return base_html_code
