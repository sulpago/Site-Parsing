import logging


class logger:
    _active_logging = None
    _active_name = "TF_API_ACTIVE"
    _active_formatter = None
    _active_file_handler = None
    _active_stream_handler = None

    _error_logging = None
    _error_name = "TF_API_ERROR"
    _error_formatter = None
    _error_file_handler = None
    _error_stream_handler = None
    _configuration = False

    @classmethod
    def init_Active_Log(cls):
        cls._active_logging = logging.getLogger(cls._active_name)
        cls._active_logging.setLevel(logging.DEBUG)
        cls._active_formatter = logging.Formatter(
            '%(asctime)s [ %(levelname)s ] %(message)s')
        cls._active_stream_handler = logging.StreamHandler()
        cls._active_stream_handler.setFormatter(cls._active_formatter)
        cls._active_logging.addHandler(cls._active_stream_handler)

    @classmethod
    def init_Error_Log(cls):
        cls._error_logging = logging.getLogger(cls._error_name)
        cls._error_formatter = logging.Formatter(
            '%(asctime)s [ %(levelname)s ] %(message)s')
        cls._error_stream_handler = logging.StreamHandler()
        cls._error_stream_handler.setFormatter(cls._error_formatter)
        cls._error_logging.addHandler(cls._error_stream_handler)

    @classmethod
    def initialize(cls):
        if cls._configuration is False:
            cls.init_Active_Log()
            cls.init_Error_Log()
            cls._configuration = True
            # else:
            #     cls.warning("Logger is Already initialize")

    @classmethod
    def set_Active_Config(cls, base_config):
        cls._active_logging.basicConfig(base_config)

    @classmethod
    def set_Error_config(cls, base_config):
        cls._error_logging.basicConfig(base_config)

    @classmethod
    def set_Active_File(cls, save_path):
        if cls._active_file_handler is not None:
            cls._active_file_handler.close()
            cls._active_logging.removeHandler(cls._active_file_handler)
            cls._active_file_handler = None
        cls._active_file_handler = logging.FileHandler(save_path)
        cls._active_logging.addHandler(cls._active_file_handler)

    @classmethod
    def set_Error_File(cls, save_path):
        if cls._error_file_handler is not None:
            cls._error_file_handler.close()
            cls._error_logging.removeHandler(cls._error_file_handler)
            cls._error_file_handler = None
        cls._error_file_handler = logging.FileHandler(save_path)
        cls._error_logging.addHandler(cls._error_file_handler)

    @classmethod
    def debug(cls, message):
        cls._active_logging.debug(message)
        # print("[Debug] " + str(message))

    @classmethod
    def info(cls, message):
        cls._active_logging.debug(message)
        # print("[Info] " + str(message))

    @classmethod
    def warning(cls, message):
        cls._error_logging.warning(message)
        # print("[Warning] " + str(message))

    @classmethod
    def error(cls, message):
        cls._error_logging.error(message)
        # print("[error] " + str(message))

    @classmethod
    def critical(cls, message):
        cls._error_logging.critical(message)
        # print("[critical] " + str(message))