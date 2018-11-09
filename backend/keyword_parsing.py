import urllib3
import json
import re
from bs4 import BeautifulSoup
from backend.keyword_parsing_worker import ImageCheckWorker, ImageResultSum
from multiprocessing import Queue as ProcQueue
from common.logger import logger

logger.initialize()

class ImageParsingByKeyword(object):
    def __init__(self, id_name):
        self.id_name = id_name
        self.num_threads = 8
        self.queue_endian = "GENERATOR_QUEUE_END"

    def request_query(self, category, keyword, page=1):
        logger.debug("Request Query to G9")
        self.item_dict = None
        self.item_del_dict = None
        self.item_del_dict = dict()
        http = urllib3.PoolManager()

        page_info = page
        search_keyword = keyword
        target_category = category

        raw_keyword = str(search_keyword.encode('utf-8'))
        raw_keyword = raw_keyword[1:]
        raw_keyword = raw_keyword.replace("'", "")
        raw_keyword = raw_keyword.replace("x", "")

        encode_keyword = re.sub("[/\\\:?\"]", "%", raw_keyword)

        query_url = 'http://www.g9.co.kr/Display/Category/' + \
                    str(target_category) + '?page=' + str(page_info) + \
                    "&sort=latest&viewType=B&searchQuery=%20" + encode_keyword

        print(query_url)
        req = http.request('GET', query_url, preload_content=False)
        decoded_html = (req.data).decode('utf-8')


        self.parsing_html = decoded_html
        req.release_conn()

    def get_items_in_page(self):
        logger.debug("Get Items From HTML response")
        decoded_html = self.parsing_html

        item_dict = dict()

        soup = BeautifulSoup(decoded_html, 'html.parser')
        items = soup.find_all('li')

        for cached_item in items:
            class_type = cached_item.get('class')
            if class_type is None:
                continue
            if 'format-itemcard-list__item' in class_type:
                single_item = cached_item.find('a')
                type_code = single_item.get('data-area-type')
                if type_code == 'item':
                    item_parameter = single_item.get('data-area-parameter')
                    temp_item_json = json.loads(item_parameter)
                    temp_goodscode = temp_item_json.get('goodscode')
                    if temp_goodscode not in item_dict:
                        item_dict[temp_goodscode] = temp_item_json


        # items = soup.find_all('a')
        # for single_item in items:
        #     type_code = single_item.get('data-area-type')
        #     if type_code == 'item':
        #         item_parameter = single_item.get('data-area-parameter')
        #         temp_item_json = json.loads(item_parameter)
        #         temp_goodscode = temp_item_json.get('goodscode')
        #         if temp_goodscode not in item_dict:
        #             item_dict[temp_goodscode] = None

        self.item_dict = item_dict
        logger.debug("Get Items Dictornary " + str(self.item_dict))
        return self.item_dict

    def get_item_page_num(self):
        decoded_html = self.parsing_html

        soup = BeautifulSoup(decoded_html, 'html.parser')
        items = soup.find_all('a')
        for single_item in items:
            type_code = single_item.get('data-area-type')
            if type_code == 'utility':
                page_parameter = single_item.get('onclick')
                if page_parameter:
                    print(page_parameter)

    def get_itemlist(self):
        if self.item_dict:
            return self.item_dict
        else:
            return None

    def get_delete_item_list(self):
        if self.item_del_dict:
            return self.item_del_dict
        else:
            return None

    def delete_goodscode(self, goodscode):
        if goodscode not in self.item_dict:
            # print("Wrong Goodscode, " + goodscode)
            return False

        item_del_dict = self.item_del_dict
        if goodscode in item_del_dict:
            logger.warning("Already Added,  Goodscode :" + goodscode)
        else:
            # print("Added to Delete list,  Goodscode :" + goodscode)
            item_del_dict[goodscode] = None
        self.item_del_dict = item_del_dict
        return True

    def put_goodscode(self, goodscode):
        if goodscode not in self.item_dict:
            # print("Wrong Goodscode, " + goodscode)
            return False
        item_del_dict = self.item_del_dict
        if goodscode in item_del_dict:
            # print("Remove from Delete list,  Goodscode :" + goodscode)
            del item_del_dict[goodscode]
        else:
            logger.warning("Already  Delete,  Goodscode :" + goodscode)
        self.item_del_dict = item_del_dict
        return True

    def get_item_url_check(self):
        logger.debug("URL Item Exist Check")
        item_dict = self.item_dict
        item_dict_key = item_dict.keys()

        queue_endian = self.queue_endian
        threads_num = self.num_threads
        good_item_queue = ProcQueue()
        good_item_result_queue = ProcQueue()

        logger.debug("Item Num Producer")
        for goodscode in item_dict_key:
            item_id = str(goodscode)
            good_item_queue.put(item_id)
        for i in range(0, threads_num):
            good_item_queue.put(queue_endian)

        run_threads = list()

        logger.debug("Item Image URL check")
        for i in range(0, threads_num):
            __single_thread = ImageCheckWorker(good_item_queue, good_item_result_queue, queue_endian)
            run_threads.append(__single_thread)
            __single_thread.start()

        for __single_thread in run_threads:
            __single_thread.join()

        # good_item_result_queue.put(queue_endian)

        logger.debug("Get Null Item List")
        null_image_list = ImageResultSum(good_item_result_queue, queue_endian, threads_num)

        logger.debug("Remove Null Item List")
        for null_item in null_image_list:
            del item_dict[null_item]

        logger.debug("Close Queues")
        good_item_queue.close()
        good_item_queue.join_thread()

        good_item_result_queue.close()
        good_item_result_queue.join_thread()

        self.item_dict = item_dict
        print(str(self.item_dict))

        return self.item_dict

    def get_item_url_checkV0(self):
        print("get_item_url_check start")
        item_dict = self.item_dict

        item_dict_key = item_dict.keys()
        http = urllib3.PoolManager()
        null_image_list = list()
        for goodscode in item_dict_key:
            item_id = str(goodscode)
            img_url_convention = "http://image.g9.co.kr/g/" + str(item_id) + "/o"
            req = http.request('GET', img_url_convention)
            item_image_status = req.status
            if item_image_status != 200:
                print("Blank Item Remove " + str(goodscode))
                null_image_list.append(goodscode)

        for null_item in null_image_list:
            del item_dict[null_item]

        self.item_dict = item_dict
        print(str(self.item_dict))
        print("get_item_url_check done")
        return self.item_dict


def get_ipbk_object(watcher, request):
    user_id = request.remote_addr
    w_user = watcher.get_user(user_id)
    if w_user is None:
        watcher.create_user(user_id)
        w_user = watcher.get_user(user_id)

    ipbk = w_user.get("IPBK", None)
    if ipbk is None:
        ipbk = ImageParsingByKeyword(str(user_id))
        watcher.modify_user(user_id, "IPBK", ipbk)
    return ipbk
