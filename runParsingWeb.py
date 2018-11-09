from server import setup
from os import environ


def dev_server():
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000

    _ret_app = setup.create_app()
    _ret_app.run(host=HOST, port=PORT, threaded=True)


def main_server():
    _ret_app = setup.create_app()
    _ret_app.run(host='0.0.0.0', port=8080, threaded=True)


if __name__ == '__main__':
    main_server()