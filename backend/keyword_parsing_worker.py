import urllib3
import os
import threading
from common.logger import logger

logger.initialize()


class ImageCheckWorker(threading.Thread):
    def __init__(self, input_queue, result_queue, queue_endian=None):
        threading.Thread.__init__(self)
        self.input_queue = input_queue
        self.result_queue = result_queue
        self.queue_endian = queue_endian

    def run(self):
        input_queue = self.input_queue
        result_queue = self.result_queue
        queue_endian = self.queue_endian

        while True:
            if input_queue is not None:
                __get_queue = input_queue.get()
                if __get_queue == queue_endian:
                    logger.debug("ImageCheckWorker Done")
                    result_queue.put(queue_endian)
                    break
                else:
                    __get_data = __get_queue
                    # print(__get_data)
                    goodscode = __get_data.strip()
                    if goodscode is not None:
                        __img_exist = exist_check(goodscode)
                        __ret_data = [goodscode, __img_exist]
                        result_queue.put(__ret_data)
                    else:
                        logger.warning(str(os.getpid()) + " / Warning with Queue " + str(__get_queue))
            else:
                logger.critical("Queue is Empty")
                break


def ImageResultSum(result_queue, queue_endian, threads_num):
    __counter = 0
    __check_endian = 0

    null_image_list = list()

    while True:
        if result_queue is not None:
            __get_queue = result_queue.get()

            if __get_queue == queue_endian:
                __check_endian = __check_endian + 1
                logger.debug("Get Endian")
                if __check_endian == threads_num:
                    logger.debug("ImageResultSum Done")
                    break
            else:
                __data = __get_queue
                goodscode = __data[0]
                exist = __data[1]
                if exist is False:
                    print("Null Goodscode " + str(goodscode))
                    null_image_list.append(goodscode)
        else:
            logger.critical("Queue is Empty")
            break

    return null_image_list


def exist_check(goodscode):
    http = urllib3.PoolManager()
    item_id = str(goodscode)
    img_url_convention = "http://image.g9.co.kr/g/" + str(item_id) + "/o"
    req = http.request('GET', img_url_convention)
    item_image_status = req.status
    if item_image_status != 200:
        print("Blank Item Remove " + str(goodscode))
        req.release_conn()
        return False
    else:
        req.release_conn()
        return True
