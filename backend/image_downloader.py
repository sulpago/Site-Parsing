import os
from backend.image_downloader_worker import ImageDownloaderWorker
from multiprocessing import Queue as ProcQueue
from common.logger import logger
from common import filesystem

logger.initialize()


class ImageDownloader(object):
    def __init__(self, id_name):
        self.id_name = id_name
        self.num_threads = 8
        self.queue_endian = "GENERATOR_QUEUE_END"

    def create_folders(self, base_path, category_name):
        logger.debug("Create Save Folder Directory")
        self.base_path = base_path
        self.category_name = category_name
        save_path = os.path.join(base_path, category_name)
        save_path = os.path.normcase(save_path)
        filesystem.create_folder(save_path)
        self.save_path = save_path

    def get_item_dict(self, items_dict, item_remove_dict):
        logger.debug("Check Item from remove dict")
        self.download_item_dict = None
        if item_remove_dict:
            for remove_item in item_remove_dict.keys():
                if remove_item in items_dict:
                    del items_dict[remove_item]
        self.download_item_dict = items_dict

    def image_download(self):
        queue_endian = self.queue_endian
        threads_num = self.num_threads
        download_item_queue = ProcQueue()
        save_path = self.save_path
        download_item_dict = self.download_item_dict

        logger.debug("Item Num Producer")
        for goodscode in download_item_dict:
            item_id = str(goodscode)
            input_data = [save_path, item_id]
            download_item_queue.put(input_data)
        for i in range(0, threads_num):
            download_item_queue.put(queue_endian)

        run_threads = list()

        logger.debug("Item Image URL check")
        for i in range(0, threads_num):
            __single_thread = ImageDownloaderWorker(download_item_queue, queue_endian)
            run_threads.append(__single_thread)
            __single_thread.start()

        for __single_thread in run_threads:
            __single_thread.join()

        logger.debug("Close Queues")
        download_item_queue.close()
        download_item_queue.join_thread()

def get_imdo_object(watcher, request):
    user_id = request.remote_addr
    w_user = watcher.get_user(user_id)
    if w_user is None:
        watcher.create_user(user_id)
        w_user = watcher.get_user(user_id)

    imdo = w_user.get("IMDO", None)
    if imdo is None:
        imdo = ImageDownloader(str(user_id))
        watcher.modify_user(user_id, "IMDO", imdo)
    return imdo