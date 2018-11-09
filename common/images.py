import PIL.Image as pilImage
import numpy as np
import cv2
import matplotlib.image as plt_img

from keras.preprocessing.image import load_img

from common.logger import logger

logger.initialize()


def image_reshape_2(pil_image, width, height, dimension):
    __input_width = width
    __input_height = height
    __input_dimension = dimension
    __reshape_img = None

    if (pil_image is None):
        __input_zeros = np.zeros((__input_width * __input_height * __input_dimension))
        __reshape_img = np.reshape(__input_zeros, [1, __input_width, __input_height, __input_dimension])
    else:

        __rsz_img = pil_image.resize((__input_width, __input_height), pilImage.ANTIALIAS)
        __numpy_image = np.asarray(__rsz_img)

        __check_img_len = len(__numpy_image)
        if __check_img_len < __input_dimension:
            return False, None

        if __numpy_image.shape[2] > __input_dimension:
            __numpy_image = __numpy_image[:, :, :__input_dimension]  # 차원 축소 ;

        __reshape_img = np.reshape(__numpy_image, [1, __input_width, __input_height, __input_dimension])

    return True, __reshape_img


def image_reshape(file_path, img_width, img_height, img_dim):
    __input_width = img_width
    __input_height = img_height
    __input_dimension = img_dim

    __check_shape_type = (__input_height, __input_width, __input_dimension)

    # Pillow 라이브러리 사용하여 open
    # size – The requested size in pixels, as a 2-tuple: (width, height).
    # 파일 형식을 RGB로 변환하여 진행.

    with pilImage.open(file_path) as __open_pil:
        __resized_img = __open_pil.resize((__input_width, __input_height))
        __numpyed_array = np.array(__resized_img)
        __check_shape = __numpyed_array.shape
        if __check_shape != __check_shape_type:
            logger.critical("Reshape Array for prediction")
            logger.debug("File " + str(file_path) + " / Shape " + str(__check_shape))
            return None
        else:
            return __numpyed_array


def image_loading_extension(file_path, img_width, img_height, img_dim, category_output=1):
    # print("Image Loading")
    __width = img_width
    __height = img_height
    __dim = img_dim

    image_height_width = (__height, __width)
    __cached_img = image_check(file_path, image_height_width)
    __np_img = image_to_numpy_extension(__cached_img, __width, __height, __dim, category_output)
    return __np_img


def image_loading(file_path, img_width, img_height, img_dim, category_output=1):
    # print("Image Loading")
    __width = img_width
    __height = img_height
    __dim = img_dim

    image_height_width = (__height, __width)

    try:
        __cached_img = image_check(file_path, image_height_width)
        __np_img = image_to_numpy_extension(__cached_img, __width, __height, __dim, category_output)
        return __np_img
    except:
        # print('ValueError - ', file_path)
        return None


def image_loading_cv(file_path, img_width, img_height, img_dim):
    __input_width = img_width
    __input_height = img_height
    __input_dimension = img_dim

    try:
        __cached_img = plt_img.imread(file_path)
        __cached_img = cv2.resize(__cached_img, (img_width, img_height))
        __np_img = np.reshape(__cached_img, [1, __input_width, __input_height, __input_dimension])
        return __np_img
    except:
        # print('ValueError - ', file_path)
        return None


def image_stream(file_path, img_width, img_height, img_dim):
    __input_width = img_width
    __input_height = img_height
    __input_dimension = img_dim

    try:
        __cached_img = file_path
        __cached_img = cv2.resize(__cached_img, (img_width, img_height))
        __np_img = np.reshape(__cached_img, [1, __input_width, __input_height, 3])
        return __np_img
    except:
        # print('ValueError - ', file_path)
        return None


def image_to_numpy_extension(pil_img, image_width, image_height, image_dim, category_output):
    __p_img = np.asarray(pil_img)
    # __p_img = pil_img
    if __p_img.shape[2] > image_dim:
        __p_img = __p_img[:, :, :image_dim]  # 차원 축소 ;

    __reshape_img = np.reshape(__p_img, [category_output, image_width, image_height, image_dim])
    return __reshape_img


def image_to_numpy(pil_img, image_width, image_height, image_dim):
    __p_img = np.asarray(pil_img)
    # __p_img = pil_img
    if __p_img.shape[2] > image_dim:
        __p_img = __p_img[:, :, :image_dim]  # 차원 축소 ;

    __reshape_img = np.reshape(__p_img, [image_width, image_height, image_dim])
    return __reshape_img


def image_check(image_path, target_size):
    try:
        cached_x_img = load_img(image_path, target_size=target_size)
        return cached_x_img
    except:
        logger.error("      Image Parsing Error " + str(image_path))
        return None


def image_show(numpy_array):
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(12, 9))

    sub_1 = fig.add_subplot(221)
    sub_1.imshow(numpy_array)

    plt.waitforbuttonpress()
    plt.close()
