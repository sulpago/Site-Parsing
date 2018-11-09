def file_name_generator(identification='Noname', title='Unknown', extension='txt', add_time=True):
    import datetime

    if add_time is True:
        __file_name = identification + "_" + title + "_" + str(
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + "." + extension
    else:
        __file_name = identification + "_" + title + "." + extension

    return __file_name


def model_figure_save(model, save_path):
    import time
    from keras.utils.vis_utils import plot_model

    time.sleep(1)
    plot_model(model, to_file=save_path, show_shapes=True, show_layer_names=True)
    time.sleep(1)


def history_save(history, save_path):
    import matplotlib.pyplot as plt

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['acc', 'val_acc'], loc='upper left')
    plt.savefig(save_path)
    plt.clf()
    plt.cla()
    plt.close()


def indexed_dict_keys(target_dict):
    cached_dict_key_list = sorted(list(target_dict.keys()))
    ret_dict = dict()
    for idx, keys_value in enumerate(cached_dict_key_list):
        if keys_value is None:
            print("     Keys Value is None")
        ret_dict[idx] = keys_value
    return ret_dict


def indexed_dict_rearrange(target_dict, skip_None=True):
    get_keys = sorted(list(target_dict.keyts()))
    ret_dict = dict()
    dict_idx = 0
    for idx, key_idx in enumerate(get_keys):
        cached_value = target_dict.get(key_idx, None)
        if skip_None:
            if cached_value is not None:
                dict_idx = dict_idx + 1
                ret_dict[dict_idx] = cached_value
            else:
                print("     Get Value is None")
        else:
            ret_dict[idx] = cached_value

    return ret_dict


def dict_revserse(target_dict):
    return {v: k for k, v in target_dict.items()}
