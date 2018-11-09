import os
import json
import shutil
import csv


def create_file(file_path):
    if file_exist(file_path) is False:
        try:
            os.mknod(file_path)
            return True
        except:
            return False
    return False


def create_folder(filepath):
    __path_format = os.path.normpath(filepath)
    __path_array = __path_format.split(os.sep)
    __length = len(__path_array)
    __check_path = __path_array[0]

    # Auto Make Folders
    for i in range(1, __length):
        __check_path = __check_path + "/" + __path_array[i]
        __check_path = os.path.normpath(__check_path)
        if os.path.isdir(__check_path) is True:
            pass
        else:
            try:
                os.mkdir(__check_path)
            except:
                return False

    return True



def remove_file(file_path):
    if file_exist(file_path) is True and os.path.isfile(file_path) is True:
        try:
            os.remove(file_path)
            return True
        except:
            return False
    return False

def file_save(filename, data):
    with open(filename, "wb") as __tempFile:
        try:
            __tempFile.write(data)
            return True
        except:
            print("     Unknown Save Error")
            return False

def file_exist(file_path):
    try:
        if os.path.exists(file_path):
            return True
        else:
            return False
    except:
        return False


def path_comapre(file_path_A, file_path_B):
    try:
        __norm_A = os.path.normcase(file_path_A)
        __norm_B = os.path.normcase(file_path_B)
        __flag = os.path.samefile(__norm_A, __norm_B)
        return __flag
    except:
        return False


def file_copy(src_path, dst_path):
    shutil.copy(src_path, dst_path)


def file_move(src_path, dst_path):
    shutil.move(src_path, dst_path)


def base_server_path():
    __util_file_path = os.path.dirname(os.path.abspath(__file__))
    (__path_common, __path_filesystem) = os.path.split(__util_file_path)
    (__path_server, __path_common) = os.path.split(__path_common)
    return __path_server


def read_json_file(filepath):
    __ret_json = None
    __is_exist = file_exist(filepath)
    if __is_exist is False:
        return __ret_json
    with open(filepath, 'r') as __default_config:
        __ret_json = json.load(__default_config)
    return __ret_json


def save_json_file(filepath, json_data):
    create_file(filepath)
    with open(filepath, 'w') as __running_config:
        json.dump(json_data, __running_config)
    return True


def get_folders(folder_path):
    depth = 1
    for __dirpath, __dirnames, __filenames in os.walk(folder_path):
        if depth == 1:
            __folders = __dirnames
            break
    return __folders


def get_folders_v2(folder_path):
    cached_dicted_file = get_files_to_dict(folder_path)
    filterd_folder_list = filtering_folder_from_files(cached_dicted_file)
    return filterd_folder_list


def filtering_folder_from_files(dicted_file):
    from tqdm import tqdm

    cached_dict_folder = dict()

    num_of_files = len(dicted_file)
    progress_tqdm = tqdm(total=num_of_files, desc='Folder Filtering', unit_scale=True, dynamic_ncols=True,
                         leave=True)

    for idx in range(0, num_of_files):
        progress_tqdm.update(idx - progress_tqdm.n)
        __target_file = dicted_file.get(idx, None)
        if __target_file is None:
            continue
        sliced_path = os.path.split(__target_file)
        key_folder = sliced_path[0]
        if key_folder not in cached_dict_folder:
            cached_dict_folder[key_folder] = True

    progress_tqdm.close()
    filtered_folder_path = list(cached_dict_folder.keys())

    return filtered_folder_path


def convert_folder_to_database(root_path, depth=0):
    __contents = os.listdir(root_path)
    __results = []
    for __files in __contents:
        __results.append(__files)

    return __results
    # has file name or not


def search_file(root_path, results):
    __path = os.path.normpath(root_path)
    __files = os.listdir(__path)

    __test_array = results

    for __file in __files:
        __full_file = os.path.join(__path, __file)
        if os.path.isdir(__full_file):
            search_file(__full_file, __test_array)
        else:
            __test_array.append(__full_file)
            print(__full_file)


def get_files(folder_path):
    __path = os.path.normpath(folder_path)
    __results = []
    for __dirpath, __dirnames, __filenames in os.walk(__path):
        for __file in __filenames:
            __check_path = os.path.join(__dirpath, __file)
            __results.append(str(__check_path))
    return __results


def get_files_to_dict(folder_path):
    __path = os.path.normpath(folder_path)
    __results = {}
    __index_key = 0
    for __dirpath, __dirnames, __filenames in os.walk(__path):
        for __file in __filenames:
            __check_path = os.path.join(__dirpath, __file)
            __results[__index_key] = (str(__check_path))
            __index_key = __index_key + 1
    return __results


def get_folders_to_dictv0(folder_path):
    __path = os.path.normpath(folder_path)
    __results = {}
    __index_key = 0
    for __dirpath, __dirnames, __filenames in os.walk(__path):
        for __dir in __dirnames:
            __check_path = os.path.join(__dirpath, __dir)
            __results[__index_key] = (str(__check_path))
            __index_key = __index_key + 1
    return __results


def get_folders_to_dict(folder_path):
    __path = os.path.normpath(folder_path)
    __results = {}
    __index_key = 0
    __cached_dict = {}
    for __dirpath, __dirnames, __filenames in os.walk(__path):
        for __dir in __dirnames:
            len_of_files = len(__filenames)
            if len_of_files != 0:
                # print("     Uppper Directory Path")
                continue
            __check_path = os.path.join(__dirpath, __dir)
            __results[__index_key] = (str(__check_path))
            __index_key = __index_key + 1
    return __results


# def file_counter(dir, counter=0):
#     "returns number of files in dir and subdirs"
#     for pack in os.walk(dir):
#         for f in pack[2]:
#             counter += 1
#     return dir + " : " + str(counter) + "files"

def save_pandas(base_path, data, title="results", worksheet='savedata', use_reg_data=False):
    import pandas as pd
    import datetime

    if use_reg_data is True:
        __file_name = title + "_" + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + ".xlsx"
    else:
        __file_name = title + ".xlsx"

    __file_path = os.path.join(base_path, __file_name)
    __savedata = pd.ExcelWriter(__file_path, engine="xlsxwriter")
    data.to_excel(__savedata, sheet_name=worksheet, index=True)
    __savedata.save()
    return True


def dict_to_save(target_dict, save_path):
    with open(save_path, 'w', newline='') as csvfile:
        __dump_data = csv.writer(csvfile, delimiter=',')
        for __key, __val in target_dict.items():
            __dump_data.writerow([__key, __val])


def list_to_save(target_list, save_path):
    with open(save_path, 'w', newline='') as csvfile:
        __dump_data = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for __row in target_list:
            __dump_data.writerow(__row)


def read_csv_to_dict(target_path, overwirte_key=False):
    read_dict = dict()

    with open(target_path, 'r') as csvfile:
        cached_data = csv.reader(csvfile, delimiter=',')
        for row in cached_data:
            read_key = row[0]
            read_val = row[1]
            if overwirte_key is False:
                if read_key in read_dict:
                    print("     Duplicated Unique Index")
                    continue
            read_dict[read_key] = read_val

    return read_dict


def get_file_name(target_path, with_ext=False):
    cached_filename = os.path.basename(target_path)
    if with_ext:
        return str(cached_filename)
    else:
        return str(os.path.splitext(cached_filename)[0])
