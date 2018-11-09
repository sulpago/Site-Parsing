from backend.keyword_parsing import ImageParsingByKeyword
from multiprocessing import freeze_support

def test_parsing():
    ipbk = ImageParsingByKeyword("DEV")
    page = 4
    keyword = '기본셔츠'
    category = '400000076/500001266/600005247'
    ipbk.request_query(category=category, keyword=keyword, page=page)

    ipbk.get_items_in_page()
    # ipbk.get_item_page_num()
    # ipbk.get_item_url_check()

def timestamp_check():
    import datetime
    print(datetime.datetime.now())

def filedownload_check():
    from backend.image_downloader_worker import url_image_download
    url_image_download('D:\WorkPlace\Python\machine-learning\Gnine.Image.Parsing\dummy', '1500741652')

if __name__ == '__main__':
    freeze_support()
    filedownload_check()