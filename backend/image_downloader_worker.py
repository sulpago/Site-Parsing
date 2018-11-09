import urllib3
import os
import threading
from common.logger import logger
from common import filesystem

logger.initialize()


class ImageDownloaderWorker(threading.Thread):
    def __init__(self, input_queue, queue_endian=None, overwrite=False):
        threading.Thread.__init__(self)
        self.input_queue = input_queue
        self.queue_endian = queue_endian
        self.overwrite = overwrite

    def run(self):
        input_queue = self.input_queue
        queue_endian = self.queue_endian
        overwrite = self.overwrite

        while True:
            if input_queue is not None:
                __get_queue = input_queue.get()
                if __get_queue == queue_endian:
                    logger.debug("ImageDownloader Done")
                    break
                else:
                    __get_data = __get_queue
                    # print(__get_data)
                    save_path = (__get_data[0]).strip()
                    goodscode = (__get_data[1]).strip()
                    if save_path is not None and goodscode is not None:
                        __flag = url_image_download(save_path, goodscode, overwrite)
                        if __flag is False:
                            logger.warning("Image Donwload Error " + goodscode)
                    else:
                        logger.warning(str(os.getpid()) + " / Warning with Queue " + str(__get_queue))
            else:
                logger.critical("Queue is Empty")
                break


def url_image_download(save_path, goodscode, overwrite):
    item_id = str(goodscode)
    __file_name = item_id + ".jpg"
    __file_path = os.path.join(save_path, __file_name)
    save_file_path = os.path.normcase(__file_path)

    if overwrite is False:
        if filesystem.file_exist(save_file_path):
            return True

    http = urllib3.PoolManager()
    img_url_convention = "http://image.g9.co.kr/g/" + str(item_id) + "/o"
    req = http.request('GET', img_url_convention)
    item_image_status = req.status
    if item_image_status != 200:
        logger.warning("Image URL Connection Error")
        req.release_conn()
        return False
    else:
        img_data = req.data
        is_saved = filesystem.file_save(save_file_path, img_data)
        req.release_conn()
        return is_saved
