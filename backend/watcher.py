from common.logger import logger

logger.initialize()


class Watcher(object):
    def __init__(self, id_name):
        self.id_name = id_name
        self.user_dict = dict()

    def get_user(self, user_id):
        user_dict = self.user_dict
        logger.debug("Request User : " + str(user_id))
        if user_id in user_dict:
            (user_dict[user_id])["timestamp"] = self._get_timestamp()
            return user_dict[user_id]
        else:
            return None

    def create_user(self, user_id):
        user_dict = self.user_dict
        if user_id in user_dict:
            print("Duplicated User")
            return True
        else:
            user_dict[user_id] = dict()
            (user_dict[user_id])["timestamp"] = self._get_timestamp()
            return True

    def _get_timestamp(self):
        import datetime
        return datetime.datetime.now()

    def modify_user(self, user_id, key, value):
        user_dict = self.user_dict
        if user_id in user_dict:
            (user_dict[user_id])["timestamp"] = self._get_timestamp()
            (user_dict[user_id])[key] = value
            return True
        else:
            return False
