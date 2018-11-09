import sys


def command_parsing():
    get_command_line = sys.argv
    command_dict = dict()
    print(str(get_command_line))

    command_length = len(get_command_line)
    command_length = command_length - 1
    option_num = command_length // 2

    for idx in range(0, option_num):
        option_idx = (idx * 2 + 1)
        request_idx = option_idx + 1

        cached_option = get_command_line[option_idx]
        cached_option = (str(cached_option)).replace('-', '')
        cached_request = get_command_line[request_idx]
        command_dict[cached_option] = str(cached_request)

    print(str(command_dict))
    return command_dict
